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

function parseLiteralOrPath(data: StrMap, context: StrMap, value: string): unknown {
  const trimmed = value.trim();
  if (/^".*"$/.test(trimmed) || /^'.*'$/.test(trimmed)) {
    return trimmed.slice(1, -1);
  }
  if (/^-?\d+(?:\.\d+)?$/.test(trimmed)) {
    return Number(trimmed);
  }
  if (trimmed === "true") return true;
  if (trimmed === "false") return false;
  return resolvePath(data, context, trimmed);
}

function resolvePath(data: StrMap, context: StrMap, path: string): unknown {
  const trimmed = path.trim();
  const lengthMatch = trimmed.match(/^(.*)\|length$/);
  if (lengthMatch) {
    const val = resolvePath(data, context, lengthMatch[1].trim());
    if (typeof val === "string" || isArr(val)) return (val as string | unknown[]).length;
    if (isObj(val)) return Object.keys(val).length;
    return 0;
  }

  const sliceMatch = trimmed.match(/^(.*)\[:(\d+)\]$/);
  if (sliceMatch) {
    const val = resolvePath(data, context, sliceMatch[1].trim());
    const count = Number(sliceMatch[2]);
    if (typeof val === "string") return (val as string).slice(0, count);
    if (isArr(val)) return (val as unknown[]).slice(0, count);
    return "";
  }

  const parts = trimmed.split(".");
  let cur: unknown;
  if (parts[0] === "data") {
    cur = data;
    parts.shift();
  } else {
    cur = context[parts[0]];
    if (cur === undefined && isObj(data) && Object.prototype.hasOwnProperty.call(data, parts[0])) {
      cur = (data as StrMap)[parts[0]];
    }
    parts.shift();
  }

  for (const part of parts) {
    if (!isObj(cur)) return "";
    cur = (cur as StrMap)[part];
  }

  return cur;
}

function replaceVariables(html: string, data: StrMap, context: StrMap): string {
  const expr = "[a-zA-Z_][\\w.]*?(?:\\[:\\d+\\])?(?:\\|length)?";
  let result = html;

  result = result.replace(new RegExp(`\\{\\{\\s*(${expr})\\s+or\\s+"([^"\\\\]*)"\\s*\\}\\}`, "g"), (_1: string, path: string, def: string) => {
    const val = resolvePath(data, context, path.trim());
    return truthy(val) ? toStr(val) : def;
  });
  result = result.replace(new RegExp(`\\{\\{\\s*(${expr})\\s+or\\s+'([^'\\\\]*)'\\s*\\}\\}`, "g"), (_1: string, path: string, def: string) => {
    const val = resolvePath(data, context, path.trim());
    return truthy(val) ? toStr(val) : def;
  });
  result = result.replace(new RegExp(`\\{\\{\\s*(${expr})\\s+or\\s+(${expr})\\s*\\}\\}`, "g"), (_1: string, path1: string, path2: string) => {
    const val1 = resolvePath(data, context, path1.trim());
    const val2 = resolvePath(data, context, path2.trim());
    return truthy(val1) ? toStr(val1) : toStr(val2);
  });
  result = result.replace(new RegExp(`\\{\\{\\s*(${expr})\\s*\\}\\}`, "g"), (_1: string, path: string) => {
    return toStr(resolvePath(data, context, path.trim()));
  });

  return result;
}

function evaluateCondition(data: StrMap, context: StrMap, condition: string): boolean {
  const expr = condition.trim();
  if (expr.includes(" or ")) {
    return expr.split(/\s+or\s+/).some((part) => evaluateCondition(data, context, part));
  }
  if (expr.includes(" and ")) {
    return expr.split(/\s+and\s+/).every((part) => evaluateCondition(data, context, part));
  }

  const stringCheck = expr.match(/^(.*)\s+is\s+string$/);
  if (stringCheck) {
    return typeof resolvePath(data, context, stringCheck[1].trim()) === "string";
  }

  const comparison = expr.match(/^(.*?)(==|!=|>=|<=|>|<)(.*)$/);
  if (comparison) {
    const left = resolvePath(data, context, comparison[1].trim());
    const right = parseLiteralOrPath(data, context, comparison[3].trim());
    if (comparison[2] === "==") return left === right;
    if (comparison[2] === "!=") return left !== right;
    const leftNum = typeof left === "number" ? left : Number(left);
    const rightNum = typeof right === "number" ? right : Number(right);
    if (Number.isNaN(leftNum) || Number.isNaN(rightNum)) {
      if (comparison[2] === ">") return toStr(left) > toStr(right);
      if (comparison[2] === "<") return toStr(left) < toStr(right);
      if (comparison[2] === ">=") return toStr(left) >= toStr(right);
      if (comparison[2] === "<=") return toStr(left) <= toStr(right);
      return false;
    }
    if (comparison[2] === ">=") return leftNum >= rightNum;
    if (comparison[2] === "<=") return leftNum <= rightNum;
    if (comparison[2] === ">") return leftNum > rightNum;
    if (comparison[2] === "<") return leftNum < rightNum;
  }

  return truthy(resolvePath(data, context, expr));
}

