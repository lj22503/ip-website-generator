#!/usr/bin/env python3
import sys
sys.path.insert(0, 'C:/Users/lj225/Hermes/workspace/projects/ip-website-generator')

from skill.core import DEMO_PERSONAL_SITE
from skill.rendering.renderer import render_html_template

# Render the developerfolio HTML with lijing data
html = render_html_template('developerfolio', DEMO_PERSONAL_SITE, 'C:/Users/lj225/Hermes/workspace/projects/ip-website-generator/skill/examples/lijing_developerfolio.html')

print('Length:', len(html) if html else 0)
print('Success:', html is not None and len(html) > 1000)

# Also render alfolio and rahulbeniwal
html2 = render_html_template('alfolio', DEMO_PERSONAL_SITE, 'C:/Users/lj225/Hermes/workspace/projects/ip-website-generator/skill/examples/lijing_alfolio.html')
print('alfolio length:', len(html2) if html2 else 0)

html3 = render_html_template('rahulbeniwal', DEMO_PERSONAL_SITE, 'C:/Users/lj225/Hermes/workspace/projects/ip-website-generator/skill/examples/lijing_rahulbeniwal.html')
print('rahulbeniwal length:', len(html3) if html3 else 0)