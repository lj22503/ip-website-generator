#!/usr/bin/env node
/**
 * Generate Flow Test Script
 * Tests the complete flow from resume upload to website generation
 */

const fs = require('fs');
const path = require('path');

// Test data
const testData = {
  dimensions: [
    { icon: '◎', label: '职业定位', score: 4.5, text: '资深前端工程师，专注于 React 和 Node.js 全栈开发' },
    { icon: '◈', label: '核心技能', score: 4.8, text: 'React, TypeScript, Node.js, Next.js, GraphQL' },
    { icon: '◉', label: '教育背景', score: 4.0, text: '计算机科学学士，北京大学，2015-2019' },
    { icon: '△', label: '项目成就', score: 4.7, text: '主导公司核心产品重构，性能提升 300%' },
    { icon: '◇', label: '行业洞察', score: 4.2, text: '关注 Web3 和 AI 技术在前端的应用' },
  ],
  short_story: '5 年前端经验，从创业公司到大厂，始终追求技术卓越',
  full_story: '我是一名热爱技术的前端工程师。毕业于北京大学计算机系，先后在两家创业公司和一家大厂工作。擅长 React 生态，主导过多个从 0 到 1 的项目。最近专注于性能优化和开发者体验提升，带领团队将核心产品加载速度提升了 3 倍。',
  mbti: 'INTJ',
  style: 'notion',
  profile: {
    name: '张三',
    role: '前端工程师',
    company: '某科技公司',
    skills: ['React', 'TypeScript', 'Node.js', 'Next.js', 'GraphQL'],
    education: ['北京大学 计算机科学 学士 2015-2019'],
    projects: ['核心产品重构', '开发者工具链建设', '性能优化专项'],
    achievements: ['性能提升 300%', '团队规模从 3 人扩展到 10 人', '获得公司技术创新奖'],
    values: ['技术卓越', '持续学习', '团队协作'],
    direction: ['技术管理', '架构师'],
    summary: '5 年前端经验，专注 React 全栈开发',
  },
};

console.log('🧪 Generate Flow Test');
console.log('=' .repeat(50));
console.log();

// Test 1: Validate test data
console.log('Test 1: 验证测试数据');
if (!testData.dimensions || testData.dimensions.length === 0) {
  console.error('❌ 维度数据为空');
  process.exit(1);
}
if (!testData.short_story && !testData.full_story) {
  console.error('❌ 故事内容为空');
  process.exit(1);
}
console.log('✅ 测试数据有效');
console.log();

// Test 2: Check API route exists
console.log('Test 2: 检查 API 路由');
const apiRoutePath = path.join(__dirname, 'app/api/generate/route.ts');
if (!fs.existsSync(apiRoutePath)) {
  console.error(`❌ API 路由文件不存在：${apiRoutePath}`);
  process.exit(1);
}
console.log('✅ API 路由文件存在');
console.log();

// Test 3: Check HTML renderer
console.log('Test 3: 检查 HTML 渲染器');
const rendererPath = path.join(__dirname, 'lib/html-renderer.ts');
if (!fs.existsSync(rendererPath)) {
  console.error(`❌ HTML 渲染器文件不存在：${rendererPath}`);
  process.exit(1);
}
console.log('✅ HTML 渲染器文件存在');
console.log();

// Test 4: Validate JSON structure
console.log('Test 4: 验证 JSON 结构');
const requiredFields = ['dimensions', 'short_story', 'full_story', 'mbti', 'style'];
const missingFields = requiredFields.filter(field => !testData[field]);
if (missingFields.length > 0) {
  console.error(`❌ 缺少必填字段：${missingFields.join(', ')}`);
  process.exit(1);
}
console.log('✅ JSON 结构完整');
console.log();

// Test 5: Check dimension scores
console.log('Test 5: 检查维度分数');
const invalidScores = testData.dimensions.filter(d => d.score < 0 || d.score > 5);
if (invalidScores.length > 0) {
  console.error(`❌ 维度分数超出范围 (0-5): ${invalidScores.map(d => d.label).join(', ')}`);
  process.exit(1);
}
console.log('✅ 维度分数有效');
console.log();

// Test 6: Check style validity
console.log('Test 6: 检查设计风格');
const validStyles = [
  'notion', 'linear.app', 'stripe', 'figma', 'apple', 'framer',
  'airbnb', 'spotify', 'vercel', 'claude', 'cohere', 'ollama',
];
if (!validStyles.includes(testData.style)) {
  console.warn(`⚠️  设计风格 "${testData.style}" 可能无效`);
  console.log(`   有效风格：${validStyles.slice(0, 6).join(', ')}...`);
} else {
  console.log('✅ 设计风格有效');
}
console.log();

// Summary
console.log('=' .repeat(50));
console.log('✅ 所有静态检查通过');
console.log();
console.log('下一步：');
console.log('1. 启动开发服务器：npm run dev');
console.log('2. 在浏览器中测试完整流程');
console.log('3. 或使用 Postman/curl 测试 API 端点');
console.log();
console.log('API 测试命令：');
console.log('curl -X POST http://localhost:3000/api/generate \\');
console.log('  -H "Content-Type: application/json" \\');
console.log('  -d \'', JSON.stringify(testData).substring(0, 100), '...\'');
