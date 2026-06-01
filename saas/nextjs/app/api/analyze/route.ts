// API Route: POST /api/analyze
// AI Analysis of resume text - extracts 7 IP dimensions + narrative + MBTI
// Uses DeepSeek API, no fallback allowed

import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

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

interface AnalysisResult {
  dimensions: Dimension[];
  short_story: string;
  full_story: string;
  mbti: string;
}

const apiKey = process.env.DEEPSEEK_API_KEY;
if (!apiKey) {
  throw new Error('DEEPSEEK_API_KEY environment variable is not set');
}

const client = new OpenAI({ apiKey, baseURL: 'https://api.deepseek.com' });

export async function POST(request: NextRequest) {
  try {
    const { resume_text } = await request.json();
    const resumeText = resume_text || '';

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

    const completion = await client.chat.completions.create({
      model: 'deepseek-chat',
      messages: [
        {
          role: 'user',
          content: `你是一位专业的人生IP分析师。请从以下简历文本中提取人物的7个IP维度，生成人物叙事。

简历文本:
---
${resume_text}
---

请用JSON格式返回以下结构化分析结果:

{
  "dimensions": [
    {"icon": "✨", "label": "Soul", "score": 0-100, "text": "一段具体的话，基于简历说明此人的核心价值观、使命、热情、信念——如'他坚信XX，体现在XX'", "sub_labels": [{"title": "核心理念", "description": "一段具体的话", "outcome": "体现"}, {"title": "信念", "description": "一段具体的话", "outcome": "体现"}]},
    {"icon": "🔧", "label": "Framework", "score": 0-100, "text": "一段具体的话，基于简历说明此人的方法论、决策逻辑、学习方式、工作流", "sub_labels": [{"title": "方法论", "description": "一段具体的话", "outcome": ""}, {"title": "决策逻辑", "description": "一段具体的话", "outcome": ""}]},
    {"icon": "🛠️", "label": "Skills", "score": 0-100, "text": "一段具体的话，基于简历说明此人的硬技能、软技能、行业经验", "sub_labels": [{"title": "硬技能", "description": "一段具体的话", "tags": ["技能1", "技能2"]}, {"title": "软技能", "description": "一段具体的话", "tags": []}]},
    {"icon": "📂", "label": "Work", "score": 0-100, "text": "一段具体的话，基于简历说明此人的代表作、内容、知识体系、证书等可见成果", "sub_labels": [{"title": "项目名称", "description": "项目描述", "outcome": "项目成果", "tags": ["标签1"]}, {"title": "项目名称2", "description": "项目描述2", "outcome": "", "tags": []}]},
    {"icon": "📅", "label": "Timeline", "score": 0-100, "text": "一段具体的话，基于简历说明此人的经历、成长曲线与未来方向", "sub_labels": [{"title": "经历阶段", "description": "一段具体的话", "outcome": ""}, {"title": "成长曲线", "description": "一段具体的话", "outcome": ""}]},
    {"icon": "🔗", "label": "Resources", "score": 0-100, "text": "一段具体的话，基于简历说明此人的人脉资源、信息工具、影响力", "sub_labels": [{"title": "人脉资源", "description": "一段具体的话", "outcome": ""}, {"title": "信息工具", "description": "一段具体的话", "outcome": ""}]},
    {"icon": "🎨", "label": "Form", "score": 0-100, "text": "一段具体的话，基于简历说明此人的外在呈现、个人品牌关键词、他人评价", "sub_labels": [{"title": "品牌关键词", "description": "一段具体的话", "outcome": ""}, {"title": "他人评价", "description": "一段具体的话", "outcome": ""}]}
  ],
  "short_story": "一段简短的自我介绍故事（50字以内，用于快速展示，如'他是XX，基于XX的创作者'）",
  "full_story": "一段完整的人物故事（150字以内，第三人称视角，有画面感和情感温度）",
  "mbti": "推测的MBTI类型，如INTJ、ENFP等"
}

请确保:
1. 每个dimension的text都要具体且有信息量，基于简历中的真实信息，避免泛泛而谈
2. 7个维度必须完整返回，label严格为Soul/Framework/Skills/Work/Timeline/Resources/Form
3. 每个维度必须包含sub_labels数组，每个元素包含title（必填）、description（必填）、outcome（可选）、tags（可选数组）
4. Work维度的sub_labels代表具体项目或成果，title为项目名，description为项目描述，outcome为项目成果
5. short_story要简洁有力，full_story要有叙事感
6. mbti要基于简历中的行为模式推断
7. 直接返回JSON，不要有markdown代码块包裹`,
        },
      ],
      response_format: { type: 'json_object' },
    });

    const raw = completion.choices[0]?.message?.content || '';
    const result = JSON.parse(raw) as AnalysisResult;

    // Validate 7 dimensions with correct labels
    if (!result.dimensions || result.dimensions.length !== 7) {
      return NextResponse.json(
        { error: 'Invalid response: expected 7 dimensions' },
        { status: 500 }
      );
    }

    const expectedLabels = ['Soul', 'Framework', 'Skills', 'Work', 'Timeline', 'Resources', 'Form'];
    const hasAllLabels = expectedLabels.every((label) =>
      result.dimensions.some((d) => d.label === label)
    );
    if (!hasAllLabels) {
      return NextResponse.json(
        { error: 'Invalid response: missing required dimension labels' },
        { status: 500 }
      );
    }

    return NextResponse.json(result);
  } catch (error: unknown) {
    console.error('Analysis error:', error);
    const message = error instanceof Error ? error.message : String(error);
    return NextResponse.json(
      { error: `Analysis failed: ${message}` },
      { status: 500 }
    );
  }
}