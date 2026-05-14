// Types for the SaaS website generator

export interface DesignSystem {
  name: string;
  site: string;
  category: string;
  description: string;
  tags: string[];
  mood: string;
  recommended_for: string[];
  font_primary: string;
  font_mono: string;
  color_scheme: string;
  bg_base: string;
  text_base: string;
  accent_color: string;
  popularity: number;
}

export interface MBTIStyle {
  name: string;
  description: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  text_color: string;
  bg_color: string;
  font_heading: string;
  font_body: string;
  layout: string;
  hero_align: string;
  card_style: string;
  spacing: string;
  decorative: string;
  animation: string;
  personality_traits: string[];
}

export interface Highlight {
  year?: string;
  title: string;
  description: string;
}

export interface Contact {
  email?: string;
  wechat?: string;
  link?: string;
  github?: string;
  twitter?: string;
  phone?: string;
}

export interface GenerateRequest {
  product: 'portfolio' | 'personal_site';
  design: string;
  content: {
    name: string;
    role: string;
    full_story: string;
    short_story: string;
    bio: string;
    mbti: string;
    highlights?: Highlight[];
    contact?: Contact;
  };
  selected_modules: string[];
  mbti_style?: string;
}

export interface GenerateResponse {
  id: string;
  status: 'ready' | 'generating' | 'error';
  html_url?: string;
  preview_url?: string;
  error?: string;
}

export interface DesignSpecs {
  fonts: {
    primary: string;
    mono: string;
    google_link: string;
  };
  colors: {
    bg: string;
    bg_secondary: string;
    surface: string;
    text_primary: string;
    text_secondary: string;
    text_tertiary: string;
    text_muted: string;
    accent: string;
    accent_hover: string;
    border: string;
    border_subtle?: string;
    border_primary?: string;
    success: string;
  };
  typography: {
    display_size: string;
    display_weight: string;
    display_letter_spacing: string;
    h1_size: string;
    h1_weight: string;
    h1_ls: string;
    h2_size: string;
    h3_size: string;
    body_size: string;
    body_lh: string;
    caption_size: string;
  };
  spacing: string;
  border_radius: string;
  radius_card: string;
  radius_large: string;
}
