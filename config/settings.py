from pathlib import Path
from datetime import timedelta
from decouple import config

# === Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# === Seguridad / Debug
SECRET_KEY = config("SECRET_KEY", default="dev-secret-key")
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Si sirves el front desde Vite en localhost:5173
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# === Usuario custom
AUTH_USER_MODEL = "auth_app.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# === Apps
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",

    # Terceros
    "rest_framework",
    "rest_framework_simplejwt",
    "django_celery_beat",
    "corsheaders",
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",
    "import_export",

    # Propias
    "auth_app",
    "core",
    "gyms",
    "subscriptions",
    "clients",
    "staff",
    "billing",
    "activities",
    "marketing",
    "scheduler",
    "dashboard",
    "reports",
    "products",
    "services",
    "bonuses",
    "plans",
    "saas",
    "saas_payments",
]

# === Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS para front externo
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# === Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# === Base de datos (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# === Password validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# === I18N
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# === Static & Media
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === DRF + JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    # Paginación DRF clásica -> {count, next, previous, results}
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),  # el front envía Authorization: Bearer <token>
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# === CORS (desarrollo)
CORS_ALLOW_ALL_ORIGINS = True
# Si prefieres cerrarlo en dev, comenta la línea anterior y usa:
# CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

# === Celery
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# === Stripe (claves y URLs de retorno)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="sk_test_xxx")
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", default="pk_test_xxx")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", default="whsec_xxx")

STRIPE_SUCCESS_URL = config(
    "STRIPE_SUCCESS_URL",
    default="http://localhost:5173/#/stripe/success?session_id={CHECKOUT_SESSION_ID}",
)
STRIPE_CANCEL_URL = config(
    "STRIPE_CANCEL_URL",
    default="http://localhost:5173/#/stripe/cancel",
)
STRIPE_PORTAL_RETURN_URL = config(
    "STRIPE_PORTAL_RETURN_URL",
    default="http://localhost:5173/#/",
)
