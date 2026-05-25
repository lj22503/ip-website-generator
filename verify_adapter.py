#!/usr/bin/env python3
import sys
sys.path.insert(0, 'C:/Users/lj225/Hermes/workspace/projects/ip-website-generator')

from skill.core import DEMO_PERSONAL_SITE
from skill.modules.data_adapter import to_developerfolio, to_alfolio, to_rahulbeniwal

# Test adapter output
print("=== Developerfolio adapter ===")
df = to_developerfolio(DEMO_PERSONAL_SITE)
keys = ["mbti", "soul_statement", "challenge_quote", "framework_items", "stats", "testimonials", "timeline", "resources"]
for k in keys:
    v = df.get(k)
    if v:
        print(f"  {k}: present (type={type(v).__name__})")
    else:
        print(f"  {k}: MISSING")

print("\n=== Alfolio adapter ===")
af = to_alfolio(DEMO_PERSONAL_SITE)
for k in keys:
    v = af.get(k)
    if v:
        print(f"  {k}: present")
    else:
        print(f"  {k}: MISSING")

print("\n=== Rahulbeniwal adapter ===")
rb = to_rahulbeniwal(DEMO_PERSONAL_SITE)
for k in keys:
    v = rb.get(k)
    if v:
        print(f"  {k}: present")
    else:
        print(f"  {k}: MISSING")