# Deployment Guide 🚀

This guide provides instructions for deploying **College Connect** to a production environment.

## 1. Preparing the Environment

### Secure Your Settings
In `college_connect/settings.py`, ensure the following are configured for production:
- `DEBUG = False`
- `ALLOWED_HOSTS = ['yourdomain.com', 'localhost']`
- `SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')`

### Static Files
Run the following command to collect all static files (CSS/JS/Images) into a single production-ready directory:
```bash
python manage.py collectstatic
```

## 2. Shared Hosting / PythonAnywhere

1. **Upload Files:** Zip your project and upload it to the platform.
2. **Virtual Environment:** 
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 CC_env
   pip install -r requirements.txt
   ```
3. **Migarations:**
   ```bash
   python manage.py migrate
   ```
4. **WSGI Configuration:** Update the site's WSGI file to point to your `college_connect.wsgi` application.

## 3. Deployment via Heroku

1. **Procfile:** Create a file named `Procfile` (no extension) in the root:
   ```
   web: gunicorn college_connect.wsgi
   ```
2. **Push to GitHub/Heroku:** 
   ```bash
   git add .
   git commit -m "Deploying to production"
   git push heroku main
   ```

## 4. Manual Deployment (Linux/Nginx/Gunicorn)

1. **Setup Gunicorn:** Install gunicorn using pip and create a service file to keep it running.
2. **Nginx Proxy:** Configure Nginx to proxy requests from Port 80 to the Gunicorn socket.
3. **Database Migration:** If using MySQL/PostgreSQL, update `DATABASES` in `settings.py` before running `python manage.py migrate`.

> [!CAUTION]
> Always use environment variables for your `SECRET_KEY` and database credentials. Never hardcode them in the version you push to GitHub.
