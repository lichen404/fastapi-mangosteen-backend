# FastAPI Mangosteen Backend - AI Coding Guide

## Project Overview
This is a personal accounting backend inspired by "山竹记账" (Mangosteen Accounting), built with FastAPI + Tortoise ORM + SQLite. It's a Chinese-language project with mixed Chinese/English code and documentation.

## Architecture & Key Patterns

### Project Structure
- **`api/`**: API layer with versioned endpoints (`v1/`)
- **`models/`**: Tortoise ORM models (User, Item, Tag)
- **`schemas/`**: Pydantic response models using `pydantic_model_creator`
- **`core/`**: Configuration, security, dependencies, Redis integration
- **`migrations/`**: Aerich database migrations

### Authentication Flow
- **Email-based authentication** with verification codes (no passwords)
- Redis stores verification codes (5min expiry): `redis.set(email, code, ex=300)`
- JWT tokens contain `user_id` payload, validated in `core/deps.py:get_current_user()`
- Authorization header format: `Authorization: Bearer <token>`

### Database Patterns
- **Tortoise ORM** with SQLite (`watch.sqlite`)
- Models use `fields.ForeignKeyField` and `fields.ManyToManyField`
- Pydantic schemas auto-generated: `User_Pydantic = pydantic_model_creator(User)`
- Queries use `prefetch_related()` for relationships: `Item.filter().prefetch_related('tags')`

### Rate Limiting & Security
- **SlowAPI** middleware for rate limiting: `@limiter.limit("1/minute")`
- Custom error handlers in `api/__init__.py` return Chinese error messages
- Environment-based config in `core/config.py` with `.env` support

## Key Development Workflows

### Local Development
```bash
poetry install                    # Install dependencies
poetry run python main.py        # Start dev server with auto-reload
```

### Database Management
```bash
aerich init -t settings.TORTOISE_ORM    # Initialize migrations
aerich init-db                          # Create initial migration
aerich migrate                          # Generate migrations
aerich upgrade                          # Apply migrations
```

### Docker Deployment
```bash
docker-compose up -d              # Production deployment
# Requires .env with SECRET_KEY and MAIL_PASSWORD
```

## Domain-Specific Conventions

### Financial Data Modeling
- **Items** have `amount` (float), `kind` enum (`income`/`expenses`), and `happen_at` timestamps
- **Many-to-many** relationship between Items and Tags via `tags` field
- Date queries use `happen_at__lt` and `happen_at__gt` with 366-day limit validation
- Balance calculations: expenses subtract, income adds to balance

### API Response Format
- Lists return `{"pager": {...}, "resources": [...]}` structure
- User endpoints return `{"resource": data}` format
- Error responses use `{"error": "message"}` in Chinese

### Redis Integration
- Production uses Docker service name: `redis://my-redis-container`
- Development uses localhost: `redis://localhost`
- Environment detection: `os.getenv("ENVIRONMENT", "development")`

### Email System
- **FastMail** integration with QQ SMTP
- 6-digit verification codes using `random.choices(string.digits, k=6)`
- Background tasks for email sending: `BackgroundTasks` parameter

## Critical Files for Understanding
- `api/__init__.py`: App setup, middleware, error handling
- `core/deps.py`: JWT authentication dependency injection
- `settings.py`: Tortoise ORM configuration
- `api/v1/endpoints/item.py`: Core business logic with financial calculations
- `core/redis.py`: Environment-aware Redis connection logic

## Development Notes
- **Mixed language**: Chinese comments, English code, Chinese API documentation
- **No password authentication**: Email + verification code only
- **Financial precision**: Use `round(amount, 2)` for currency calculations
- **Date handling**: Always validate date ranges don't exceed 1 year
- **Dependency injection**: Heavily used for user auth and Redis connections