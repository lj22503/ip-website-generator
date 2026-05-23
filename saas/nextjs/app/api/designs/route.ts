// API Route: GET /api/designs
// Lists all available design systems (54 systems from registry)

import { NextResponse } from 'next/server';
import { DESIGN_SYSTEMS, getCategories } from '@/lib/design-systems';

export async function GET() {
  const categories = getCategories();

  return NextResponse.json({
    designs: DESIGN_SYSTEMS,
    total: DESIGN_SYSTEMS.length,
    categories: ['All', ...categories],
  });
}