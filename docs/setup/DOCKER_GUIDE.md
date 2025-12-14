# Docker Configuration Guide

## Overview
This project is configured to run with Docker using PostgreSQL, Redis, Celery, and Gunicorn. The configuration supports both development and production environments.

## Files

### `.env.docker`
Environment configuration file for Docker containers. This file contains:
- Django settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- PostgreSQL connection details
- Email configuration (Gmail SMTP)
- Cloudinary configuration (optional)
- Security settings
- Celery & Redis configuration

### `docker-compose.yml`
Orchestrates 5 services:
1. **db** - PostgreSQL 15 database
2. **redis** - Redis cache/message broker
3. **web** - Django web application with Gunicorn
4. **celery** - Celery worker for async tasks
5. **celery_beat** - Celery scheduler for periodic tasks

### `Dockerfile`
Builds the Django application image:
- Python 3.10 slim base image
- Installs PostgreSQL client and Python dependencies
- Creates necessary directories
- Collects static files
- Runs Gunicorn with 4 workers

### `src/config/settings.py`
Updated to support both SQLite (development) and PostgreSQL (Docker):
- Detects `DB_ENGINE` or `DATABASE_URL` environment variable
- Automatically switches to PostgreSQL when in Docker
- Maintains backward compatibility with SQLite

## Quick Start

### Build and Run
```bash
cd /path/to/mwecau_ict

# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f web
```

### After First Run
```bash
# Apply migrations (if not auto-run)
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin
```

### Useful Commands
```bash
# Stop services
docker-compose down

# Remove volumes (reset database)
docker-compose down -v

# Rebuild after code changes
docker-compose build --no-cache

# Access web  shell
docker-compose exec web bash

# View postgres logs
docker-compose logs db

# Run management commands
docker-compose exec web python manage.py <command>

# Send test email
docker-compose exec web python manage.py test_email --check-config

# Send bulk emails
docker-compose exec web python manage.py send_bulk_email \
  --type=announcement \
  --target=all_members \
  --subject="Test Email"
```

## Services Details

### Database (PostgreSQL)
- **Host**: db
- **Port**: 5432 (exposed to localhost)
- **Database**: ictclub
- **User**: postgres
- **Password**: postgres
- **Healthcheck**: Enabled

### Redis
- **Host**: redis
- **Port**: 6379 (exposed to localhost)
- **Healthcheck**: Enabled

### Web (Django + Gunicorn)
- **Port**: 8000
- **Workers**: 4 (configurable in docker-compose.yml)
- **Command**: Runs migrations, initializes data, and starts Gunicorn
- **Healthcheck**: Enabled (HTTP health check)
- **Restart**: Unless stopped (automatic recovery)

### Celery Worker
- **Task**: Async task processing
- **Broker**: Redis
- **Restart**: Unless stopped

### Celery Beat
- **Task**: Periodic task scheduling
- **Broker**: Redis
- **Scheduler**: Database scheduler
- **Restart**: Unless stopped

## Network

All services are connected via `ictclub_network` bridge network, allowing communication between containers:
- Web → Database via `db:5432`
- Web/Celery → Redis via `redis:6379`

## Volumes

### Persistent Volumes
- `postgres_data`: PostgreSQL data persistence
- `static_files`: Collected static files
- `media_files`: User-uploaded files

### Bind Mounts
- `.:/app`: Project code (for development hot reload)

## Environment Variables

Key variables from `.env.docker`:

| Variable | Default | Purpose |
|----------|---------|---------|
| DEBUG | False | Django debug mode |
| SECRET_KEY | dev-key | Django secret key |
| DB_HOST | db | PostgreSQL host |
| DB_PORT | 5432 | PostgreSQL port |
| EMAIL_HOST_USER | mwecauictclub@gmail.com | Gmail sender |
| REDIS_URL | redis://redis:6379/0 | Redis connection |

## Troubleshooting

### Database connection refused
```bash
# Check if db service is healthy
docker-compose ps
# Ensure db healthcheck passes before web starts
docker-compose logs db
```

### Migrations not running
```bash
# Manually run migrations
docker-compose exec web python manage.py migrate
```

### Static files not loading
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --clear --noinput
```

### Celery not processing tasks
```bash
# Check celery logs
docker-compose logs celery

# Verify Redis connection
docker-compose exec redis redis-cli ping
```

### Port already in use
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change first 8000 to different port
```

## Security Notes

### Development
The `.env.docker` file contains development credentials. For production:
1. Change `DEBUG=False` (already set)
2. Use strong `SECRET_KEY`
3. Use environment-specific `.env.production`
4. Configure proper email credentials
5. Enable `SECURE_SSL_REDIRECT=True`
6. Set `SESSION_COOKIE_SECURE=True`
7. Set `CSRF_COOKIE_SECURE=True`

## Production Deployment

For production deployment:
1. Use managed database service (AWS RDS, Azure Database, etc.)
2. Use external Redis service
3. Configure proper email service
4. Set up SSL/TLS certificate
5. Update ALLOWED_HOSTS
6. Use strong SECRET_KEY
7. Set DEBUG=False
8. Configure static file serving (CDN or reverse proxy)
9. Set up proper logging and monitoring
10. Use health checks for auto-recovery

## Additional Resources

- Docker: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Gunicorn: https://gunicorn.org/
- Celery: https://docs.celeryproject.org/
