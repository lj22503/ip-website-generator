// API Route: POST /api/analyze
// AI Analysis of resume text - returns 7 dimensions + narrative + MBTI

import { NextRequest, NextResponse } from 'next/server';
import { Anthropic } from '@anthropic-ai/sdk';

const client = new Anthropic();

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

export async function POST(request: NextRequest) {
  try {
    const { resume_text } = await request.json();

    if (!resume_text || resume_text.trim().length < 50) {
      return NextResponse.json(
        { error: 'Resume text is too short (minimum 50 characters)' },
        { status: 400 }
      );
    }

    const resumeLength = resume_text.length;
    if (resumeLength > 50000) {
      return NextResponse.json(
        { error: 'Resume text is too long (maximum 50,000 characters)' },
        { status: 400 }
      );
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

    if (error?.status === 429) {
      return NextResponse.json(
        { error: 'Rate limit exceeded. Please try again later.' },
        { status: 429 }
      );
    }

    if (error?.status === 401) {
      return NextResponse.json(
        { error: 'API key invalid or missing.' },
        { status: 401 }
      );
    }

    return NextResponse.json(
      { error: 'Analysis failed. Please try again.' },
      { status: 500 }
    );
  }
}