# Contributing to Product Research Agent

Thank you for your interest! 🎉

## Development Setup

1. Fork and clone with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/YOUR_USERNAME/product-research-agent.git
   cd product-research-agent
   ```

2. Install dependencies:
   ```bash
   ./setup.sh
   source venv/bin/activate
   ```

3. Create a branch:
   ```bash
   git checkout -b feature/my-feature
   ```

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

Examples:
```bash
git commit -m "feat: add eBay scraper tool"
git commit -m "fix: handle timeout in Alibaba scraper"
git commit -m "docs: update installation instructions"
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions small

## Pull Request Process

1. Ensure tests pass
2. Update documentation
3. Create PR with clear description
4. Request review

## Questions?

Open an issue on GitHub!
