/**
 * renderTemplate — Pure TypeScript template renderer for SaaS Vercel deployment.
 * Handles the Jinja2 syntax used in the 3 HTML templates without filesystem dependencies.
 */

type StrMap = Record<string, unknown>;

function isObj(v: unknown): v is StrMap {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}
function isArr(v: unknown): v is unknown[] {
  return Array.isArray(v);
}
function toStr(v: unknown): string {
  if (v === null || v === undefined) return "";
  if (typeof v === "string") return v;
  if (typeof v === "number") return String(v);
  if (typeof v === "boolean") return v ? "true" : "false";
  return JSON.stringify(v);
}

function get(data: StrMap, path: string): string {
  const parts = path.split(".");
  let cur: unknown = data;
  for (const p of parts) {
    if (!isObj(cur)) return "";
    cur = (cur as StrMap)[p];
  }
  return toStr(cur);
}

function getObj(data: StrMap, path: string): StrMap | null {
  const parts = path.split(".");
  let cur: unknown = data;
  for (const p of parts) {
    if (!isObj(cur)) return null;
    cur = (cur as StrMap)[p];
  }
  return isObj(cur) ? (cur as StrMap) : null;
}

function getArr(data: StrMap, path: string): unknown[] | null {
  const parts = path.split(".");
  let cur: unknown = data;
  for (const p of parts) {
    if (!isObj(cur)) return null;
    cur = (cur as StrMap)[p];
  }
  return isArr(cur) ? cur : null;
}

function truthy(v: unknown): boolean {
  return v !== null && v !== undefined && v !== false && v !== "" && !(typeof v === "number" && isNaN(v as number));
}

/**
 * Process Jinja2 `or` defaults in interpolation: {{ data.x or "default" }}
 * Must run before other replacements.
 */
function replaceOrDefaults(html: string): string {
  return html.replace(/\{\{\s*([^|}]+?)\s*or\s+"([^"]+)"\s*\}\}/g, (_1: string, path: string, def: string) => {
    const val = get({}, path.trim());
    return val !== "" ? val : def;
  }).replace(/\{\{\s*([^|}]+?)\s*or\s+'([^']+)'\s*\}\}/g, (_1: string, path: string, def: string) => {
    const val = get({}, path.trim());
    return val !== "" ? val : def;
  });
}

/** Process {% if data.x %}...{% endif %} */
function processIf(html: string, data: StrMap): string {
  const re = /\{%\s*if\s+([^%]+)\s*%\}[\s\S]*?\{%\s*endif\s*%\}/g;
  return html.replace(re, (block, cond) => {
    const trimmed = cond.trim();
    if (trimmed.startsWith("data.")) {
      const path = trimmed.slice(5);
      if (path.includes(".")) {
        const obj = getObj(data, path.split(".").slice(0, -1).join("."));
        const key = path.split(".").pop() || "";
        if (!truthy(obj && obj[key])) {
          const start = block.indexOf("{% if") + block.indexOf("%}") + 2;
          const end = block.lastIndexOf("{%");
          return "";
        }
        return block;
      }
      if (!truthy(data[path])) return "";
      return block;
    }
    return block;
  });
}

