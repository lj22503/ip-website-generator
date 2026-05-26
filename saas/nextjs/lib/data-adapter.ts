/**
 * Data Adapters — Convert unified content JSON to each template's data schema.
 * Ported from skill/modules/data_adapter.py (Python → TypeScript)
 */

type Content = Record<string, unknown>;
type Dict = Record<string, unknown>;
type List = unknown[];

function isDict(v: unknown): v is Dict {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}
function isList(v: unknown): v is List {
  return Array.isArray(v);
}
function isStr(v: unknown): v is string {
  return typeof v === "string";
}
function str(v: unknown, fallback = ""): string {
  return isStr(v) ? v : fallback;
}
function getDeep(obj: Dict, path: string, fallback = ""): string {
  const parts = path.split(".");
  let cur: unknown = obj;
  for (const p of parts) {
    if (!isDict(cur)) return fallback;
    cur = cur[p];
  }
  return isStr(cur) ? cur : fallback;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function toParagraphs(text: string): string[] {
  if (!text) return [];
  return text.split("\n\n").map((p) => p.trim()).filter((p) => p.length > 0);
}

function paragraphsFromText(text: string): string[] {
  if (!isStr(text) || !text) return [];
  return text.split("\n\n").map((p) => p.trim()).filter(Boolean);
}

function normalizeSkills(skills: unknown): Array<{ name: string; skill_list: string[] }> {
  if (!skills) return [];
  if (isDict(skills) && isList((skills as Dict).categories)) {
    return (skills as Dict).categories as List,
      [];
  }
  if (isDict(skills) && "categories" in (skills as Dict)) {
    const cats = (skills as Dict).categories as List;
    return cats.map((cat) => {
      if (isDict(cat)) {
        const items = (cat as Dict).items || (cat as Dict).skills || [];
        return { name: str((cat as Dict).name, ""), skill_list: items as string[] };
      }
      return { name: "技能", skill_list: cat as string[] };
    });
  }
  if (isList(skills)) {
    return [{ name: "技能", skill_list: skills as string[] }];
  }
  return [];
}

function extractProjects(projs: unknown): List {
  if (!projs) return [];
  if (isDict(projs)) {
    return ((projs as Dict).projects || (projs as Dict).items || []) as List;
  }
  if (isList(projs)) return projs;
  return [];
}

function extractExperience(exps: unknown): List {
  if (!exps) return [];
  if (isDict(exps) && "items" in (exps as Dict)) return (exps as Dict).items as List;
  if (isList(exps)) return exps;
  return [];
}

function generateFrameworkItems(aboutBio: string): Array<{ number: string; title: string; description: string }> {
  const paras = aboutBio.split("\n\n").map((p) => p.trim()).filter(Boolean);
  return paras.slice(0, 5).map((p, i) => ({
    number: String(i + 1),
    title: p.slice(0, 30),
    description: p,
  }));
}

function calcStats(data: Dict) {
  const mbti = str(data.mbti || "");
  let skillsCount = 0;
  const cats = (data.skills as Dict)?.categories as List || [];
  for (const cat of cats) {
    if (isDict(cat)) {
      const items = (cat as Dict).items as List || [];
      skillsCount += items.length;
    }
  }
  if (!mbti && !skillsCount) return null;
  return {
    mbti,
    skills: skillsCount,
    years: "N年",
    availability: "随时可联系",
  };
}

function extractTimeline(experience: List): Array<{ year: string; title: string; description: string }> {
  const timeline: Array<{ year: string; title: string; description: string }> = [];
  const yearRe = /\d{4}/;
  for (const exp of experience) {
    if (!isDict(exp)) continue;
    const duration = str((exp as Dict).duration || (exp as Dict).period || "");
    const match = yearRe.exec(duration);
    const year = match ? match[0] : "";
    if (year) {
      timeline.push({
        year,
        title: str((exp as Dict).role || (exp as Dict).title || ""),
        description: str((exp as Dict).description || ""),
      });
    }
  }
  return timeline;
}

// ── DeveloperFolio Adapter ──────────────────────────────────────────────────────

export interface DevfolioData {
  name: string;
  title: string;
  headline: string;
  hero_subtitle: string;
  greeting: string;
  avatar: string;
  resume_url: string;
  socials: Record<string, string>;
  accent_color: string;
  accent_secondary: string;
  year: string;
  footer: string;
  contact_heading: string;
  contact_subtitle: string;
  contact_note: string;
  location: string;
  address: string;
  about?: { subtitle: string; bio: string };
  story?: {
    experiences: string;
    experiences_paragraphs: string[];
    challenges: string;
    challenges_paragraphs: string[];
    insights: string;
    insights_paragraphs: string[];
  };
  skills?: {
    categories: Array<{ name: string; skill_list: string[] }>;
  };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  skills_bars?: any[];
  experience?: List;
  education?: List;
  projects?: List;
  achievements?: List;
  blogs?: List;
  badges?: List;
  mbti: string;
  mbti_description: string;
  soul_statement: string;
  deepest_challenge: string;
  challenge_quote: string;
  framework_items: List;
  stats: ReturnType<typeof calcStats>;
  timeline: Array<{ year: string; title: string; description: string }>;
  testimonials: List;
  resources: Dict;
}

export function toDeveloperfolio(content: Content): DevfolioData {
  const raw = isDict(content) && "content" in content ? content.content as Dict : content;
  const data = isDict(raw) ? raw : {};

  const name = str(content.name || data.name || data.hero_name || "");
  const role = str(content.role || data.role || data.hero_label || "");

  // Socials
  const socialsSource = (data.socials || {}) as Dict;
  const socials: Record<string, string> = {};
  for (const key of ["github", "linkedin", "twitter", "email", "medium"] as const) {
    const val = str(content[key] || data[key] || socialsSource[key] || "");
    if (val) socials[key] = val;
  }
  for (const key of ["email", "phone"] as const) {
    if (!socials[key]) {
      const val = str(data[key] || ((data.contact || {}) as Dict)[key] || "");
      if (val) socials[key] = val;
    }
  }

  // Hero story
  let headline = "";
  let heroSubtitle = "";
  const heroStory = data.hero_story;
  if (isDict(heroStory)) {
    headline = str((heroStory as Dict).headline || "");
    heroSubtitle = str((heroStory as Dict).subtitle || "");
  } else if (heroStory) {
    headline = str(heroStory);
  } else {
    headline = str(data.headline || "");
    heroSubtitle = str(data.hero_subtitle || "");
  }

  const result: DevfolioData = {
    name,
    title: role,
    headline,
    hero_subtitle: heroSubtitle,
    greeting: str(data.greeting || ""),
    avatar: str(data.avatar || ""),
    resume_url: str(data.resume_url || ""),
    socials,
    accent_color: str(data.accent_color || "#55d4eb"),
    accent_secondary: str(data.accent_secondary || "#a855f7"),
    year: str(data.year || "2026"),
    footer: str(data.footer || ""),
    contact_heading: str(data.contact_heading || "保持联系"),
    contact_subtitle: str(data.contact_subtitle || "我通常在24小时内回复合作邀请。"),
    contact_note: str(data.contact_note || ""),
    location: str(data.location || content.location || ""),
    address: str(data.address || content.address || ""),
    mbti: "",
    mbti_description: "",
    soul_statement: "",
    deepest_challenge: "",
    challenge_quote: "",
    framework_items: [],
    stats: null,
    timeline: [],
    testimonials: [],
    resources: {},
  };

  // Story
  if (isDict(data.story)) {
    const story = data.story as Dict;
    result.story = {
      experiences: str(story.experiences || ""),
      experiences_paragraphs: toParagraphs(str(story.experiences || "")),
      challenges: str(story.challenges || ""),
      challenges_paragraphs: toParagraphs(str(story.challenges || "")),
      insights: str(story.insights || ""),
      insights_paragraphs: toParagraphs(str(story.insights || "")),
    };
  }

  // About
  if (isDict(data.about)) {
    const about = data.about as Dict;
    result.about = {
      subtitle: str(about.subtitle || about.headline || "关于我"),
      bio: str(about.bio || about.description || ""),
    };
  }

  // Skills
  if (isDict(data.skills)) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const skillsAny: any = data.skills;
    const skillsCats: Dict = { categories: skillsAny.categories, items: skillsAny.items };
    const skillsBars: unknown = skillsAny.bars;
    result.skills = {
      categories: normalizeSkills(skillsCats),
    };
    if (skillsBars) {
      (result as any).skills_bars = skillsBars;
    }
  } else if (isList(data.skills)) {
    result.skills = { categories: normalizeSkills(data.skills) };
  }

  // Experience
  const exps = data.experience;
  if (exps) {
    result.experience = extractExperience(exps);
  } else if (isDict(data.story)) {
    const storyExp = (data.story as Dict).experiences;
    if (isList(storyExp) && storyExp.some((e) => isDict(e))) {
      result.experience = storyExp.map((e) => {
        if (!isDict(e)) return {};
        return {
          role: str((e as Dict).role || (e as Dict).title || ""),
          company: str((e as Dict).company || ""),
          duration: str((e as Dict).period || (e as Dict).duration || ""),
          location: str((e as Dict).location || ""),
          description: str((e as Dict).description || (e as Dict).summary || ""),
          achievements: (e as Dict).achievements || [],
        };
      });
    }
  }

  // Education
  const edu = data.education;
  if (edu) {
    result.education = isList(edu) ? edu : isDict(edu) ? [edu] : [];
  }

  // Projects
  const projs = data.projects;
  if (projs) {
    const extracted = extractProjects(projs);
    result.projects = extracted.map((p) => {
      if (!isDict(p)) return {};
      const pp = p as Dict;
      return {
        ...pp,
        description: str(pp.description || pp.background || pp.desc || ""),
        outcome: str(pp.outcome || pp.result || ""),
      };
    });
  }

  // Achievements
  if (data.achievements) result.achievements = data.achievements as List;

  // Blogs / Writing
  if (data.blogs || data.writing) result.blogs = (data.blogs || data.writing) as List;

  // Badges
  const badges = data.badges;
  if (isList(badges) && badges.length > 0) result.badges = badges;

  // ── 7 IP Dimensions ─────────────────────────────────────────────────────────
  const storyData = (data.story || {}) as Dict;
  result.mbti = str(storyData.mbti || "");
  result.mbti_description = str(storyData.mbti_description || "");
  result.soul_statement = str(storyData.insights || "");
  result.deepest_challenge = str(storyData.deepest_challenge || "");
  result.challenge_quote = str(storyData.challenges || "");

  // Framework
  let frameworkItems = (data.framework_items as List) || [];
  if (!frameworkItems.length && isDict(data.about)) {
    const bio = str((data.about as Dict).bio || "");
    frameworkItems = generateFrameworkItems(bio);
  }
  result.framework_items = frameworkItems;

  // Stats
  result.stats = calcStats(data);

  // Timeline
  if (result.experience) {
    result.timeline = extractTimeline(result.experience);
  }

  // Testimonials & Resources
  result.testimonials = (data.testimonials as List) || [];
  result.resources = (data.resources as Dict) || {};

  return result;
}

