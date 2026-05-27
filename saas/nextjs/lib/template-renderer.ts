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

function resolvePath(data: StrMap, context: StrMap, path: string): unknown {
  const parts = path.split(".");
  if (parts[0] === "data") {
    return get(data, parts.slice(1).join("."));
  }

  let cur: unknown = context[parts[0]];
  if (cur === undefined && isObj(data) && Object.prototype.hasOwnProperty.call(data, parts[0])) {
    cur = (data as StrMap)[parts[0]];
  }

  for (let i = 1; i < parts.length; i++) {
    if (!isObj(cur)) return "";
    cur = (cur as StrMap)[parts[i]];
  }

  return cur;
}

function replaceVariables(html: string, data: StrMap, context: StrMap): string {
  let result = html;

  result = result.replace(/\{\{\s*([a-zA-Z_][\w.]*)\s+or\s+"([^"\\]*)"\s*\}\}/g, (_1: string, path: string, def: string) => {
    const val = resolvePath(data, context, path.trim());
    return truthy(val) ? toStr(val) : def;
  });
  result = result.replace(/\{\{\s*([a-zA-Z_][\w.]*)\s+or\s+'([^'\\]*)'\s*\}\}/g, (_1: string, path: string, def: string) => {
    const val = resolvePath(data, context, path.trim());
    return truthy(val) ? toStr(val) : def;
  });
  result = result.replace(/\{\{\s*([a-zA-Z_][\w.]*)\s+or\s+([a-zA-Z_][\w.]*)\s*\}\}/g, (_1: string, path1: string, path2: string) => {
    const val1 = resolvePath(data, context, path1.trim());
    const val2 = resolvePath(data, context, path2.trim());
    return truthy(val1) ? toStr(val1) : toStr(val2);
  });
  result = result.replace(/\{\{\s*([a-zA-Z_][\w.]*)\s*\}\}/g, (_1: string, path: string) => {
    return toStr(resolvePath(data, context, path.trim()));
  });

  return result;
}

function evaluateCondition(data: StrMap, context: StrMap, condition: string): boolean {
  return condition
    .split(" and ")
    .map((part) => part.trim())
    .every((part) => truthy(resolvePath(data, context, part)));
}

function processIfBlocks(html: string, data: StrMap, context: StrMap): string {
  return html.replace(/\{%\s*if\s+([^%]+?)\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/g, (_: string, condition: string, body: string) => {
    return evaluateCondition(data, context, condition) ? body : "";
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
  function processTemplate(html: string, context: StrMap = {}): string {
    html = html.replace(
      /\{%\s*for\s+(\w+)\s+in\s+([a-zA-Z_][\w.]*)\s*%\}([\s\S]*?)\{%\s*endfor\s*%\}/g,
      (_: string, itemName: string, path: string, body: string) => {
        const arr = resolvePath(data, context, path);
        if (!isArr(arr) || arr.length === 0) return "";
        return arr
          .map((item) => {
            const childContext: StrMap = { ...context, [itemName]: item };
            return processTemplate(body, childContext);
          })
          .join("");
      }
    );

    let previous = "";
    while (previous !== html) {
      previous = html;
      html = processIfBlocks(html, data, context);
    }

    return replaceVariables(html, data, context);
  }

  return processTemplate(htmlTemplate);
}