function processIfBlocks(
  html: string,
  data: StrMap,
  context: StrMap,
  processNested: (html: string, context: StrMap) => string
): string {
  const tagRegex = /\{%\s*(if|elif|else|endif)\b([^%]*)%\}/g;
  const tokens: Array<{ type: string; expr: string; index: number; end: number }> = [];
  let match: RegExpExecArray | null;

  while ((match = tagRegex.exec(html)) !== null) {
    tokens.push({
      type: match[1],
      expr: match[2].trim(),
      index: match.index,
      end: match.index + match[0].length,
    });
  }

  if (tokens.length === 0) return html;

  const stack: Array<{
    start: number;
    condition: string;
    ifTagEnd: number;
    elifs: Array<{ condition: string; start: number; end: number }>;
    elseStart: number | null;
    elseEnd: number | null;
    endifIndex: number | null;
    endifEnd: number | null;
  }> = [];
  const blocks: Array<{
    start: number;
    condition: string;
    ifTagEnd: number;
    elifs: Array<{ condition: string; start: number; end: number }>;
    elseStart: number | null;
    elseEnd: number | null;
    endifIndex: number;
    endifEnd: number;
  }> = [];

  for (const token of tokens) {
    if (token.type === "if") {
      stack.push({
        start: token.index,
        condition: token.expr,
        ifTagEnd: token.end,
        elifs: [],
        elseStart: null,
        elseEnd: null,
        endifIndex: null,
        endifEnd: null,
      });
      continue;
    }

    const current = stack[stack.length - 1];
    if (!current) continue;

    if (token.type === "elif" && current.elseStart === null && current.endifIndex === null) {
      current.elifs.push({ condition: token.expr, start: token.index, end: token.end });
      continue;
    }

    if (token.type === "else" && current.elseStart === null && current.endifIndex === null) {
      current.elseStart = token.index;
      current.elseEnd = token.end;
      continue;
    }

    if (token.type === "endif") {
      current.endifIndex = token.index;
      current.endifEnd = token.end;
      blocks.push(current as any);
      stack.pop();
    }
  }

  if (blocks.length === 0) return html;

  blocks.sort((a, b) => b.start - a.start);

  let result = html;
  const adjustments: Array<{ start: number; delta: number }> = [];
  const offsetAt = (pos: number) => adjustments.reduce((sum, adj) => (adj.start < pos ? sum + adj.delta : sum), 0);

  for (const block of blocks) {
    const ifStart = block.start + offsetAt(block.start);
    const ifEnd = block.ifTagEnd + offsetAt(block.ifTagEnd);
    const endifStart = block.endifIndex! + offsetAt(block.endifIndex!);
    const endifEnd = block.endifEnd! + offsetAt(block.endifEnd!);

    const branches: Array<{ condition: string | null; start: number; end: number }> = [];
    let cursor = ifEnd;
    let currentCondition: string | null = block.condition;

    for (const elif of block.elifs) {
      branches.push({ condition: currentCondition, start: cursor, end: elif.start + offsetAt(elif.start) });
      cursor = elif.end + offsetAt(elif.end);
      currentCondition = elif.condition;
    }

    if (block.elseStart !== null && block.elseEnd !== null) {
      branches.push({ condition: currentCondition, start: cursor, end: block.elseStart + offsetAt(block.elseStart) });
      branches.push({ condition: null, start: block.elseEnd + offsetAt(block.elseEnd), end: endifStart });
    } else {
      branches.push({ condition: currentCondition, start: cursor, end: endifStart });
    }

    let selected = "";
    for (const branch of branches) {
      const body = result.slice(branch.start, branch.end);
      if (branch.condition === null) {
        selected = body;
        break;
      }
      if (evaluateCondition(data, context, branch.condition)) {
        selected = body;
        break;
      }
    }

    const processed = processNested(selected, context);
    result = result.slice(0, ifStart) + processed + result.slice(endifEnd);
    adjustments.push({ start: block.start, delta: processed.length - (block.endifEnd! - block.start) });
  }

  return result;
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

/** Find the matching {% endfor %} for an {% for %} at startPos, returning the endfor position */
function findMatchingEndfor(html: string, startPos: number): number | null {
  // Find the end of the opening {% for ... %} tag
  const openTagEnd = html.indexOf('%}', startPos);
  if (openTagEnd === -1) return null;

  let depth = 1;
  let i = openTagEnd + 2; // Start scanning after the opening tag

  while (i < html.length && depth > 0) {
    // Find the next {%
    const nextTag = html.indexOf('{%', i);
    if (nextTag === -1) return null;

    const c13 = html.slice(nextTag, nextTag + 13);
    const c10 = html.slice(nextTag, nextTag + 10);
    const c11 = html.slice(nextTag, nextTag + 11);

    if (c11.startsWith('{% for ') || c10.startsWith('{%for ')) {
      depth++;
      i = nextTag + 11;
    } else if (c13.startsWith('{% endfor %}') || c13.startsWith('{%endfor%}')) {
      depth--;
      if (depth === 0) return nextTag;
      i = nextTag + 13;
    } else {
      i = nextTag + 2;
    }
  }
  return null;
}

/** Process {% for item in data.items %}...{% endfor %} with proper nested loop handling */
function processFor(html: string, data: StrMap, context: StrMap = {}): string {
  // Match {% for tag in path %}...{% endfor %} with proper nesting
  // We need to find the matching endfor by tracking nesting depth
  const forOpenRe = /\{%\s*for\s+(\w+)\s+in\s+([\w.]+)\s*%\}/g;
  let result = html;
  let offset = 0;

  // We can't use a simple regex replace because of nested loops
  // Instead, find each {% for %}, find its matching {% endfor %}, then replace
  const tokens: Array<{ openStart: number; openEnd: number; itemName: string; dataPath: string; bodyStart: number; bodyEnd: number; endforStart: number; endforEnd: number }> = [];

  // Find all {% for %} positions
  const openMatches: Array<{ index: number; itemName: string; dataPath: string; endTagPos: number }> = [];
  let m;
  const cloneRe = new RegExp(forOpenRe.source, forOpenRe.flags);
  while ((m = cloneRe.exec(html)) !== null) {
    openMatches.push({ index: m.index, itemName: m[1], dataPath: m[2], endTagPos: m.index + m[0].length });
  }

  // For each {% for %}, find its matching {% endfor %}
  for (const om of openMatches) {
    const endforPos = findMatchingEndfor(html, om.index);
    if (endforPos === null) continue;
    tokens.push({
      openStart: om.index,
      openEnd: om.endTagPos,
      itemName: om.itemName,
      dataPath: om.dataPath,
      bodyStart: om.endTagPos,
      bodyEnd: endforPos,
      endforStart: endforPos,
      endforEnd: endforPos + 13,
    });
  }

  // Sort by position descending (replace from end to start to preserve positions)
  tokens.sort((a, b) => b.openStart - a.openStart);

  for (const tok of tokens) {
    const body = result.slice(tok.bodyStart, tok.bodyEnd);
    const arr = resolvePath(data, context, tok.dataPath);
    if (!isArr(arr) || arr.length === 0) continue;
    const replacement = arr.map((item, idx) => {
      const itemMap = isObj(item) ? (item as StrMap) : {};
      // Bind current item to loop variable name
      const iterContext: StrMap = { ...context, [tok.itemName]: item };
      let res = body;
      // First recursively process any nested for loops
      res = processFor(res, data, iterContext);
      // Then replace {{ item.xxx }} and {{ item }} in the processed result
      res = res.replace(/\{\{\s*item\.(\w+)\s*\}\}/g, (_: string, k: string) => toStr(itemMap[k]));
      res = res.replace(/\{\{\s*data\.(\w+)\s*\}\}/g, (_: string, k: string) => toStr(itemMap[k] != null ? itemMap[k] : data[k]));
      res = res.replace(/\{\{\s*item\.(\w+)\s*\|\s*or\s+"([^"]+)"\s*\}\}/g, (_: string, k: string, def: string) => toStr(itemMap[k]) || def);
      res = res.replace(/\{\{\s*item\.(\w+)\s*\|\s*or\s+'([^']+)'\s*\}\}/g, (_: string, k: string, def: string) => toStr(itemMap[k]) || def);
      res = res.replace(/\{\{\s*item\s*\}\}/g, () => toStr(item));
      // Now replace remaining {{ ... }} (like {{ cat.name }}) using full context
      res = replaceVariables(res, data, iterContext);
      return res;
    }).join("");
    result = result.slice(0, tok.openStart) + replacement + result.slice(tok.endforEnd);
  }

  return result;
}

/** Main render function */

export function renderTemplate(htmlTemplate: string, data: StrMap): string {
  function processTemplate(html: string, context: StrMap = {}): string {
    // Use nesting-aware for loop processing
    html = processFor(html, data, context);

    let previous = "";
    while (previous !== html) {
      previous = html;
      html = processIfBlocks(html, data, context, processTemplate);
    }

    return replaceVariables(html, data, context);
  }

  return processTemplate(htmlTemplate);
}
