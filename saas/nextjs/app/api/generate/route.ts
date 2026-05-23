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

interface GenerateRequest {
  dimensions: Dimension[];
  short_story: string;
  full_story: string;
  mbti: string;
  style: string;
  name?: string;
  role?: string;
  contact_email?: string;
  social_links?: Array<{ platform: string; url: string }>;
}

export async function POST(request: NextRequest) {
  try {
    const body: GenerateRequest = await request.json();
    const { dimensions, short_story, full_story, mbti, style, name, role, contact_email, social_links } = body;

    if (!dimensions && !short_story && !full_story) {
      return NextResponse.json(
        { error: 'Missing content: dimensions or stories required' },
        { status: 400 }
      );
    }

    const design = style || 'notion';

    // Build name from first dimension text (职业经历) or use provided name
    const careerDim = dimensions?.find(d => d.label.includes('职业'));
    const nameFromText = name || short_story?.split(/[|\n]/)[0]?.trim() || careerDim?.text?.split(/[，。\n]/)[0]?.split(' ')[0] || '我';
    const nameVal = name || nameFromText;

    // Build role from career dimension
    const roleVal = role || (careerDim?.text?.match(/\b(工程师|经理|总监|创始人|设计师|产品|运营|市场|销售|研发|技术|前端|后端|全栈)\b/)?.[0]) || '创作者';

    // Build skills from core skills dimension
    const skillsDim = dimensions?.find(d => d.label.includes('技能') || d.label.includes('核心'));
    const skillsText = skillsDim?.text || '';

    // Build projects/highlights from project dimension
    const projectDim = dimensions?.find(d => d.label.includes('项目') || d.label.includes('成就'));

    // Build page modules content
    const pageContent: Record<string, any> = {};

    // Hero — use short_story or career intro
    pageContent['hero_featured'] = {
      title: nameVal,
      subtitle: roleVal,
      featured_projects: [],
    };

    // Story — use full_story
    if (full_story) {
      pageContent['story'] = {
        experiences: full_story,
        challenges: dimensions?.find(d => d.label.includes('洞察') || d.label.includes('特质'))?.text || '',
        insights: dimensions?.find(d => d.label.includes('潜力'))?.text || '',
      };
    }

    // About — derive from several dimensions
    const eduDim = dimensions?.find(d => d.label.includes('教育'));
    const highlightDim = dimensions?.find(d => d.label.includes('成就') || d.label.includes('亮点'));

    let bioParts: string[] = [];
    if (skillsDim?.text) bioParts.push(skillsDim.text);
    if (eduDim?.text) bioParts.push(eduDim.text);
    if (highlightDim?.text) bioParts.push(highlightDim.text);

    pageContent['about'] = {
      headline: nameVal,
      bio: bioParts.join('。'),
      photo: '',
    };

    // Skills — from skills dimension text
    if (skillsText) {
      const skillTags = skillsText
        .split(/[,，、\n]/)
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

    // Awards — from highlight dimension
    if (highlightDim?.text) {
      pageContent['awards'] = {
        awards: [
          { title: highlightDim.text.split(/[，。]/)[0], year: '', issuer: '' },
        ],
      };
    }

    // Projects — from project dimension
    if (projectDim?.text) {
      const projects = projectDim.text
        .split(/[,，、\n]/)
        .filter((s: string) => s.trim().length > 5)
        .slice(0, 5)
        .map((title: string) => ({
          title: title.trim(),
          year: '',
          role: roleVal,
          background: '',
          outcome: '',
          tags: [],
          url: '',
        }));

      if (projects.length > 0) {
        pageContent['projects'] = { projects };
      }
    }

    // Contact
    if (contact_email || social_links) {
      pageContent['contact'] = {
        email: contact_email || '',
        links: social_links || [],
      };
    }

    // Social
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