# Contributing to CodeRoot Bot

We love your input! We want to make contributing to CodeRoot Bot as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, track issues and feature requests, as well as accept pull requests.

### Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `go`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/air.git
cd air
git checkout go

# Install dependencies
go mod download

# Install development tools
go install honnef.co/go/tools/cmd/staticcheck@latest
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Set up environment
cp .env.go.example .env
# Edit .env with your test configuration
```

### Code Style

- Follow standard Go conventions and idioms
- Use `gofmt` to format your code
- Run `go vet` to catch common errors
- Use `golangci-lint` for comprehensive linting
- Add comments for exported functions and types
- Keep functions small and focused

### Testing

- Write unit tests for new functionality
- Ensure all tests pass: `go test ./...`
- Add integration tests for complex features
- Test with real Telegram bot tokens (in development environment only)

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add user authentication feature

- Implement JWT token validation
- Add middleware for protected routes
- Update user model with authentication fields

Fixes #123
```

## Issue Reporting

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/A4ever-ORG/air/issues).

### Bug Reports

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists
- Explain the use case and benefit
- Consider the scope - is this a core feature or plugin?
- Be prepared to contribute code if possible

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

## Architecture Guidelines

### Project Structure

```
internal/
├── app/          # Application layer - orchestration
├── config/       # Configuration management
├── database/     # Data access layer
├── handlers/     # Telegram handlers
├── models/       # Data models
├── services/     # Business logic
├── utils/        # Utilities and helpers
└── logger/       # Logging infrastructure
```

### Design Principles

1. **Separation of Concerns**: Each package has a single responsibility
2. **Dependency Injection**: Use interfaces and inject dependencies
3. **Error Handling**: Always handle errors explicitly
4. **Context Usage**: Use context.Context for cancellation and timeouts
5. **Resource Cleanup**: Always clean up resources (defer close())

### Database Guidelines

- Use repository pattern for data access
- Implement proper connection pooling
- Use transactions for multi-step operations
- Cache frequently accessed data in Redis
- Create proper indexes for performance

### API Guidelines

- Use RESTful principles for HTTP endpoints
- Implement proper error responses
- Add request/response logging
- Use middleware for cross-cutting concerns
- Document API endpoints

## Security Guidelines

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all input data
- Implement rate limiting
- Use HTTPS in production
- Regular security audits with `gosec`

## Performance Guidelines

- Profile code for performance bottlenecks
- Use connection pooling for databases
- Implement caching strategies
- Monitor memory usage
- Use goroutines appropriately
- Avoid blocking operations in handlers

## Documentation

- Update README.md for significant changes
- Document all exported functions
- Add examples in documentation
- Keep deployment guides updated
- Update API documentation

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Deploy to staging
7. Deploy to production

## Questions?

Don't hesitate to ask questions if anything is unclear:

- 📧 Email: dev@coderoot.ir
- 💬 Telegram: @CodeRootSupport
- 🐛 GitHub Issues: For bugs and features
- 💡 GitHub Discussions: For questions and ideas

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you for contributing to CodeRoot Bot! Your efforts help make this project better for everyone.

---

**Happy coding! 🚀**