// API Route: POST /api/generate
// Generates a personal IP website using the full-featured html-renderer

import { NextRequest, NextResponse } from 'next/server';
import { renderPage } from '@/lib/html-renderer';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const {
      product = 'personal_site',
      design = 'notion',
      content,
      selected_modules = ['hero_featured', 'story', 'contact'],
    } = body;

    // Validate required fields
    if (!content) {
      return NextResponse.json(
        { error: 'Content is required' },
        { status: 400 }
      );
    }

    const { name, role, short_story } = content;

    if (!name || !role) {
      return NextResponse.json(
        { error: 'Missing required content fields: name and role are required' },
        { status: 400 }
      );
    }

    // Normalize content to what renderPage expects
    // Map from flat content structure to module-based structure
    const pageContent: Record<string, any> = {};

    // Hero module
    if (short_story || role) {
      pageContent['hero_featured'] = {
        title: name,
        subtitle: role,
        featured_projects: [],
      };
    }

    // Story module — short_story goes into the story section
    if (content.full_story || short_story) {
      pageContent['story'] = {
        experiences: content.full_story || short_story || '',
        challenges: '',
        insights: '',
      };
    }

    // About module
    if (content.bio) {
      pageContent['about'] = {
        headline: name,
        bio: content.bio,
        photo: content.photo || '',
      };
    }

    // Contact module
    if (content.contact) {
      pageContent['contact'] = {
        email: content.contact.email || '',
        links: [],
      };
    }

    // Awards module
    if (content.awards) {
      pageContent['awards'] = { awards: content.awards };
    }

    // Projects module
    if (content.projects) {
      pageContent['projects'] = { projects: content.projects };
    }

    // Social module
    if (content.social) {
      pageContent['social'] = { links: content.social };
    }

    // Newsletter module
    if (content.newsletter) {
      pageContent['newsletter'] = content.newsletter;
    }

    // Skills module
    if (content.skills) {
      pageContent['skills'] = { categories: content.skills };
    }

    // Blog module
    if (content.blog) {
      pageContent['blog'] = { posts: content.blog };
    }

    // Render the website HTML using the full-featured renderer
    const html = renderPage({
      designSystem: design,
      content: pageContent,
      selectedModules: selected_modules,
      productType: product,
    });

    // Generate a unique ID for this generation
    const id = `site-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    // In a real SaaS, this would save to storage and return a preview URL
    // For now, we return the HTML directly as base64
    const htmlBase64 = Buffer.from(html).toString('base64');

    return NextResponse.json({
      id,
      status: 'ready',
      html_url: `/api/preview/${id}`,
      preview_url: `/preview/${id}`,
      html_base64: htmlBase64,
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
        description: 'Generate a personal IP website',
        body: {
          product: 'portfolio | personal_site',
          design: 'design system name (e.g., notion, linear.app, stripe)',
          content: {
            name: 'Your name',
            role: 'Your title/role',
            full_story: 'Your full story (400-800 characters)',
            short_story: 'Short story for hero (150-300 characters)',
            bio: 'Brief bio (under 150 characters)',
            mbti: 'MBTI type (e.g., INFJ, ENFP)',
            highlights: '[{ year, title, description }]',
            contact: '{ email, wechat, link, github, twitter }',
          },
          selected_modules: ['hero', 'story', 'highlights', 'contact'],
        },
      },
    },
    designs: [
      'notion', 'linear.app', 'stripe', 'figma', 'apple', 'framer',
      'airbnb', 'spotify', 'vercel', 'claude'
    ],
    mbti_types: ['INFJ', 'INFP', 'ENFJ', 'ENFP', 'INTJ', 'ENTP', 'ESFP', 'ISFJ'],
  });
}
