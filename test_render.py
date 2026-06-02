import sys
sys.path.insert(0, 'C:/Users/lj225/Hermes/workspace/projects/ip-website-generator')

from skill.core import render_html_template, DEMO_PERSONAL_SITE
from skill.modules.data_adapter import to_developerfolio

print('=== TEST 1: developerfolio rendering ===')
try:
    result = render_html_template('developerfolio', 'notion', 'personal_site', 'hero_story')
    print(f'Result type: {type(result)}')
    print(f'Result length: {len(result) if result else 0}')
    if result:
        print(result[:1500])
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()

print('\n=== TEST 2: DEMO_PERSONAL_SITE keys ===')
try:
    print(list(DEMO_PERSONAL_SITE.keys()))
except Exception as e:
    print(f'ERROR: {e}')

print('\n=== TEST 3: to_developerfolio adapter ===')
try:
    adapted = to_developerfolio(DEMO_PERSONAL_SITE)
    print(f'Adapted keys: {list(adapted.keys())}')
    print(f'hero_subtitle: {adapted.get("hero_subtitle", "MISSING")}')
    print(f'hero_name: {adapted.get("hero_name", "MISSING")}')
    bio = str(adapted.get('about', {}).get('bio', ''))[:80]
    print(f'about.bio[:80]: {bio}')
    print(f'experience type: {type(adapted.get("experience"))}')
    print(f'experience value: {adapted.get("experience")}')
    print(f'mbti: {adapted.get("mbti", "MISSING")}')
    social = adapted.get('social', {})
    print(f'social keys: {list(social.keys()) if isinstance(social, dict) else "NOT A DICT"}')
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()