// ── AlFolio Adapter ────────────────────────────────────────────────────────────

export interface AlfolioData {
  name: string;
  title: string;
  headline: string;
  hero_subtitle: string;
  bio_short: string;
  avatar: string;
  accent_color: string;
  socials: Record<string, string>;
  address: string;
  about?: { paragraphs: string[]; subtitle: string };
  story?: {
    experiences: string;
    experiences_paragraphs: string[];
    challenges: string;
    challenges_paragraphs: string[];
    insights: string;
    insights_paragraphs: string[];
  };
  news?: List;
  publications?: List;
  projects?: List;
  skills?: List;
  experience?: List;
  mbti: string;
  mbti_description: string;
  soul_statement: string;
  deepest_challenge: string;
  challenge_quote: string;
  framework_items: List;
  stats: ReturnType<typeof calcStats>;
  testimonials: List;
  resources: Dict;
}

export function toAlfolio(content: Content): AlfolioData {
  const raw = isDict(content) && "content" in content ? content.content as Dict : content;
  const data = isDict(raw) ? raw : {};

  const name = str(content.name || data.name || data.hero_name || "");
  const role = str(content.role || data.role || data.hero_label || "");

  const socials: Record<string, string> = {};
  for (const key of ["github", "linkedin", "twitter", "email"] as const) {
    const val = str(content[key] || data[key] || ((data.socials || {}) as Dict)[key] || "");
    if (val) socials[key] = val;
  }
  const phone = str(data.phone || ((data.contact || {}) as Dict).phone || "");
  if (phone) socials.phone = phone;

  let headline = "";
  let heroSubtitle = "";
  const heroStory = data.hero_story;
  if (isDict(heroStory)) {
    headline = str((heroStory as Dict).headline || "");
    heroSubtitle = str((heroStory as Dict).subtitle || "");
  } else if (heroStory) {
    headline = str(heroStory);
  }

  const result: AlfolioData = {
    name,
    title: role,
    headline,
    hero_subtitle: heroSubtitle,
    bio_short: isDict(data.about) ? str((data.about as Dict).bio || "").slice(0, 120) : "",
    avatar: str(data.avatar || ""),
    accent_color: str(data.accent_color || "#7c3aed"),
    socials,
    address: str(data.location || data.address || ""),
    mbti: "",
    mbti_description: "",
    soul_statement: "",
    deepest_challenge: "",
    challenge_quote: "",
    framework_items: [],
    stats: null,
    testimonials: [],
    resources: {},
  };

  // About
  if (isDict(data.about)) {
    const about = data.about as Dict;
    const bio = str(about.bio || about.description || "");
    const paragraphs = paragraphsFromText(bio);
    result.about = {
      paragraphs: paragraphs.length > 0 ? paragraphs : [bio],
      subtitle: str(about.subtitle || ""),
    };
  }

  // Story
  if (isDict(data.story)) {
    const story = data.story as Dict;
    result.story = {
      experiences: str(story.experiences || ""),
      experiences_paragraphs: toParagraphs(str(story.experiences || "")),
      challenges: str(story.challenges || ""),
      challenges_paragraphs: toParagraphs(str(story.challenges || "")),
      insights: str(story.insights || ""),
      insights_paragraphs: toParagraphs(str(story.insights || "")),
    };
  }

  // News
  if (data.news) result.news = data.news as List;

  // Publications
  if (data.publications) result.publications = data.publications as List;

  // Projects
  const projs = data.projects;
  if (projs) {
    const extracted = extractProjects(projs);
    result.projects = extracted.map((p) => {
      if (!isDict(p)) return {};
      const pp = p as Dict;
      return {
        name: str(pp.title || pp.name || ""),
        description: str(pp.description || pp.background || ""),
        outcome: str(pp.outcome || pp.result || ""),
        tags: (pp.tags as List) || [],
      };
    });
  }

  // Skills
  if (data.skills) {
    const skills = data.skills;
    if (isDict(skills) && (skills as Dict).categories) {
      result.skills = ((skills as Dict).categories as List).map((c) => {
        if (isDict(c)) return { name: str((c as Dict).name || ""), skill_list: ((c as Dict).items as List) || [] };
        return { name: "技能", skill_list: c as string[] };
      });
    } else if (isList(skills)) {
      result.skills = [{ name: "技能", skill_list: skills as string[] }];
    } else if (isDict(skills)) {
      result.skills = Object.entries(skills)
        .filter(([, v]) => isList(v))
        .map(([k, v]) => ({ name: k, skill_list: v as string[] }));
    }
  }

  // Experience
  const exps = data.experience;
  if (exps) {
    const extracted = extractExperience(exps);
    result.experience = extracted.map((e) => {
      if (!isDict(e)) return {};
      const ee = e as Dict;
      return {
        title: str(ee.role || ee.title || ""),
        company: str(ee.company || ""),
        date: str(ee.period || ee.duration || ""),
        description: str(ee.description || ""),
      };
    });
  }

  // ── 7 IP Dimensions ──────────────────────────────────────────────────────────
  const storyData = (data.story || {}) as Dict;
  result.mbti = str(storyData.mbti || "");
  result.mbti_description = str(storyData.mbti_description || "");
  result.soul_statement = str(storyData.insights || "");
  result.deepest_challenge = str(storyData.deepest_challenge || "");
  result.challenge_quote = str(storyData.challenges || "");

  let frameworkItems = (data.framework_items as List) || [];
  if (!frameworkItems.length && isDict(data.about)) {
    const bio = str((data.about as Dict).bio || "");
    frameworkItems = generateFrameworkItems(bio);
  }
  result.framework_items = frameworkItems;

  result.testimonials = (data.testimonials as List) || [];
  result.resources = (data.resources as Dict) || {};
  result.stats = calcStats(data);

  return result;
}

