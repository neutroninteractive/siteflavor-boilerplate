
INSTALLED_APPS = (
    'siteflavor.boilerplate',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'common',
    'search',
    'offer',
    'compressor',
    # 'debug_toolbar',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'wagtailmenus',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)

WAGTAIL_SITE_NAME = 'Boilerplate'

ROOT_URLCONF = 'siteflavor.boilerplate.urls'

VERTICAL = 'education'

# Linkout Constants
EDDY_CLICKS_PRODUCT_ACTIVE = False
QUINSTREET_CLICKS_PRODUCT_ACTIVE = False
QUINSTREET_SMS_POPUP_ACTIVE = False
QUINSTREET_SMS_POPUP_OFFER = '287202'

PHONE_NUMBER = '(888) 555-5555'

PHONE_NUMBERS = {
    'organic': PHONE_NUMBER,
}

ADMIN_EMAIL_ADDRESS = 'admin@boilerplate.com'
