// API Route: POST /api/generate
// Generates a personal IP website from AI-analyzed 7 IP dimensions

import { NextRequest, NextResponse } from 'next/server';
import { renderPage } from '@/lib/html-renderer';

interface Dimension {
  icon: string;
  label: string;
  score: number;
  text: string;
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
  profile?: ProfileData;
  contact_email?: string;
  social_links?: Array<{ platform: string; url: string }>;
}

export async function POST(request: NextRequest) {
  try {
    const body: GenerateRequest = await request.json();
    const { dimensions, short_story, full_story, mbti, style, profile, contact_email, social_links } = body;

    if (!dimensions && !short_story && !full_story) {
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

    // Skills: extract from Skills dimension text
    const skillsText = profileData.skills.length > 0
      ? profileData.skills.join('、')
      : skillsDim?.text || '';

    // Work dimension text → projects
    const workText = workDim?.text || '';
    const projectTitles = profileData.projects.length > 0
      ? profileData.projects
      : workText
          .split(/[，。、\n]/)
          .map((item: string) => item.trim())
          .filter(Boolean)
          .filter(s => s.length > 3 && s.length < 50)
          .slice(0, 5);

    // Resources dimension text → social links (heuristic extraction if no social_links provided)
    const resourcesText = resourcesDim?.text || '';
    const socialLinksFromResources = social_links?.length > 0
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
      featured_projects: projectTitles.slice(0, 5),
    };

    // story.experiences = full_story (AI-generated narrative), NOT raw dimension text
    // story.insights = from Soul dimension (values, beliefs)
    // story.challenges = from Soul dimension (what they care about, growth direction)
    if (full_story || profileData.summary) {
      pageContent['story'] = {
        experiences: full_story || profileData.summary,
        insights: soulDim?.text || profileData.values.join('、') || '',
        challenges: soulDim?.text || profileData.direction.join('、') || '',
      };
    }

    // about.bio = from Framework dimension (methodology, decision logic)
    pageContent['about'] = {
      headline: nameVal,
      bio: frameworkDim?.text || profileData.education.join('；') || '',
      photo: '',
    };

    // Skills from Skills dimension
    if (skillsText || mbti) {
      const skillTags = skillsText
        ? skillsText
            .split(/[，、,\n]/)
            .map((s: string) => s.trim())
            .filter((s: string) => s.length > 0 && s.length < 20)
            .slice(0, 15)
        : [];

      pageContent['skills'] = {
        categories: [
          { name: '核心技能', items: skillTags },
          { name: 'MBTI', items: mbti ? [mbti] : [] },
        ],
      };
    }

    // Projects from Work dimension
    if (projectTitles.length > 0) {
      pageContent['projects'] = {
        projects: projectTitles.map((title: string) => ({
          title,
          year: '',
          role: roleVal,
          background: '',
          outcome: '',
          tags: skillsText
            ? skillsText.split(/[，、,\n]/).slice(0, 4).map((s: string) => s.trim())
            : profileData.skills.slice(0, 4),
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
    if (socialLinksFromResources !== undefined || social_links?.length > 0) {
      pageContent['social'] = {
        links: social_links || [],
      };
    }

    // Render
    const html = renderPage({
      designSystem: design,
      content: pageContent,
      selectedModules: ['hero_featured', 'about', 'story', 'skills', 'projects', 'awards', 'contact', 'social'],
      productType: 'personal_site',
    });

    const id = `site-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    return NextResponse.json({
      id,
      status: 'ready',
      html,
      message: 'Website generated successfully',
    });

  } catch (error) {
    console.error('Generation error:', error);
    return NextResponse.json(
      { error: 'Failed to generate website', details: String(error) },
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