// ── RahulBeniwal Adapter ──────────────────────────────────────────────────────

export interface RahulData {
  name: string;
  title: string;
  headline: string;
  hero_name: string;
  hero_label: string;
  hero_tagline: string;
  avatar: string;
  accent_color: string;
  bg_color: string;
  surface_color: string;
  location: string;
  available: string;
  contact_heading: string;
  contact_subtitle: string;
  socials: Record<string, string>;
  year: string;
  footer: string;
  hero_meta: List;
  about?: { title: string; image: string; paragraphs: string[]; text: string };
  story?: Dict;
  projects?: List;
  mini_projects?: List;
  skills?: List;
  open_source?: List;
  experience?: List;
  mbti: string;
  mbti_description: string;
  soul_statement: string;
  deepest_challenge: string;
  challenge_quote: string;
  framework_items: List;
  stats: ReturnType<typeof calcStats>;
  testimonials: List;
  resources: Dict;
}

export function toRahulbeniwal(content: Content): RahulData {
  const raw = isDict(content) && "content" in content ? content.content as Dict : content;
  const data = isDict(raw) ? raw : {};

  const name = str(content.name || data.name || data.hero_name || "");
  const role = str(content.role || data.role || data.hero_label || "");

  const socials: Record<string, string> = {};
  for (const key of ["github", "linkedin", "twitter", "email"] as const) {
    const val = str(content[key] || data[key] || ((data.socials || {}) as Dict)[key] || "");
    if (val) socials[key] = val;
  }
  const phone = str(data.phone || ((data.contact || {}) as Dict).phone || "");
  if (phone) socials.phone = phone;

  let headline = "";
  let heroSubtitle = "";
  const heroStory = data.hero_story;
  if (isDict(heroStory)) {
    headline = str((heroStory as Dict).headline || "");
    heroSubtitle = str((heroStory as Dict).subtitle || "");
  } else if (heroStory) {
    headline = str(heroStory);
  }

  const result: RahulData = {
    name,
    title: role,
    headline,
    hero_name: name,
    hero_label: role || "Portfolio",
    hero_tagline: heroSubtitle,
    avatar: str(data.avatar || ""),
    accent_color: str(data.accent_color || "#e8ff58"),
    bg_color: str(data.bg_color || "#08080c"),
    surface_color: str(data.surface_color || "#101018"),
    location: str(data.location || ""),
    available: str(data.available || ""),
    contact_heading: str(data.contact_heading || "Let's work together."),
    contact_subtitle: str(data.contact_subtitle || "我通常在24小时内回复合作邀请。"),
    socials,
    year: str(data.year || "2026"),
    footer: str(data.footer || ""),
    hero_meta: (data.hero_meta as List) || [],
    mbti: "",
    mbti_description: "",
    soul_statement: "",
    deepest_challenge: "",
    challenge_quote: "",
    framework_items: [],
    stats: null,
    testimonials: [],
    resources: {},
  };

  // About
  if (isDict(data.about)) {
    const about = data.about as Dict;
    const bio = str(about.bio || about.description || "");
    const paragraphs = paragraphsFromText(bio);
    result.about = {
      title: str(about.subtitle || about.headline || "About Me"),
      image: str(about.image || ""),
      paragraphs: paragraphs.length > 0 ? paragraphs : [bio],
      text: paragraphs[0] || bio,
    };
  } else if (isDict(data.story)) {
    const story = data.story as Dict;
    const parts: string[] = [];
    if (story.experiences) parts.push(str(story.experiences));
    if (story.challenges) parts.push(str(story.challenges));
    if (story.insights) parts.push(str(story.insights));
    const combined = parts.join("\n\n");
    const paragraphs = paragraphsFromText(combined);
    result.about = {
      title: "About Me",
      text: paragraphs[0] || "",
      paragraphs,
      image: "",
    };
  }

  // Story
  if (isDict(data.story)) {
    const story = data.story as Dict;
    const storyOut: Dict = { ...story };
    for (const key of ["experiences", "challenges", "insights"] as const) {
      const val = story[key];
      if (val && isStr(val)) {
        storyOut[key + "_paragraphs"] = toParagraphs(str(val));
      } else if (isList(val)) {
        storyOut[key + "_paragraphs"] = val;
      }
    }
    result.story = storyOut;
  }

  // Projects
  const projs = data.projects;
  if (projs) {
    const extracted = (isDict(projs) ? (projs as Dict).items || (projs as Dict).projects || [] : projs) as List;
    result.projects = extracted.map((p) => {
      if (!isDict(p)) return {};
      const pp = p as Dict;
      return {
        title: str(pp.title || pp.name || ""),
        summary: str(pp.summary || pp.description || ""),
        description: str(pp.description || ""),
        year: str(pp.year || ""),
        role: str(pp.role || ""),
        outcome: str(pp.outcome || pp.result || ""),
        tags: (pp.tags as List) || [],
        url: str(pp.url || ""),
        icon: str(pp.icon || "layers"),
      };
    });
  }

  // Mini projects
  if (data.mini_projects) result.mini_projects = data.mini_projects as List;

  // Skills
  if (data.skills) {
    const skills = data.skills;
    if (isDict(skills) && (skills as Dict).categories) {
      result.skills = ((skills as Dict).categories as List).map((c) => {
        if (isDict(c)) return { name: str((c as Dict).name || ""), skill_list: ((c as Dict).items as List) || [] };
        return { name: "技能", skill_list: c as string[] };
      });
    } else if (isList(skills)) {
      result.skills = [{ name: "技能", skill_list: skills as string[] }];
    } else if (isDict(skills)) {
      result.skills = Object.entries(skills)
        .filter(([, v]) => isList(v))
        .map(([k, v]) => ({ name: k, skill_list: v as string[] }));
    }
  }

  // Open source
  if (data.open_source) result.open_source = data.open_source as List;

  // Experience
  const exps = data.experience;
  if (exps) {
    const extracted = extractExperience(exps);
    result.experience = extracted.map((e) => {
      if (!isDict(e)) return {};
      const ee = e as Dict;
      return {
        role: str(ee.role || ee.title || ""),
        company: str(ee.company || ""),
        period: str(ee.period || ee.duration || ""),
        location: str(ee.location || ""),
        description: str(ee.description || ""),
      };
    });
  }

  // ── 7 IP Dimensions ──────────────────────────────────────────────────────────
  const storyData = (data.story || {}) as Dict;
  result.mbti = str(storyData.mbti || "");
  result.mbti_description = str(storyData.mbti_description || "");
  result.soul_statement = str(storyData.insights || "");
  result.deepest_challenge = str(storyData.deepest_challenge || "");
  result.challenge_quote = str(storyData.challenges || "");

  let frameworkItems = (data.framework_items as List) || [];
  if (!frameworkItems.length && isDict(data.about)) {
    const bio = str((data.about as Dict).bio || "");
    frameworkItems = generateFrameworkItems(bio);
  }
  result.framework_items = frameworkItems;

  result.testimonials = (data.testimonials as List) || [];
  result.resources = (data.resources as Dict) || {};
  result.stats = calcStats(data);

  return result;
}

// ── Main adapt function ────────────────────────────────────────────────────────

export type TemplateName = "developerfolio" | "alfolio" | "rahulbeniwal";

export function adapt(content: Content, templateName: TemplateName): DevfolioData | AlfolioData | RahulData {
  switch (templateName) {
    case "developerfolio": return toDeveloperfolio(content);
    case "alfolio": return toAlfolio(content);
    case "rahulbeniwal": return toRahulbeniwal(content);
    default:
      throw new Error(`Unknown template: ${templateName}. Available: developerfolio, alfolio, rahulbeniwal`);
  }
}