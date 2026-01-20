# Contributing to COCUS MVP

Thank you for your interest in contributing to the COCUS MVP ML/LLM RAG System!

## 🚀 Quick Start for Contributors

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/COCUS-MVP_ML_LLM_RAG_System.git
cd COCUS-MVP_ML_LLM_RAG_System
```

### 2. Set Up Development Environment
```bash
./setup.sh
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes & Test
```bash
# Run tests
pytest tests/ -v

# Run linters
make lint

# Format code
make format
```

### 5. Commit & Push
```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
Go to GitHub and create a PR from your branch.

---

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints
- Write docstrings for all functions/classes
- Keep functions small and focused

### Testing
- Write tests for all new features
- Maintain >80% code coverage
- Run `pytest tests/ -v` before committing

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring

---

## 🧪 Testing Your Changes

```bash
# Run all tests
make test

# Run specific test file
pytest tests/unit/test_models.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 📚 Documentation

When adding features, update:
- README.md - If it affects usage
- QUICK_START.md - If it affects setup
- API documentation - Add docstrings

---

## 🐛 Reporting Bugs

Create an issue with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)

---

## 💡 Feature Requests

Create an issue with:
- Clear description
- Use case
- Proposed solution (optional)

---

## ✅ Pull Request Checklist

Before submitting:
- [ ] Tests pass (`make test`)
- [ ] Linters pass (`make lint`)
- [ ] Code is formatted (`make format`)
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] PR description explains changes

---

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

---

Thank you for contributing! 🎉
