// API Route: POST /api/analyze
// AI Analysis of resume text - returns 7 dimensions + narrative + MBTI

import { NextRequest, NextResponse } from 'next/server';
import { Anthropic } from '@anthropic-ai/sdk';

interface Dimension {
  icon: string;
  label: string;
  score: number;
  text: string;
}

interface AnalysisResult {
  dimensions: Dimension[];
  short_story: string;
  full_story: string;
  mbti: string;
}

const apiKey = process.env.ANTHROPIC_API_KEY;
const client = apiKey ? new Anthropic({ apiKey }) : null;

function createFallbackAnalysis(resumeText: string): AnalysisResult {
  const normalized = resumeText.replace(/\s+/g, ' ').trim();
  const sentences = normalized
    .split(/[。！？\n]+/)
    .map((s) => s.trim())
    .filter(Boolean);

  const contains = (keywords: string[]) => keywords.some((keyword) => normalized.includes(keyword));

  const roleSentence =
    sentences.find((sentence) => /(工程|产品|设计|运营|市场|研究|开发|管理|执行|写作|创意)/.test(sentence)) ||
    sentences[0] ||
    '这份简历呈现了候选人的核心专业能力。';
  const projectSentence =
    sentences.find((sentence) => /(项目|主导|负责|落地|上线|搭建|优化|交付|迭代)/.test(sentence)) ||
    '项目经验在简历中有明确体现。';
  const skillSentence =
    sentences.find((sentence) => /(技术|技能|Python|TypeScript|JavaScript|React|SQL|AI|数据|架构|系统|产品)/.test(sentence)) ||
    '核心技能可从简历内容中直接提炼。';
  const educationSentence =
    sentences.find((sentence) => /(大学|硕士|本科|博士|学校|学历|教育)/.test(sentence)) ||
    '教育背景清晰可见。';
  const achievementSentence =
    sentences.find((sentence) => /(奖|增长|提升|突破|覆盖|发布|完成|达成|入选)/.test(sentence)) ||
    '亮点表现出较强的执行力与成果导向。';

  const storyBase = [roleSentence, projectSentence, achievementSentence].join('；');
  const shortStory = storyBase.length > 60 ? `${storyBase.slice(0, 57)}…` : storyBase;
  const fullStory = storyBase.length > 140 ? `${storyBase.slice(0, 137)}…` : storyBase;

  const mbti = contains(['沟通', '客户', '市场', '运营', '销售', '产品'])
    ? 'ENFP'
    : contains(['数据', '架构', '系统', '工程', '技术', '算法', '分析'])
      ? 'INTJ'
      : contains(['设计', '创意', '体验', '用户', '视觉'])
        ? 'INFP'
        : contains(['管理', '执行', '领导', '目标', '结果', '运营'])
          ? 'ESTJ'
          : 'INTJ';

  const dimensions: Dimension[] = [
    {
      icon: '💼',
      label: '职业经历',
      score: 65 + Math.min(25, Math.floor(normalized.length / 1200)),
      text: roleSentence,
    },
    {
      icon: '🧠',
      label: '核心技能',
      score: 60 + Math.min(30, Math.floor((normalized.match(/(Python|TypeScript|JavaScript|React|SQL|AI|产品|数据|架构|系统|前端|后端)/g) || []).length * 6)),
      text: skillSentence,
    },
    {
      icon: '🎓',
      label: '教育背景',
      score: 55 + (educationSentence.includes('大学') || educationSentence.includes('本科') || educationSentence.includes('硕士') || educationSentence.includes('博士') ? 20 : 0),
      text: educationSentence,
    },
    {
      icon: '💡',
      label: '项目经验',
      score: 60 + Math.min(25, Math.floor((normalized.match(/(项目|主导|负责|落地|上线|优化|交付|迭代|搭建)/g) || []).length * 5)),
      text: projectSentence,
    },
    {
      icon: '🌟',
      label: '成就亮点',
      score: 55 + Math.min(25, Math.floor((normalized.match(/(奖|增长|提升|突破|覆盖|发布|完成|达成|入选)/g) || []).length * 7)),
      text: achievementSentence,
    },
    {
      icon: '🔍',
      label: '洞察与价值观',
      score: 58,
      text: contains(['用户', '价值', '成长', '原则', '诚信', '目标'])
        ? '简历中体现出明确的价值判断与可持续成长思维。'
        : '简历内容显示出较强的目标意识与自我驱动能力。',
    },
    {
      icon: '⚡',
      label: '潜力与方向',
      score: 57,
      text: contains(['产品', '运营', '市场', '增长'])
        ? '未来可在产品运营与增长方向继续深化。'
        : contains(['数据', '架构', '系统', '技术'])
          ? '未来可在技术架构与数据方向继续发力。'
          : '未来具备继续扩展认知边界与带来更多业务价值的空间。',
    },
  ];

  return {
    dimensions,
    short_story: shortStory,
    full_story: fullStory,
    mbti,
  };
}

