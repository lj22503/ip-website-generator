// API Route: POST /api/generate
// Generates a personal IP website from AI-analyzed dimensions

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

    const careerDim = dimensions?.find(d => d.label.includes('职业'));
    const skillsDim = dimensions?.find(d => d.label.includes('技能') || d.label.includes('核心'));
    const eduDim = dimensions?.find(d => d.label.includes('教育'));
    const highlightDim = dimensions?.find(d => d.label.includes('成就') || d.label.includes('亮点'));
    const projectDim = dimensions?.find(d => d.label.includes('项目') || d.label.includes('成就'));
    const insightDim = dimensions?.find(d => d.label.includes('洞察') || d.label.includes('特质'));
    const potentialDim = dimensions?.find(d => d.label.includes('潜力'));

    const nameVal = profileData.name || careerDim?.text?.split(/[，。\n]/)[0]?.trim() || '我';
    const roleVal = profileData.role || careerDim?.text?.match(/\b(工程师|经理|总监|创始人|设计师|产品|运营|市场|销售|研发|技术|前端|后端|全栈)\b/)?.[0] || '创作者';

    const skillsText = profileData.skills.length > 0
      ? profileData.skills.join('、')
      : skillsDim?.text || '';

    const projectTitles = profileData.projects.length > 0
      ? profileData.projects
      : (projectDim?.text || '')
          .split(/[，、\n]/)
          .map((item: string) => item.trim())
          .filter(Boolean)
          .slice(0, 5);

    const awardTitles = profileData.achievements.length > 0
      ? profileData.achievements
      : (highlightDim?.text || '')
          .split(/[，。\n]/)
          .map((item: string) => item.trim())
          .filter(Boolean)
          .slice(0, 3);

    const bioParts = [
      skillsText,
      eduDim?.text || profileData.education.join('；'),
      highlightDim?.text || profileData.achievements.join('；'),
    ].filter(Boolean);

    const pageContent: Record<string, any> = {};

    pageContent['hero_featured'] = {
      title: nameVal,
      subtitle: [roleVal, profileData.company].filter(Boolean).join(' · '),
      featured_projects: projectTitles.slice(0, 5),
    };

    if (full_story || profileData.summary) {
      pageContent['story'] = {
        experiences: full_story || profileData.summary,
        challenges: insightDim?.text || profileData.values.join('、') || '',
        insights: potentialDim?.text || profileData.direction.join('、') || '',
      };
    }

    pageContent['about'] = {
      headline: nameVal,
      bio: bioParts.join('。'),
      photo: '',
    };

    if (skillsText) {
      const skillTags = skillsText
        .split(/[，、,\n]/)
        .map((s: string) => s.trim())
        .filter((s: string) => s.length > 0 && s.length < 20)
        .slice(0, 15);

      pageContent['skills'] = {
        categories: [
          { name: '专业技能', items: skillTags },
          { name: 'MBTI', items: mbti ? [mbti] : [] },
        ],
      };
    }

    if (awardTitles.length > 0) {
      pageContent['awards'] = {
        awards: awardTitles.map((title: string) => ({
          title,
          year: '',
          issuer: profileData.company || '',
        })),
      };
    }

    if (projectTitles.length > 0) {
      pageContent['projects'] = {
        projects: projectTitles.map((title: string) => ({
          title,
          year: '',
          role: roleVal,
          background: '',
          outcome: '',
          tags: profileData.skills.slice(0, 4),
          url: '',
        })),
      };
    }

    if (contact_email || social_links) {
      pageContent['contact'] = {
        email: contact_email || '',
        links: social_links || [],
      };
    }

    if (social_links && social_links.length > 0) {
      pageContent['social'] = { links: social_links };
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
        description: 'Generate a personal IP website from AI-analyzed dimensions',
        body: {
          dimensions: '[{ icon, label, score, text }]',
          short_story: 'string',
          full_story: 'string',
          mbti: 'string',
          style: 'design system name',
          name: 'optional — overrides extracted name',
          role: 'optional — overrides extracted role',
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