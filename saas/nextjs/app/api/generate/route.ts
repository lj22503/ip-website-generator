// API Route: POST /api/generate
// Generates a personal IP website from AI-analyzed 7 IP dimensions
// Supports both renderPage() mode (legacy) and Jinja2 template mode (new)

import { NextRequest, NextResponse } from 'next/server';
import { renderPage } from '@/lib/html-renderer';
import { adapt, TemplateName } from '@/lib/data-adapter';
import { renderTemplate } from '@/lib/template-renderer';
import developerfolioHtml from '@/lib/html-templates/developerfolio/template.html';
import alfolioHtml from '@/lib/html-templates/alfolio/template.html';
import rahulbeniwalHtml from '@/lib/html-templates/rahulbeniwal/template.html';

interface Dimension {
  icon: string;
  label: string;
  score: number;
  text: string;
  sub_labels?: Array<{
    title: string;
    description: string;
    outcome?: string;
    tags?: string[];
  }>;
}

interface ProfileData {
  name: string;
  role: string;
  company: string;
  skills: string[];
  education: string[];
  projects: string[];
  achievements: string[];
  values: string[];
  direction: string[];
  summary: string;
}

interface GenerateRequest {
  dimensions: Dimension[];
  short_story: string;
  full_story: string;
  mbti: string;
  style: string;
  template?: TemplateName;
  profile?: ProfileData;
  contact_email?: string;
  social_links?: Array<{ platform: string; url: string }>;
  content?: Record<string, unknown>;
}