/** Process {% for item in data.items %}...{% endfor %} */
function processFor(html: string, data: StrMap): string {
  const re = /\{%\s*for\s+(\w+)\s+in\s+([\w.]+)\s*%\}([\s\S]*?)\{%\s*endfor\s*%\}/g;
  return html.replace(re, (_1: string, itemName: string, dataPath: string, body: string) => {
    const arr = getArr(data, dataPath);
    if (!arr || arr.length === 0) return "";
    return arr.map((item) => {
      if (!isObj(item)) return toStr(item);
      const itemMap = item as StrMap;
      // Replace {{ item.field }} or {{ data.field }} within the loop body
      let result = body;
      result = result.replace(/\{\{\s*item\.(\w+)\s*\}\}/g, (_: string, k: string) => toStr(itemMap[k]));
      result = result.replace(/\{\{\s*data\.(\w+)\s*\}\}/g, (_: string, k: string) => toStr(itemMap[k] ?? data[k]));
      result = result.replace(/\{\{\s*item\.(\w+)\s*\|\s*or\s+"([^"]+)"\s*\}\}/g, (_: string, k: string, def: string) => toStr(itemMap[k]) || def);
      result = result.replace(/\{\{\s*item\.(\w+)\s*\|\s*or\s+'([^']+)'\s*\}\}/g, (_: string, k: string, def: string) => toStr(itemMap[k]) || def);
      // Handle nested for loops within this item (e.g. project.tags)
      result = result.replace(
        /\{%\s*for\s+(\w+)\s+in\s+item\.(\w+)\s*%\}[\s\S]*?\{%\s*endfor\s*%\}/g,
        (_: string, tagName: string, tagPath: string) => {
          const tagArr = itemMap[tagPath];
          if (!isArr(tagArr)) return "";
          return tagArr.map((t) => {
            const tagStr = isObj(t) ? (t as StrMap).toString() : toStr(t);
            return tagStr;
          }).join("");
        }
      );
      return result;
    }).join("");
  });
}

/** Main render function */
export function renderTemplate(htmlTemplate: string, data: StrMap): string {
  let html = htmlTemplate;

  // 1. Handle `or` defaults in {{ }} interpolations
  html = html.replace(/\{\{\s*data\.([\w.]+)\s*or\s+"([^"]+)"\s*\}\}/g, (_1: string, path: string, def: string) => {
    const val = get(data, path);
    return val !== "" ? val : def;
  }).replace(/\{\{\s*data\.([\w.]+)\s*or\s+'([^']+)'\s*\}\}/g, (_1: string, path: string, def: string) => {
    const val = get(data, path);
    return val !== "" ? val : def;
  }).replace(/\{\{\s*data\.([\w.]+)\s*\}\}/g, (_1: string, path: string) => {
    const val = get(data, path);
    return val;
  });

  // 2. Process for loops (may need multiple passes for nested)
  for (let pass = 0; pass < 3; pass++) {
    const before = html;
    html = html.replace(
      /\{%\s*for\s+(\w+)\s+in\s+data\.([\w.]+)\s*%\}[\s\S]*?\{%\s*endfor\s*%\}/g,
      (block, itemName, dataPath) => {
        const arr = getArr(data, dataPath);
        if (!isArr(arr) || arr.length === 0) return "";
        const innerStart = block.indexOf("%}") + 2;
        const innerEnd = block.lastIndexOf("{%");
        const body = block.slice(innerStart, innerEnd);
        return arr.map((item) => {
          if (!isObj(item)) return toStr(item);
          const m = item as StrMap;
          let result = body;
          // item.field references
          result = result.replace(/\{\{\s*item\.(\w+)\s*\}\}/g, (_s: string, k: string) => toStr(m[k]));
          result = result.replace(/\{\{\s*item\.(\w+)\s*or\s+"([^"]+)"\s*\}\}/g, (_s: string, k: string, def: string) => toStr(m[k]) || def);
          result = result.replace(/\{\{\s*item\.(\w+)\s*or\s+'([^']+)'\s*\}\}/g, (_s: string, k: string, def: string) => toStr(m[k]) || def);
          // item.nested.field
          result = result.replace(/\{\{\s*item\.([\w.]+)\.(\w+)\s*\}\}/g, (_s: string, obj: string, k: string) => {
            const o = m[obj];
            return isObj(o) ? toStr((o as StrMap)[k]) : "";
          });
          // Handle inner for loops: {% for tag in item.tags %}
          result = result.replace(
            /\{%\s*for\s+(\w+)\s+in\s+item\.(\w+)\s*%\}[\s\S]*?\{%\s*endfor\s*%\}/g,
            (iblock: string, itag: string, ipath: string) => {
              const iarr = m[ipath];
              if (!isArr(iarr)) return "";
              const istart = iblock.indexOf("%}") + 2;
              const iend = iblock.lastIndexOf("{%");
              const ibody = iblock.slice(istart, iend);
              return iarr.map((t) => {
                if (isObj(t)) return ibody.replace(/\{\{\s*item\.(\w+)\s*\}\}/g, (_s2: string, k2: string) => toStr((t as StrMap)[k2]));
                return toStr(t);
              }).join("");
            }
          );
          return result;
        }).join("");
      }
    );
    if (html === before) break;
  }

  // 3. Process if blocks (remove entire {% if data.x %}...{% endif %} when falsey)
  html = html.replace(
    /\{%\s*if\s+data\.([\w.]+)\s*%\}[\s\S]*?\{%\s*endif\s*%\}/g,
    (block, path) => {
      const val = get(data, path.split(".")[0] === "data" ? path.slice(5) : path);
      return truthy(val) ? block : "";
    }
  );
  // Also handle {% if data.socials and data.socials.xxx %}
  html = html.replace(
    /\{%\s*if\s+data\.([\w.]+)\s+and\s+data\.([\w.]+)\s*%\}[\s\S]*?\{%\s*endif\s*%\}/g,
    (block, path1, path2) => {
      const v1 = get(data, path1);
      const v2 = get(data, path2);
      return truthy(v1) && truthy(v2) ? block : "";
    }
  );

  // 4. Clean up any raw Jinja2 tags left (shouldn't happen if above works)
  html = html.replace(/\{%[^%]*%\}/g, "");

  return html;
}