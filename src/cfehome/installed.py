DEFAULT_APPS = [
     # django-apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party-apps
    "allauth_ui",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'django_hosts',
    'slippers',
    "widget_tweaks",
]

# tenant/enterpise apps
_CUSTOMER_INSTALLED_APPS = DEFAULT_APPS + [
    # my-apps
    "commando",
    "profiles",
    "visits",
]
# reverse("tenants:list")

# public schema default installed apps
_INSTALLED_APPS = _CUSTOMER_INSTALLED_APPS + [
    # my-apps
    "commando",
    "customers",
    "profiles",
    "subscriptions",
    "tenants",
    "visits",
]

_INSTALLED_APPS = list(set(_INSTALLED_APPS))