# 🤝 Contributing Guide

Thank you for your interest in contributing to our Multi-Platform Security Suite! This guide will help you get started.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branch Strategy](#branch-strategy)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Platform-Specific Guidelines](#platform-specific-guidelines)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Go 1.21 or higher
- Git
- Platform-specific tools (see individual branch guides)

### Fork and Clone

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/awesome-project.git
   cd awesome-project
   ```

## 🛠️ Development Setup

### Environment Setup

1. **Install Go**: Download and install Go 1.21+ from [golang.org](https://golang.org)

2. **Install Dependencies**:
   ```bash
   go mod download
   ```

3. **Install Development Tools**:
   ```bash
   go install golang.org/x/lint/golint@latest
   go install golang.org/x/tools/cmd/goimports@latest
   go install golang.org/x/vuln/cmd/govulncheck@latest
   ```

### Platform-Specific Setup

#### **Liara Development**
```bash
git checkout go
# Follow Liara deployment guide for local development
```

#### **Kali Linux Development**
```bash
git checkout go-kali
# Install Kali Linux tools and dependencies
```

#### **Termux Development**
```bash
git checkout go-ter
# Install Termux and Android development tools
```

## 🌿 Branch Strategy

### Branch Naming Convention

- `main` - Main development branch
- `go` - Liara cloud deployment branch
- `go-kali` - Kali Linux security tools branch
- `go-ter` - Android/Termux mobile tools branch
- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/urgent-fix` - Critical fixes

### Workflow

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Changes**: Follow coding standards

3. **Test**: Run tests for all affected platforms

4. **Commit**: Use conventional commit messages

5. **Push**: Push to your fork

6. **Pull Request**: Create PR with detailed description

## 📝 Coding Standards

### Go Code Style

- Follow [Effective Go](https://golang.org/doc/effective_go.html)
- Use `gofmt` for formatting
- Use `golint` for linting
- Write clear, documented code

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

### Code Documentation

- Document all exported functions
- Include examples for complex functions
- Update README for new features
- Add inline comments for complex logic

## 🧪 Testing

### Running Tests

```bash
# All tests
go test ./...

# Platform-specific tests
go test -tags=liara ./...
go test -tags=kali ./...
go test -tags=termux ./...

# Performance tests
go test -tags=performance ./...

# Coverage
go test -cover ./...
```

### Test Guidelines

- Write tests for new features
- Maintain >80% code coverage
- Test platform-specific functionality
- Include integration tests
- Test error conditions

## 📤 Submitting Changes

### Pull Request Process

1. **Update Documentation**: Update relevant documentation
2. **Add Tests**: Include tests for new functionality
3. **Update CHANGELOG**: Document changes
4. **Create PR**: Use the PR template
5. **Review**: Address review comments
6. **Merge**: After approval

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Platform-specific considerations included
- [ ] No new warnings generated

## 🔧 Platform-Specific Guidelines

### Liara (go branch)

**Focus Areas**:
- Cloud optimization
- Monitoring and health checks
- Auto-scaling capabilities
- Production readiness

**Guidelines**:
- Optimize for cloud deployment
- Include comprehensive monitoring
- Ensure graceful shutdown
- Test with Liara CLI

### Kali Linux (go-kali branch)

**Focus Areas**:
- Security tools and penetration testing
- Network analysis capabilities
- Vulnerability assessment
- Real-time monitoring

**Guidelines**:
- Follow security best practices
- Include comprehensive logging
- Test with Kali Linux tools
- Ensure proper error handling

### Termux (go-ter branch)

**Focus Areas**:
- Mobile optimization
- Battery efficiency
- Touch-friendly interface
- Mobile security tools

**Guidelines**:
- Optimize for battery life
- Ensure touch-friendly UI
- Test on Android devices
- Consider mobile limitations

## 🐛 Bug Reports

### Before Submitting

1. Search existing issues
2. Test on latest version
3. Include platform details
4. Provide reproduction steps

### Bug Report Template

Use the GitHub issue template for bug reports, including:
- Platform and version information
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## 💡 Feature Requests

### Before Submitting

1. Check existing features
2. Consider platform impact
3. Provide use case
4. Include implementation suggestions

### Feature Request Template

Use the GitHub issue template for feature requests, including:
- Clear description
- Problem statement
- Proposed solution
- Platform considerations

## 📚 Documentation

### Contributing to Docs

- Keep documentation up-to-date
- Include code examples
- Add platform-specific notes
- Update installation guides

### Documentation Standards

- Use clear, concise language
- Include step-by-step instructions
- Add troubleshooting sections
- Maintain consistent formatting

## 🔒 Security

### Security Guidelines

- Report security issues privately
- Follow secure coding practices
- Validate all inputs
- Use secure defaults
- Keep dependencies updated

### Reporting Security Issues

Email security issues to: security@awesome-project.com

## 🎉 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor hall of fame
- GitHub contributors list

## 📞 Support

### Getting Help

- Check existing documentation
- Search existing issues
- Join community discussions
- Contact maintainers

### Communication Channels

- GitHub Issues
- GitHub Discussions
- Email: support@awesome-project.com

---

Thank you for contributing to our Multi-Platform Security Suite! 🚀