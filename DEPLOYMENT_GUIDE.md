# Deployment Guide

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Cloudinary account (optional, for image storage)
- Gunicorn or similar WSGI server
- Nginx or Apache for reverse proxy

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/mwecau_ict.git
cd mwecau_ict
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy and configure the production environment file:

```bash
cp .env.prod .env
# Edit .env with your production settings
```

Required environment variables:
- `SECRET_KEY`: Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `DEBUG`: Set to `False`
- Database credentials
- Email credentials
- Cloudinary credentials (if using)

### 5. Run Migrations

```bash
python src/manage.py migrate
```

### 6. Create Superuser

```bash
python src/manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python src/manage.py collectstatic --noinput
```

### 8. Initialize Data

```bash
python src/manage.py init_data
```

## Server Deployment

### Using Gunicorn

#### Install Gunicorn

```bash
pip install gunicorn
```

#### Create Systemd Service

Create `/etc/systemd/system/mwecau_ict.service`:

```ini
[Unit]
Description=MWECAU ICT Club
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/username/mwecau_ict
Environment="PATH=/home/username/mwecau_ict/venv/bin"
ExecStart=/home/username/mwecau_ict/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl start mwecau_ict
sudo systemctl enable mwecau_ict
```

### Using Docker

#### Build Image

```bash
docker build -t mwecau_ict:latest .
```

#### Run Container

```bash
docker run -d \
    --name mwecau_ict \
    -p 8000:8000 \
    -e DEBUG=False \
    -e SECRET_KEY=your-secret-key \
    -v /data/mwecau_ict:/app/data \
    mwecau_ict:latest
```

#### Using Docker Compose

```bash
docker-compose up -d
```

## Nginx Configuration

Create `/etc/nginx/sites-available/mwecau_ict`:

```nginx
upstream mwecau_ict {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Static files
    location /static/ {
        alias /home/username/mwecau_ict/staticfiles/;
        expires 30d;
    }
    
    # Media files
    location /media/ {
        alias /home/username/mwecau_ict/media/;
        expires 7d;
    }
    
    # Application
    location / {
        proxy_pass http://mwecau_ict;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/mwecau_ict /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL Certificate (Let's Encrypt)

### Install Certbot

```bash
sudo apt-get install certbot python3-certbot-nginx
```

### Generate Certificate

```bash
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### Auto-renewal

Certbot automatically sets up auto-renewal. Check status:

```bash
sudo certbot renew --dry-run
```

## Database Backup

### Daily Backup

Create `/home/username/backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backups/mwecau_ict"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

pg_dump -U postgres mwecau_ict > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

Add to crontab:

```bash
0 2 * * * /home/username/backup_db.sh
```

## Monitoring

### Application Logs

```bash
sudo journalctl -u mwecau_ict -f
```

### Database Monitoring

```bash
sudo -u postgres psql
\du  # Show users and privileges
\l   # Show databases
```

### Disk Space

```bash
df -h
du -sh /home/username/mwecau_ict
```

## Performance Optimization

### Database Indexing

Indexes are already created. Check with:

```bash
python src/manage.py shell
>>> from django.db import connection
>>> connection.queries
```

### Caching

Redis is configured in settings. Install and start Redis:

```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

### Static Files

Use a CDN for static files:

```python
# In settings.py (production)
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

## Troubleshooting

### 500 Internal Server Error

Check logs:
```bash
sudo journalctl -u mwecau_ict -n 50
```

### Database Connection Issues

Verify credentials:
```bash
psql -U postgres -h localhost -d mwecau_ict
```

### Migration Issues

Reset database (development only):
```bash
python src/manage.py migrate accounts zero
python src/manage.py migrate
```

### Static Files Not Found

Recollect:
```bash
python src/manage.py collectstatic --clear --noinput
```

## Security Checklist

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is unique and secure
- [ ] SSL/TLS enabled
- [ ] Database credentials not in code
- [ ] Regular security updates
- [ ] CSRF protection enabled
- [ ] SQL injection protection
- [ ] XSS protection headers
- [ ] Rate limiting enabled
- [ ] Regular backups
- [ ] Admin interface protected
- [ ] Log monitoring enabled

## Maintenance

### Weekly Tasks
- Monitor application logs
- Check disk space
- Verify backups

### Monthly Tasks
- Update dependencies
- Review security logs
- Performance analysis

### Quarterly Tasks
- Security audit
- Load testing
- Disaster recovery test

## Support

For deployment issues, contact: devops@yourdomain.com
