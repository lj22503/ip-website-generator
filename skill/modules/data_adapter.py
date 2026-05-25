"""
Data Adapters — Convert unified content JSON to each template's schema.

Each adapter takes the unified content JSON and returns a dict that
directly maps to the template's Jinja2 variable expectations.
"""

from typing import Any


def to_developerfolio(content: dict) -> dict:
    """Convert content JSON → developerFolio template data."""
    # Support both flat JSON and {"content": {...}} wrapped
    data = content.get("content", content)

    # Top-level fields (name/role live at JSON root, not inside content)
    name = content.get("name") or data.get("name", data.get("hero_name", ""))
    role = content.get("role") or data.get("role") or data.get("hero_label", "")

    # Socials — check top-level first, then data.socials (object or dict)
    socials = {}
    socials_source = data.get("socials", {})
    # Handle case where socials is a dict with nested {email, phone, github...} keys
    if isinstance(socials_source, dict):
        for key in ["github", "linkedin", "twitter", "email", "medium"]:
            val = (content.get(key) or data.get(key) or socials_source.get(key))
            if val:
                socials[key] = val
    # Handle contact as flat fields
    for key in ["email", "phone"]:
        if key not in socials:
            val = data.get(key) or (data.get("contact", {}) or {}).get(key)
            if val:
                socials[key] = val

    # Hero story — handle both dict and string
    hero_story = data.get("hero_story", {})
    if isinstance(hero_story, dict):
        headline = hero_story.get("headline", "")
        hero_subtitle = hero_story.get("subtitle", "")
    elif hero_story:
        headline = hero_story
        hero_subtitle = ""
    else:
        headline = data.get("headline", "")
        hero_subtitle = data.get("hero_subtitle", "")

    result = {
        "name": name,
        "title": role,
        "headline": headline,
        "hero_subtitle": hero_subtitle,
        "greeting": data.get("greeting", ""),
        "avatar": data.get("avatar", ""),
        "resume_url": data.get("resume_url", ""),
        "socials": socials,
        "accent_color": data.get("accent_color", "#55d4eb"),
        "accent_secondary": data.get("accent_secondary", "#a855f7"),
        "year": data.get("year", "2026"),
        "footer": data.get("footer", ""),
        "contact_heading": data.get("contact_heading", "保持联系"),
        "contact_subtitle": data.get("contact_subtitle", "我通常在24小时内回复合作邀请。"),
        "contact_note": data.get("contact_note", ""),
        "location": data.get("location", content.get("location", "")),
        "address": data.get("address", content.get("address", "")),
    }

    # Story — structured narrative with paragraphs
    if data.get("story"):
        story = data["story"]
        def to_paragraphs(text):
            if not text:
                return []
            return [p.strip() for p in text.split("\n\n") if p.strip()]
        result["story"] = {
            "experiences": story.get("experiences", ""),
            "experiences_paragraphs": to_paragraphs(story.get("experiences", "")),
            "challenges": story.get("challenges", ""),
            "challenges_paragraphs": to_paragraphs(story.get("challenges", "")),
            "insights": story.get("insights", ""),
            "insights_paragraphs": to_paragraphs(story.get("insights", "")),
        }

    # About
    if data.get("about"):
        about = data["about"]
        result["about"] = {
            "subtitle": about.get("subtitle", about.get("headline", "关于我")),
            "bio": about.get("bio", about.get("description", "")),
        }

    # Skills
    if data.get("skills"):
        skills = data["skills"]
        result["skills"] = {}
        if isinstance(skills, dict) and "categories" in skills:
            result["skills"]["categories"] = [
                {"name": cat.get("name", ""), "skill_list": cat.get("items", cat.get("skills", []))}
                if isinstance(cat, dict)
                else {"name": "技能", "skill_list": cat}
                for cat in skills["categories"]
            ]
        elif isinstance(skills, list):
            result["skills"]["categories"] = [
                {"name": "技能", "skill_list": skills}
            ]
        if isinstance(skills, dict) and "bars" in skills:
            result["skills"]["bars"] = skills["bars"]

    # Experience — only use story.experiences if it's a list of dicts, NOT a raw string
    if data.get("experience"):
        exps = data["experience"]
        if isinstance(exps, dict) and "items" in exps:
            result["experience"] = exps["items"]
        elif isinstance(exps, list):
            result["experience"] = exps
    elif data.get("story", {}).get("experiences"):
        story_exps = data["story"]["experiences"]
        # Only use as experience if it's a list of dicts (not a raw string narrative)
        if isinstance(story_exps, list) and any(isinstance(e, dict) for e in story_exps):
            result["experience"] = [
                {
                    "role": e.get("role", e.get("title", "")),
                    "company": e.get("company", ""),
                    "duration": e.get("period", e.get("duration", "")),
                    "location": e.get("location", ""),
                    "description": e.get("description", e.get("summary", "")),
                    "achievements": e.get("achievements", []),
                }
                for e in story_exps if isinstance(e, dict)
            ]

    # Education
    if data.get("education"):
        edu = data["education"]
        if isinstance(edu, list):
            result["education"] = edu
        elif isinstance(edu, dict):
            result["education"] = [edu]

    # Projects — support {"projects": [...]} or {"items": [...]} or [...]
    if data.get("projects"):
        projs = data["projects"]
        if isinstance(projs, dict):
            result["projects"] = projs.get("projects") or projs.get("items") or []
        elif isinstance(projs, list):
            result["projects"] = projs
        else:
            result["projects"] = []
        # Enrich with background/outcome from project entries
        for p in result.get("projects", []):
            if isinstance(p, dict):
                p.setdefault("description", p.get("background", p.get("desc", "")))
                p.setdefault("outcome", p.get("result", p.get("outcome", "")))

    # Achievements
    if data.get("achievements"):
        result["achievements"] = data["achievements"]

    # Blogs
    if data.get("blogs") or data.get("writing"):
        result["blogs"] = data.get("blogs") or data.get("writing")

    # Badges
    badges = data.get("badges", [])
    if isinstance(badges, list) and badges:
        result["badges"] = badges

    # ─── 7 IP Dimensions (Soul/Framework/Timeline/Resources/Form) ───
    story_data = data.get("story", {})

    # Soul: mbti + soul_statement (insights) + challenge_quote (challenges)
    result["mbti"] = story_data.get("mbti", "")
    result["mbti_description"] = story_data.get("mbti_description", "")
    result["soul_statement"] = story_data.get("insights", "")
    result["deepest_challenge"] = story_data.get("deepest_challenge", "")
    result["challenge_quote"] = story_data.get("challenges", "")

    # Framework: method cards from dedicated field or about.bio paragraphs
    framework_items = data.get("framework_items", [])
    if not framework_items and data.get("about"):
        about_bio = data["about"].get("bio", "")
        paras = [p.strip() for p in about_bio.split("\n\n") if p.strip()]
        framework_items = [
            {"number": str(i + 1), "title": p[:30], "description": p}
            for i, p in enumerate(paras) if p
        ][:5]
    result["framework_items"] = framework_items

    # Identity stats grid
    mbti_val = result["mbti"]
    skills_count = 0
    if data.get("skills"):
        cats = data["skills"].get("categories", [])
        skills_count = sum(len(c.get("items", [])) for c in cats if isinstance(c, dict))
    result["stats"] = {
        "mbti": mbti_val,
        "skills": skills_count,
        "years": "N年",
        "availability": "随时可联系",
    } if mbti_val or skills_count else None

    # Timeline: narrative entries from experience[] (year extracted from duration)
    import re as _re
    timeline = []
    for exp in result.get("experience", []):
        duration = exp.get("duration", "")
        year_m = _re.search(r'\d{4}', duration)
        year = year_m.group(0) if year_m else ""
        if year:
            timeline.append({
                "year": year,
                "title": exp.get("role", ""),
                "description": exp.get("description", ""),
            })
    result["timeline"] = timeline

    # Testimonials
    result["testimonials"] = data.get("testimonials", [])

    # Resources (for template use if needed)
    result["resources"] = data.get("resources", {})

    return result


