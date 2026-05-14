// API Route: GET /api/designs
// Lists all available design systems

import { NextResponse } from 'next/server';
import { DESIGN_SPECS } from '@/lib/css-builder';

// Get all design systems
export async function GET() {
  const designs = Object.entries(DESIGN_SPECS).map(([key, spec]) => ({
    id: key,
    name: key.replace('.app', ' (App)').replace('_', ' ').toUpperCase(),
    category: getCategory(key),
    description: getDescription(key),
    preview: {
      bg: spec.colors?.bg || '#ffffff',
      text: spec.colors?.text_primary || '#000000',
      accent: spec.colors?.accent || '#0075de',
    },
    fonts: {
      primary: spec.fonts?.primary || 'Inter',
      mono: spec.fonts?.mono || 'JetBrains Mono',
    },
    popularity: getPopularity(key),
  }));

  // Sort by popularity
  designs.sort((a, b) => b.popularity - a.popularity);

  return NextResponse.json({
    designs,
    total: designs.length,
    categories: [
      'All',
      'AI & ML',
      'Developer Tools',
      'Design & Productivity',
      'Marketing & Landing',
      'Fintech',
      'Enterprise & Consumer',
      'Documentation & Knowledge',
    ],
  });
}

function getCategory(key: string): string {
  const categories: Record<string, string> = {
    'linear.app': 'Developer Tools',
    'vercel': 'Developer Tools',
    'notion': 'Design & Productivity',
    'figma': 'Design & Productivity',
    'framer': 'Design & Productivity',
    'stripe': 'Fintech',
    'apple': 'Enterprise & Consumer',
    'airbnb': 'Enterprise & Consumer',
    'spotify': 'Enterprise & Consumer',
    'claude': 'AI & ML',
  };
  return categories[key] || 'General';
}

function getDescription(key: string): string {
  const descriptions: Record<string, string> = {
    'linear.app': 'Ultra-minimal dark-mode, precise, purple accent',
    'vercel': 'Black and white precision, Geist font system',
    'notion': 'Warm minimalism, serif headings, soft surfaces',
    'figma': 'Vibrant multi-color, playful yet professional',
    'framer': 'Bold black and blue, motion-first, design-forward',
    'stripe': 'Signature purple gradients, weight-300 elegance',
    'apple': 'Premium white space, SF Pro, cinematic imagery',
    'airbnb': 'Warm coral accent, photography-driven, rounded UI',
    'spotify': 'Vibrant green on dark, bold type, album-art-driven',
    'claude': 'Warm terracotta accent, clean editorial layout',
  };
  return descriptions[key] || 'Clean and modern design';
}

function getPopularity(key: string): number {
  const popularity: Record<string, number> = {
    'linear.app': 95,
    'vercel': 90,
    'notion': 98,
    'figma': 92,
    'framer': 86,
    'stripe': 96,
    'apple': 99,
    'airbnb': 90,
    'spotify': 88,
    'claude': 85,
  };
  return popularity[key] || 70;
}
