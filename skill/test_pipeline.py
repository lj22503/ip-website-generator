"""Pipeline test for ip-website-generator."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from rendering.renderer import render_html_template

demo = {
    'content': {
        'hero_story': {'headline': '把100个失败案例变成方法论的人', 'subtitle': '产品设计师 | 独立开发者'},
        'story': {
            'experiences': '2019年，我从字节离职。带着一个判断：未来的工作形态是「一人公司」。\n\n这3年，我做过50个项目。',
            'challenges': '最大的挑战不是做产品，而是和自己对抗。当副业收入开始超过主业，我开始怀疑自己是不是在逃避职场。',
            'insights': '我学到了一件事：失败不是成功之母，失败是成功之母——的前提是你愿意直视它。'
        },
        'skills': {
            'categories': [
                {'name': '设计工具', 'items': ['Figma', 'Sketch', 'Framer']},
                {'name': '专业能力', 'items': ['产品策略', '用户体验设计']},
                {'name': '技术栈', 'items': ['React', 'TypeScript', 'Python']}
            ]
        },
        'projects': {
            'projects': [
                {
                    'title': 'Z型人才规划器',
                    'year': '2024',
                    'role': '独立产品设计 + 开发',
                    'background': '发现很多人对自己的人生规划感到迷茫。',
                    'outcome': '上线6个月，付费用户超过3000人',
                    'tags': ['产品设计', '独立开发']
                },
                {
                    'title': '失败博物馆',
                    'year': '2023',
                    'role': '发起人与策展人',
                    'background': '互联网行业对失败讳莫如深。',
                    'outcome': '全网超过100万人参观',
                    'tags': ['内容IP', '策展']
                }
            ]
        },
        'about': {
            'headline': '专注产品体验设计的6年老鸟',
            'bio': '毕业于清华美院，曾在字节、腾讯担任产品设计师。过去6年，我主导过3个从0到1的产品。'
        }
    },
    'name': 'Hermes',
    'role': '产品设计师 & 独立开发者',
    'github': 'https://github.com/hermes',
    'email': 'hello@hermes.com'
}

out_dir = r'C:\Users\lj225\Hermes\workspace\projects\ip-website-generator\skill'
os.makedirs(out_dir, exist_ok=True)

# Test developerfolio
try:
    html = render_html_template('developerfolio', demo, output_path=os.path.join(out_dir, 'test_developerfolio.html'))
    print(f'developerfolio rendered: {len(html)} bytes')

    checks = [
        ('Hermes', 'name'),
        ('产品设计师', 'title'),
        ('把100个失败案例变成方法论的人', 'hero headline'),
        ('独立开发者', 'hero subtitle'),
        ('关于我', 'about section'),
        ('技能图谱', 'skills section'),
        ('项目作品', 'projects section'),
        ('我的故事', 'story section'),
        ('Z型人才规划器', 'project 1 title'),
        ('失败博物馆', 'project 2 title'),
        ('清华美院', 'about bio'),
        ('hello@hermes.com', 'email'),
        ('github.com/hermes', 'github link'),
    ]

    for check_str, label in checks:
        if check_str in html:
            print(f'  PASS: {label}')
        else:
            print(f'  FAIL: {label} -- MISSING "{check_str}"')

except Exception as e:
    import traceback
    traceback.print_exc()

# Test alfolio
try:
    html2 = render_html_template('alfolio', demo, output_path=os.path.join(out_dir, 'test_alfolio.html'))
    print(f'\nalfolio rendered: {len(html2)} bytes')
except Exception as e:
    import traceback
    traceback.print_exc()

# Test rahulbeniwal
try:
    html3 = render_html_template('rahulbeniwal', demo, output_path=os.path.join(out_dir, 'test_rahulbeniwal.html'))
    print(f'rahulbeniwal rendered: {len(html3)} bytes')
except Exception as e:
    import traceback
    traceback.print_exc()