def to_alfolio(content: dict) -> dict:
    """Convert content JSON → al-folio template data."""
    # Support both flat JSON and {"content": {...}} wrapped
    data = content.get("content", content)

    # Top-level fields (name/role live at JSON root)
    name = content.get("name") or data.get("name", data.get("hero_name", ""))
    role = content.get("role") or data.get("role") or data.get("hero_label", "")

    socials = {}
    for key in ["github", "linkedin", "twitter", "email"]:
        val = content.get(key) or data.get(key) or (data.get("socials", {}) or {}).get(key)
        if val:
            socials[key] = val
    # Handle phone for alfolio
    phone = data.get("phone") or (data.get("contact", {}) or {}).get("phone")
    if phone:
        socials["phone"] = phone

    # Hero story — handle both dict and string
    hero_story = data.get("hero_story", {})
    headline = ""
    hero_subtitle = ""
    if isinstance(hero_story, dict):
        headline = hero_story.get("headline", "")
        hero_subtitle = hero_story.get("subtitle", "")
    elif hero_story:
        headline = hero_story

    result = {
        "name": name,
        "title": role,
        "headline": headline,
        "hero_subtitle": hero_subtitle,
        "bio_short": data.get("about", {}).get("bio", "")[:120] if data.get("about", {}).get("bio") else "",
        "avatar": data.get("avatar", ""),
        "accent_color": data.get("accent_color", "#7c3aed"),
        "socials": socials,
        "address": data.get("location", data.get("address", "")),
    }

    # About — split bio into paragraphs
    if data.get("about"):
        about = data["about"]
        bio = about.get("bio", about.get("description", ""))
        paragraphs = [p.strip() for p in bio.split("\n\n") if p.strip()]
        result["about"] = {
            "paragraphs": paragraphs if paragraphs else [bio],
            "subtitle": about.get("subtitle", ""),
        }

    # Always surface story fields (even when about uses story as fallback)
    def to_paragraphs(text):
        if not text:
            return []
        return [p.strip() for p in text.split("\n\n") if p.strip()]
    if data.get("story"):
        story = data["story"]
        result["story"] = {
            "experiences": story.get("experiences", ""),
            "experiences_paragraphs": to_paragraphs(story.get("experiences", "")),
            "challenges": story.get("challenges", ""),
            "challenges_paragraphs": to_paragraphs(story.get("challenges", "")),
            "insights": story.get("insights", ""),
            "insights_paragraphs": to_paragraphs(story.get("insights", "")),
        }

    # News
    if data.get("news"):
        result["news"] = data["news"]

    # Publications
    if data.get("publications"):
        result["publications"] = data["publications"]

    # Projects
    if data.get("projects"):
        projs = data["projects"]
        if isinstance(projs, dict):
            projs = projs.get("projects") or projs.get("items") or []
        elif not isinstance(projs, list):
            projs = []
        result["projects"] = [
            {
                "name": p.get("title", p.get("name", "")),
                "description": p.get("description", p.get("background", "")),
                "outcome": p.get("outcome", p.get("result", "")),
                "tags": p.get("tags", []),
            }
            for p in projs
        ]

    # Skills — use "skill_list" to avoid Jinja2 dict.items() conflict
    if data.get("skills"):
        skills = data["skills"]
        if isinstance(skills, dict) and "categories" in skills:
            result["skills"] = [
                {"name": c.get("name", ""), "skill_list": c.get("items", [])}
                for c in skills["categories"]
            ]
        elif isinstance(skills, list):
            result["skills"] = [{"name": "技能", "skill_list": skills}]
        elif isinstance(skills, dict):
            result["skills"] = [
                {"name": k, "skill_list": v}
                for k, v in skills.items()
                if isinstance(v, list)
            ]

    # Experience
    if data.get("experience"):
        exps = data["experience"]
        if isinstance(exps, dict) and "items" in exps:
            exps = exps["items"]
        result["experience"] = [
            {
                "title": e.get("role", e.get("title", "")),
                "company": e.get("company", ""),
                "date": e.get("period", e.get("duration", "")),
                "description": e.get("description", ""),
            }
            for e in (exps if isinstance(exps, list) else [])
        ]

    # ─── 7 IP Dimensions ───
    story_data = data.get("story", {})
    result["mbti"] = story_data.get("mbti", "")
    result["mbti_description"] = story_data.get("mbti_description", "")
    result["soul_statement"] = story_data.get("insights", "")
    result["deepest_challenge"] = story_data.get("deepest_challenge", "")
    result["challenge_quote"] = story_data.get("challenges", "")

    framework_items = data.get("framework_items", [])
    if not framework_items and data.get("about"):
        about_bio = data["about"].get("bio", "")
        paras = [p.strip() for p in about_bio.split("\n\n") if p.strip()]
        framework_items = [
            {"number": str(i + 1), "title": p[:30], "description": p}
            for i, p in enumerate(paras) if p
        ][:5]
    result["framework_items"] = framework_items

    result["testimonials"] = data.get("testimonials", [])
    result["resources"] = data.get("resources", {})

    # Identity stats grid
    mbti_val = result["mbti"]
    skills_count = 0
    cats = data.get("skills", {}).get("categories", [])
    if isinstance(cats, list):
        skills_count = sum(len(c.get("items", [])) for c in cats if isinstance(c, dict))
    result["stats"] = {
        "mbti": mbti_val,
        "skills": skills_count,
        "years": "N年",
        "availability": "随时可联系",
    } if mbti_val or skills_count else None

    return result


