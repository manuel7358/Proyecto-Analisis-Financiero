# settings.py — listo para Render + Postgres (fallback a SQLite)
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# Seguridad / Entorno
# ------------------------
def env_bool(v, default=False):
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes")

# SECRET_KEY from env (produce una robusta en producción)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-por-defecto-no-usar-en-produccion')

# DEBUG desde env (por defecto False en prod)
DEBUG = env_bool(os.environ.get('DJANGO_DEBUG', 'False'))

# ALLOWED_HOSTS: puedes pasar DJANGO_ALLOWED_HOSTS como 'host1,host2'
# Añadimos por defecto dominios de Railway y localhost para evitar 500/403 comunes
DEFAULT_ALLOWED = '127.0.0.1,localhost,.up.railway.app,supportive-happiness.up.railway.app'
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', DEFAULT_ALLOWED).split(',') if h.strip()]

# CSRF_TRUSTED_ORIGINS: Django requiere esquema (https://) para orígenes confiables
# Puedes definir DJANGO_CSRF_TRUSTED_ORIGINS como 'https://a.com,https://b.com'
csrf_env = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS')
if csrf_env:
    CSRF_TRUSTED_ORIGINS = [s.strip() for s in csrf_env.split(',') if s.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://supportive-happiness.up.railway.app',
        # Si usas otro dominio custom añádelo aquí o usa la variable DJANGO_CSRF_TRUSTED_ORIGINS
    ]

# Si tu app está detrás de un proxy que termina TLS (como Railway), activa esta cabecera
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies seguras en producción
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# ------------------------
# Aplicaciones y middleware
# ------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tu app
    'appfinanciero',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'financiero.urls'

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'financiero.wsgi.application'

# ------------------------
# Base de datos
# ------------------------
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ------------------------
# Validadores de contraseña
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ------------------------
# Internacionalización / timezone
# ------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# ------------------------
# Archivos estáticos (static)
# ------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'                # collectstatic colocará aquí
STATICFILES_DIRS = [ BASE_DIR / 'static' ]            # desarrollo
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------------
# Otros
# ------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Seguridad recomendada
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Fin del archivo