export async function POST(request: NextRequest) {
  try {
    const body: GenerateRequest = await request.json();
    const { dimensions, short_story, full_story, mbti, style, profile, contact_email, social_links } = body;

    if (!dimensions && !short_story && !full_story && !profile) {
      return NextResponse.json(
        { error: 'Missing content: dimensions or stories required' },
        { status: 400 }
      );
    }

    const design = style || 'notion';
    const profileData = profile || {
      name: '我',
      role: '创作者',
      company: '',
      skills: [],
      education: [],
      projects: [],
      achievements: [],
      values: [],
      direction: [],
      summary: short_story || full_story || '',
    };

    // Map new 7 IP dimensions by label
    const soulDim = dimensions?.find(d => d.label === 'Soul');
    const frameworkDim = dimensions?.find(d => d.label === 'Framework');
    const skillsDim = dimensions?.find(d => d.label === 'Skills');
    const workDim = dimensions?.find(d => d.label === 'Work');
    const timelineDim = dimensions?.find(d => d.label === 'Timeline');
    const resourcesDim = dimensions?.find(d => d.label === 'Resources');
    const formDim = dimensions?.find(d => d.label === 'Form');

    const nameVal = profileData.name || short_story?.split(/[，。\n]/)[0]?.replace(/^(他|她|这)/, '')?.trim() || '我';
    const roleVal = profileData.role || frameworkDim?.text?.match(/\b(工程师|经理|总监|创始人|设计师|产品|运营|市场|销售|研发|技术|前端|后端|全栈|创作者)\b/)?.[0] || '创作者';

    // Skills: sub_labels as categories [{name, skill_list}]
    const skillsSubLabels = skillsDim?.sub_labels || [];
    const skillsCategories = skillsSubLabels
      .filter((sl: any) => sl.tags && sl.tags.length > 0)
      .map((sl: any) => ({ name: sl.title, skill_list: sl.tags }));

    // Work dimension sub_labels → projects
    const workSubLabels = workDim?.sub_labels || [];

    // Resources dimension text → social links (heuristic extraction if no social_links provided)
    const resourcesText = resourcesDim?.text || '';
    const socialLinksFromResources = (social_links?.length ?? 0) > 0
      ? social_links
      : (resourcesText.includes('人脉') || resourcesText.includes('资源') || resourcesText.includes('合作'))
        ? []
        : undefined;

    // Form dimension text → brand keywords for hero subtitle
    const formText = formDim?.text || '';
    const brandKeywords = formText
      .split(/[，。、\n]/)
      .map((s: string) => s.trim())
      .filter(Boolean)
      .filter(s => s.length > 1 && s.length < 20)
      .slice(0, 3);

    const pageContent: Record<string, any> = {};

    // hero_featured: title from name, subtitle from role + brand keywords
    pageContent['hero_featured'] = {
      title: nameVal,
      subtitle: [roleVal, ...brandKeywords].filter(Boolean).join(' · '),
      featured_projects: workSubLabels.slice(0, 5).map((sl: any) => sl.title),
    };

    // story.experiences = full_story (AI-generated narrative), NOT raw dimension text
    // story.insights = from Soul dimension (values, beliefs)
    // story.challenges = from Soul dimension (what they care about, growth direction)
    if (full_story || profileData.summary) {
      pageContent['story'] = {
        experiences: full_story || profileData.summary,
        insights: soulDim?.text || (Array.isArray(profileData.values) ? profileData.values.join('、') : '') || '',
        challenges: soulDim?.text || (Array.isArray(profileData.direction) ? profileData.direction.join('、') : '') || '',
      };
    }

    // about.bio = from Framework dimension (methodology, decision logic)
    pageContent['about'] = {
      headline: nameVal,
      bio: frameworkDim?.text || (Array.isArray(profileData.education) ? profileData.education.join('；') : '') || '',
      photo: '',
    };

    // Skills from Skills dimension sub_labels
    if (skillsCategories.length > 0 || mbti) {
      pageContent['skills'] = {
        categories: [
          ...skillsCategories,
          ...(mbti ? [{ name: 'MBTI', items: [mbti] }] : []),
        ],
      };
    }

    // Projects from Work dimension sub_labels
    if (workSubLabels.length > 0) {
      pageContent['projects'] = {
        projects: workSubLabels.map((sl) => ({
          title: sl.title,
          description: sl.description,
          outcome: sl.outcome || '',
          tags: sl.tags || [],
          url: '',
        })),
      };
    }

    // Awards: none in new dimensions, skip or use placeholder
    // (If needed, could derive from work/soul text heuristically)

    if (contact_email || social_links) {
      pageContent['contact'] = {
        email: contact_email || '',
        links: social_links || [],
      };
    }

    // Social links from Resources dimension or provided social_links
    if (socialLinksFromResources !== undefined || (social_links?.length ?? 0) > 0) {
      pageContent['social'] = {
        links: social_links || [],
      };
    }

    // Render
    let html: string;
    const template = body.template;
    if (template) {
      // ── Jinja2 template mode ──
      // Use profileData as content directly (has name/role/skills/etc.)
      // Fall back to building from dimensions if no profile provided
      let content: Record<string, unknown> = {};
      if (profileData.name && profileData.name !== '我') {
        // Build from profile data (comes from buildProfileData which has name/role/company/skills/...)
        content = {
          name: profileData.name,
          role: profileData.role,
          title: profileData.role,
          bio: frameworkDim?.text || profileData.summary || '',
          company: profileData.company,
          skills: profileData.skills?.length
            ? { categories: [{ name: '技能', skill_list: profileData.skills }] }
            : { categories: [] },
          education: profileData.education,
          projects: Array.isArray(profileData.projects) ? profileData.projects.map((title: string) => ({ title, description: '', outcome: '' })) : [],
          achievements: profileData.achievements,
          socials: {},
          mbti: mbti,
          story: {
            experiences: full_story || profileData.summary || '',
            insights: soulDim?.text || (Array.isArray(profileData.values) ? profileData.values.join('、') : '') || '',
            challenges: soulDim?.text || (Array.isArray(profileData.direction) ? profileData.direction.join('、') : '') || '',
          },
        };
      } else {
        // Build minimal content from dimensions
        content = {
          name: nameVal || '我',
          role: roleVal || '创作者',
          title: [roleVal, ...brandKeywords].filter(Boolean).join(' · '),
          bio: frameworkDim?.text || '',
          skills: skillsCategories.length > 0 ? { categories: skillsCategories } : { categories: [] },
          projects: workSubLabels.map((sl) => ({
            title: sl.title,
            description: sl.description,
            outcome: sl.outcome || '',
          })),
          story: {
            experiences: full_story || '',
            insights: soulDim?.text || '',
            challenges: soulDim?.text || '',
          },
          socials: {},
          mbti: mbti,
        };
      }
      const templateData = adapt(content as Record<string, unknown>, template);
      const templateHtml =
        template === 'developerfolio' ? developerfolioHtml :
        template === 'alfolio' ? alfolioHtml :
        template === 'rahulbeniwal' ? rahulbeniwalHtml :
        developerfolioHtml;
      html = renderTemplate(templateHtml, templateData as unknown as Record<string, unknown>);
    } else {
      // ── Legacy renderPage mode ──
      html = renderPage({
        designSystem: design,
        content: pageContent,
        selectedModules: ['hero_featured', 'about', 'story', 'skills', 'projects', 'awards', 'contact', 'social'],
        productType: 'personal_site',
      });
    }

    const id = `site-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    return NextResponse.json({
      id,
      status: 'ready',
      html,
      message: 'Website generated successfully',
    });

  } catch (error: unknown) {
    console.error('Generation error:', error);
    const errMsg = error instanceof Error ? error.message : String(error);
    const errStack = error instanceof Error ? error.stack : '';
    return NextResponse.json(
      { error: 'Failed to generate website', details: `${errMsg}\n${errStack}` },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    endpoints: {
      POST: {
        description: 'Generate a personal IP website from AI-analyzed 7 IP dimensions',
        body: {
          dimensions: '[{ icon, label, score, text }] — labels: Soul/Framework/Skills/Work/Timeline/Resources/Form',
          short_story: 'string (50 chars)',
          full_story: 'string (150 chars)',
          mbti: 'string',
          style: 'design system name',
          profile: 'optional',
          contact_email: 'optional',
          social_links: '[{ platform, url }]',
        },
      },
    },
    designs: [
      'notion', 'linear.app', 'stripe', 'figma', 'apple', 'framer',
      'airbnb', 'spotify', 'vercel', 'claude', 'cohere', 'ollama',
      'x.ai', 'minimax', 'raycast', 'supabase', 'resend', 'sentry',
      'mintlify', 'cursor', 'cal.com', 'loom', 'inter', 'miro',
      'airtable', 'spacex', 'revolut', 'sanity', 'mongodb', 'hashicorp',
      'clickhouse',
    ],
  });
}