def to_rahulbeniwal(content: dict) -> dict:
    """Convert content JSON → rahulbeniwal template data."""
    # Support both flat JSON and {"content": {...}} wrapped
    data = content.get("content", content)

    # Top-level fields (name/role live at JSON root)
    name = content.get("name") or data.get("name", data.get("hero_name", ""))
    role = content.get("role") or data.get("role") or data.get("hero_label", "")

    socials = {}
    for key in ["github", "linkedin", "twitter", "email"]:
        val = content.get(key) or data.get(key) or (data.get("socials", {}) or {}).get(key)
        if val:
            socials[key] = val
    # Handle phone for rahulbeniwal
    phone = data.get("phone") or (data.get("contact", {}) or {}).get("phone")
    if phone:
        socials["phone"] = phone

    # Hero story — handle both dict and string
    hero_story = data.get("hero_story", {})
    headline = ""
    hero_subtitle = ""
    if isinstance(hero_story, dict):
        headline = hero_story.get("headline", "")
        hero_subtitle = hero_story.get("subtitle", "")
    elif hero_story:
        headline = hero_story

    result = {
        "name": name,
        "title": role,
        "headline": headline,
        "hero_name": name,
        "hero_label": role or "Portfolio",
        "hero_tagline": hero_subtitle,
        "avatar": data.get("avatar", ""),
        "accent_color": data.get("accent_color", "#e8ff58"),
        "bg_color": data.get("bg_color", "#08080c"),
        "surface_color": data.get("surface_color", "#101018"),
        "location": data.get("location", ""),
        "available": data.get("available", ""),
        "contact_heading": data.get("contact_heading", "Let's work together."),
        "contact_subtitle": data.get("contact_subtitle", "我通常在24小时内回复合作邀请。"),
        "socials": socials,
        "year": data.get("year", "2026"),
        "footer": data.get("footer", ""),
    }

    # Hero meta
    hero_meta = data.get("hero_meta", [])
    if hero_meta:
        result["hero_meta"] = hero_meta

    # About
    if data.get("about"):
        about = data["about"]
        bio = about.get("bio", about.get("description", ""))
        paragraphs = [p.strip() for p in bio.split("\n\n") if p.strip()]
        first_para = paragraphs[0] if paragraphs else bio
        result["about"] = {
            "title": about.get("subtitle", about.get("headline", "About Me")),
            "image": about.get("image", ""),
            "paragraphs": paragraphs if paragraphs else [bio],
            "text": first_para,
        }
    elif data.get("story"):
        story = data["story"]
        parts = []
        if story.get("experiences"):
            parts.append(story["experiences"])
        if story.get("challenges"):
            parts.append(story["challenges"])
        if story.get("insights"):
            parts.append(story["insights"])
        combined = "\n\n".join(parts)
        paragraphs = [p.strip() for p in combined.split("\n\n") if p.strip()]
        result["about"] = {
            "title": "About Me",
            "text": paragraphs[0] if paragraphs else "",
            "paragraphs": paragraphs,
        }

    # Story — split into paragraphs for three phases
    if data.get("story"):
        story = data["story"]
        for key in ["experiences", "challenges", "insights"]:
            val = story.get(key, "")
            if val:
                if isinstance(val, str):
                    paras = [p.strip() for p in val.split("\n\n") if p.strip()]
                    story[key + "_paragraphs"] = paras
                else:
                    story[key + "_paragraphs"] = val
        result["story"] = story

    # Projects
    if data.get("projects"):
        projs = data["projects"]
        if isinstance(projs, dict) and "items" in projs:
            projs = projs["items"]
        result["projects"] = [
            {
                "title": p.get("title", p.get("name", "")),
                "summary": p.get("summary", p.get("description", "")),
                "description": p.get("description", ""),
                "year": p.get("year", ""),
                "role": p.get("role", ""),
                "outcome": p.get("outcome", p.get("result", "")),
                "tags": p.get("tags", []),
                "url": p.get("url", ""),
                "icon": p.get("icon", "layers"),
            }
            for p in (projs if isinstance(projs, list) else [])
        ]

    # Mini projects
    if data.get("mini_projects"):
        result["mini_projects"] = data["mini_projects"]

    # Skills — use "skill_list" to avoid Jinja2 dict.items() conflict
    if data.get("skills"):
        skills = data["skills"]
        if isinstance(skills, dict) and "categories" in skills:
            result["skills"] = [
                {"name": c.get("name", ""), "skill_list": c.get("items", [])}
                for c in skills["categories"]
            ]
        elif isinstance(skills, list):
            result["skills"] = [{"name": "技能", "skill_list": skills}]
        elif isinstance(skills, dict):
            result["skills"] = [
                {"name": k, "skill_list": v}
                for k, v in skills.items()
                if isinstance(v, list)
            ]

    # Open source
    if data.get("open_source"):
        result["open_source"] = data["open_source"]

    # Experience
    if data.get("experience"):
        exps = data["experience"]
        if isinstance(exps, dict) and "items" in exps:
            exps = exps["items"]
        result["experience"] = [
            {
                "role": e.get("role", e.get("title", "")),
                "company": e.get("company", ""),
                "period": e.get("period", e.get("duration", "")),
                "location": e.get("location", ""),
                "description": e.get("description", ""),
            }
            for e in (exps if isinstance(exps, list) else [])
        ]

    # ─── 7 IP Dimensions ───
    story_data = data.get("story", {})
    result["mbti"] = story_data.get("mbti", "")
    result["mbti_description"] = story_data.get("mbti_description", "")
    result["soul_statement"] = story_data.get("insights", "")
    result["deepest_challenge"] = story_data.get("deepest_challenge", "")
    result["challenge_quote"] = story_data.get("challenges", "")

    framework_items = data.get("framework_items", [])
    if not framework_items and data.get("about"):
        about_bio = data["about"].get("bio", "")
        paras = [p.strip() for p in about_bio.split("\n\n") if p.strip()]
        framework_items = [
            {"number": str(i + 1), "title": p[:30], "description": p}
            for i, p in enumerate(paras) if p
        ][:5]
    result["framework_items"] = framework_items

    result["testimonials"] = data.get("testimonials", [])
    result["resources"] = data.get("resources", {})

    # Identity stats grid
    mbti_val = result["mbti"]
    skills_count = 0
    cats = data.get("skills", {}).get("categories", [])
    if isinstance(cats, list):
        skills_count = sum(len(c.get("items", [])) for c in cats if isinstance(c, dict))
    result["stats"] = {
        "mbti": mbti_val,
        "skills": skills_count,
        "years": "N年",
        "availability": "随时可联系",
    } if mbti_val or skills_count else None

    return result


ADAPTERS = {
    "developerfolio": to_developerfolio,
    "alfolio": to_alfolio,
    "rahulbeniwal": to_rahulbeniwal,
}


def adapt(content: dict, template_name: str) -> dict:
    """Adapt unified content JSON to the target template's schema."""
    adapter = ADAPTERS.get(template_name)
    if not adapter:
        raise ValueError(f"Unknown template: {template_name}. Available: {list(ADAPTERS.keys())}")
    return adapter(content)