export async function POST(request: NextRequest) {
  let resumeText = '';

  try {
    const { resume_text } = await request.json();
    resumeText = resume_text || '';

    if (!resumeText || resumeText.trim().length < 50) {
      return NextResponse.json(
        { error: 'Resume text is too short (minimum 50 characters)' },
        { status: 400 }
      );
    }

    const resumeLength = resumeText.length;
    if (resumeLength > 50000) {
      return NextResponse.json(
        { error: 'Resume text is too long (maximum 50,000 characters)' },
        { status: 400 }
      );
    }

    if (!client) {
      return NextResponse.json(createFallbackAnalysis(resumeText));
    }

    const message = await client.messages.parse({
      model: 'claude-opus-4-7',
      max_tokens: 4096,
      messages: [
        {
          role: 'user',
          content: `你是一位专业的人生传记作家。请分析以下简历文本，提取关键信息并生成人物叙事。

简历文本:
---
${resume_text}
---

请用JSON格式返回以下结构化分析结果:

{
  "dimensions": [
    {"icon": "💼", "label": "职业经历", "score": 0-100, "text": "一段话描述职业轨迹和成就"},
    {"icon": "🧠", "label": "核心技能", "score": 0-100, "text": "一段话描述专业技能和技术栈"},
    {"icon": "🎓", "label": "教育背景", "score": 0-100, "text": "一段话描述教育经历和学术背景"},
    {"icon": "💡", "label": "项目经验", "score": 0-100, "text": "一段话描述重要项目和成果"},
    {"icon": "🌟", "label": "成就亮点", "score": 0-100, "text": "一段话描述最具代表性的成就"},
    {"icon": "🔍", "label": "洞察与价值观", "score": 0-100, "text": "一段话推断人物的核心理念和工作风格"},
    {"icon": "⚡", "label": "潜力与方向", "score": 0-100, "text": "一段话描述未来发展空间和职业方向"}
  ],
  "short_story": "一段简短的自我介绍故事（50字以内，用于快速展示）",
  "full_story": "一段完整的人物故事（150字以内，第三人称视角，生动有画面感）",
  "mbti": "推测的MBTI类型，如INTJ、ENFP等"
}

请确保:
1. score分数要客观反映该维度的丰富程度(职业经历丰富的分数高)
2. text内容要具体，基于简历中的真实信息
3. full_story使用第三人称，有画面感和情感温度
4. mbti要基于简历中的行为模式推断`,
        },
      ],
      response_format: {
        type: 'json_schema',
        json_schema: {
          name: 'AnalysisResult',
          description: '简历分析结果，包含7个维度、故事和MBTI',
          required: ['dimensions', 'short_story', 'full_story', 'mbti'],
          schema: {
            type: 'object',
            properties: {
              dimensions: {
                type: 'array',
                description: '7个维度的分析',
                items: {
                  type: 'object',
                  properties: {
                    icon: { type: 'string' },
                    label: { type: 'string' },
                    score: { type: 'number' },
                    text: { type: 'string' },
                  },
                  required: ['icon', 'label', 'score', 'text'],
                },
              },
              short_story: {
                type: 'string',
                description: '简短自我介绍故事（50字以内）',
              },
              full_story: {
                type: 'string',
                description: '完整人物故事（150字以内）',
              },
              mbti: {
                type: 'string',
                description: '推测的MBTI类型',
              },
            },
            required: ['dimensions', 'short_story', 'full_story', 'mbti'],
          },
        },
      },
    });

    const result = message.content as unknown as AnalysisResult;

    return NextResponse.json(result);
  } catch (error: any) {
    console.error('Analysis error:', error);

    const status = Number(error?.status || 0);
    const fallbackEligible =
      !apiKey ||
      status === 401 ||
      status === 429 ||
      status >= 500 ||
      /network|timeout|api/i.test(String(error?.message || ''));

    if (fallbackEligible) {
      return NextResponse.json(createFallbackAnalysis(resumeText));
    }

    return NextResponse.json(
      { error: 'Analysis failed. Please try again.' },
      { status: 500 }
    );
  }
}