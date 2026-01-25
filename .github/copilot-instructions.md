# GitHub Copilot Instructions

> **⚡ Token Efficiency Note**: This is a minimal pointer file (~500 tokens, auto-loaded by Copilot).
> For complete operational details, reference: `#file:AGENTS.md` (~2,500 tokens, loaded on-demand)
> For specialized knowledge, use: `#file:SKILLS/<skill-name>/SKILL.md` (loaded on-demand when needed)

## 🎯 Quick Context

**Project**: FastAPI REST API demonstrating modern Python async patterns
**Stack**: Python 3.13 • FastAPI • SQLAlchemy (async) • SQLite • Docker • pytest
**Pattern**: Routes → Services → Database (layered architecture)
**Philosophy**: Learning-focused PoC emphasizing async/await and type safety

## 📐 Core Conventions

- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Type Hints**: Mandatory throughout (enforced by mypy if enabled)
- **Async**: All I/O operations use `async`/`await`
- **Testing**: pytest with fixtures and async support
- **Formatting**: black (opinionated), flake8 (linting)

## 🏗️ Architecture at a Glance

```text
Route → Service → Database
  ↓         ↓
Cache    Session
```

- **Routes**: FastAPI endpoints with dependency injection
- **Services**: Async database operations via SQLAlchemy
- **Database**: SQLite with async support (`aiosqlite`)
- **Models**: Pydantic for validation, SQLAlchemy for ORM
- **Cache**: aiocache SimpleMemoryCache (TTL: 600s / 10 min)

## ✅ Copilot Should

- Generate idiomatic async FastAPI code with proper type hints
- Use SQLAlchemy async APIs (`select()`, `scalars()`, `session.commit()`)
- Follow dependency injection pattern with `Depends()`
- Write tests with pytest async fixtures
- Apply Pydantic models for request/response validation
- Use structured logging (avoid print statements)
- Implement proper HTTP status codes and responses

## 🚫 Copilot Should Avoid

- Synchronous database operations
- Mixing sync and async code
- Missing type hints on functions
- Using `print()` instead of logging
- Creating routes without caching consideration
- Ignoring Pydantic validation

## ⚡ Quick Commands

```bash
# Run with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 9000

# Test with coverage
pytest --cov=. --cov-report=term-missing

# Docker
docker compose up

# Swagger: http://localhost:9000/docs
```

## 📚 Need More Detail?

**For operational procedures**: Load `#file:AGENTS.md`
**For Docker expertise**: *(Planned)* `#file:SKILLS/docker-containerization/SKILL.md`
**For testing patterns**: *(Planned)* `#file:SKILLS/testing-patterns/SKILL.md`

---

💡 **Why this structure?** Copilot auto-loads this file on every chat (~500 tokens). Loading `AGENTS.md` or `SKILLS/` explicitly gives you deep context only when needed, saving 80% of your token budget!
