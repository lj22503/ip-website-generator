# Personal IP Website Generator

Two-track monorepo for generating personal brand websites and portfolios with AI-driven narrative and 54 design systems.

## Quick Start

### Skill Track (Self-hosted)

```bash
cd skill
pip install -e .
python -m skill.core --demo
```

### SaaS Track (Web Platform)

```bash
cd saas
pip install -e .
python -m saas.main
# API available at http://localhost:8000
```

## Project Structure

```
ip-website-generator/
├── skill/          # Self-hosted AI skill
├── saas/           # Web SaaS platform
├── shared/         # Shared code
└── tests/          # Tests
```

## Features

- **54 Design Systems**: Linear, Notion, Stripe, Figma, Apple, and more
- **MBTI Narrative Engine**: Personality-driven storytelling
- **8-Knives Quality Evaluation**: Multi-dimensional content assessment
- **Two Products**: Portfolio sites and Personal Brand sites

## License

MIT
