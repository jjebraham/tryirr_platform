import os
from pathlib import Path

# ─── BASE ────────────────────────────────────────────────────────────────────────        
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "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")

DEBUG = True

ALLOWED_HOSTS = [
    "poolexo.com",
    ".poolexo.com",
    "127.0.0.1",
    "localhost",
]

# ─── PROXY & CSRF TRUST ──────────────────────────────────────────────────────────        
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://poolexo.com",
    "https://www.poolexo.com",
    "https://exchange.poolexo.com",
]

# ─── INSTALLED APPS ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # your app
    "core",
]

AUTH_USER_MODEL = "core.CustomUser"
SITE_ID = 3

# ─── MIDDLEWARE ─────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tryirr_platform.urls"

# ─── TEMPLATES ──────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "core" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",   # required by allauth      
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tryirr_platform.wsgi.application"

# ─── DATABASE ───────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ─── PASSWORD VALIDATORS ─────────────────────────────────────────────────────────        
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── INTERNATIONALIZATION ────────────────────────────────────────────────────────        
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

# ─── STATIC & MEDIA ──────────────────────────────────────────────────────────────        
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL   = "/media/"
MEDIA_ROOT  = BASE_DIR / "media"

# ─── AUTH BACKENDS & allauth SETTINGS ──────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED        = True
ACCOUNT_EMAIL_VERIFICATION    = "optional"
ACCOUNT_LOGIN_ON_GET          = True
ACCOUNT_SIGNUP_FIELDS         = ["email", "password1", "password2"]

# ✱ namespaced redirects:
LOGIN_REDIRECT_URL  = "core:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE":       ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# ─── EMAIL (dev) ────────────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "Poolexo <noreply@poolexo.com>"

# Instructions displayed during the final KYC step.
DEPOSIT_INSTRUCTIONS = (
    "Please transfer the required guarantee deposit to our bank account and "
    "upload proof of payment below."
)

# ─── SENTRY ───────────────────────────────────────────────────────────────────
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk

        sentry_sdk.init(dsn=SENTRY_DSN)
    except ImportError:
        pass


