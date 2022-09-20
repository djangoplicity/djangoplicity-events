from .settings import *

# ENVIRONMENT CONFIG
SITE_ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')
SHORT_NAME = 'Djangoplicity'
TMP_DIR = os.path.join(BASE_DIR, 'tmp')

# CUSTOM CONFIG DEFAULTS
SERVE_STATIC_MEDIA = True

# APPLICATION DEFINITION
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Manage multiple domains content
    'django.contrib.sites',
    # Redirect URLs
    'django.contrib.redirects',
]

DJANGOPLICITY_APPS = [
    # Djangoplicity is an app package itself containing main templates, statics, etc
    'djangoplicity',
    'djangoplicity.menus',
    'djangoplicity.pages',
    'djangoplicity.metadata',
    'djangoplicity.archives',
    'djangoplicity.archives.contrib.security',
    'djangoplicity.releases',
    'djangoplicity.adminhistory',
    'djangoplicity.media',
    'djangoplicity.celery',
    'djangoplicity.iframe',
    # Used to create images derivatives
    'djangoplicity.cutter',
    'djangoplicity.announcements',
    'djangoplicity.reports',
    'djangoplicity.actions',
    'djangoplicity.utils',
    'djangoplicity.events',
]

THIRD_PARTY_APPS = [
    'test_project',
    # WYSIWYG HTML Editor (Used for example in pages editing)
    'tinymce',
    # Utility for implementing a modified pre-order traversal tree in django, used in menu items
    # See: https://www.caktusgroup.com/blog/2016/01/04/modified-preorder-tree-traversal-django/
    'mptt',
    'pipeline',
    'debug_toolbar',
    'crispy_forms',
]

INSTALLED_APPS = DJANGO_APPS + DJANGOPLICITY_APPS + THIRD_PARTY_APPS

# SITES
SITE_ID=1

if USE_I18N:
    INSTALLED_APPS += [
        'djangoplicity.translation',
    ]

    MIDDLEWARE += [
        # Sets local for request based on URL prefix.
        'djangoplicity.translation.middleware.LocaleMiddleware',  # Request/Response
    ]


# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"


# JAVASCRIPT CUSTOM CONFIG
JQUERY_JS = "jquery/jquery-1.11.1.min.js"
JQUERY_UI_JS = "jquery-ui-1.12.1/jquery-ui.min.js"
JQUERY_UI_CSS = "jquery-ui-1.12.1/jquery-ui.min.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"


# Social Networks
SOCIAL_FACEBOOK_WALL = 'https://www.facebook.com/AndresLinaresBC?sk=wall'

# Environment configuration
GA_ID = "XX-XXXXXXX-X"


############
# REPORTS  #
############
REPORTS_DEFAULT_FORMATTER = 'html'
REPORT_REGISTER_FORMATTERS = True


USE_TZ = False

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
]

# ARCHIVES
ARCHIVE_IMPORT_ROOT = os.path.join(BASE_DIR, 'import')
ARCHIVE_ROOT = 'archives/'
IMAGES_ARCHIVE_ROOT = 'archives/images/'
VIDEOS_ARCHIVE_ROOT = 'archives/videos/'
RELEASE_ARCHIVE_ROOT = 'archives/releases/'

ARCHIVE_URL_QUERY_PREFIX = 'archive'
ARCHIVE_URL_DETAIL_PREFIX = ''
ARCHIVE_URL_FEED_PREFIX = 'feed'
ARCHIVE_URL_SEARCH_PREFIX = 'search'

ARCHIVE_AUTO_RESOURCE_DELETION = False
ENABLE_ADVANCED_SEARCH = True

ARCHIVES = (
    ('djangoplicity.media.models.Image', 'djangoplicity.media.options.ImageOptions'),
    ('djangoplicity.media.models.Video', 'djangoplicity.media.options.VideoOptions'),
    ('djangoplicity.media.models.VideoSubtitle', 'djangoplicity.media.options.VideoSubtitleOptions'),
    ('djangoplicity.media.models.ImageComparison', 'djangoplicity.media.options.ImageComparisonOptions'),
)

# Allows templates coverage
TEMPLATES[0]['OPTIONS']['debug'] = True


# PIPELINE
# We split the CSS into main and extras to load the more important first

PIPELINE = {
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
                'font-awesome/css/font-awesome.min.css',
                'sprites/sprites.css',
                'css/bootstrap.3.1.1.css',
                'css/noirlab.css',
                'css/app.css',
            ),
            'output_filename': 'css/main.css',
        },
        'extras': {
            'source_filenames': (
                'jquery-ui-1.12.1/jquery-ui.min.css',
                'slick-1.5.0/slick/slick.css',
                'justified/css/jquery.justified.css',
                'magnific-popup/magnific-popup.css',
            ),
            'output_filename': 'css/extras.css',
        },
    },
    'JAVASCRIPT': {
        'main': {
            'source_filenames': (
                'jquery/jquery-1.11.1.min.js',
                'jquery-ui-1.12.1/jquery-ui.min.js',
                'bootstrap/bootstrap-3.1.1-dist/js/bootstrap.min.js',
                'js/jquery.menu-aim.js',
                'slick-1.5.0/slick/slick.min.js',
                'djangoplicity/jwplayer/jwplayer.js',
                'djangoplicity/js/jquery.beforeafter-1.4.js',
                'js/masonry.pkgd.min.js',
                'justified/js/jquery.justified.min.js',
                'magnific-popup/jquery.magnific-popup.min.js',
                'djangoplicity/js/widgets.js',
                'djangoplicity/js/pages.js',
                'djangoplicity/js/djp-jwplayer.js',
                'js/picturefill.min.js',
                'js/enquire/enquire.min.js',
                'js/sorttable.js',
                'js/noirlab.js',
            ),
            'output_filename': 'js/main.js',
        },
        'ie8compat': {
            'source_filenames': (
                'js/ie8compat/matchMedia/matchMedia.js',
                'js/ie8compat/matchMedia/matchMedia.addListener.js',
            ),
            'output_filename': 'js/ie8compat.js',
        },
        'openseadragon': {
            'source_filenames': (
                'djangoplicity/openseadragon/openseadragon.min.js',
            ),
            'output_filename': 'js/openseadragon.js',
        },
    },
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'DISABLE_WRAPPER': True,
}

# CELERY
CELERY_IMPORTS = [
    "djangoplicity.archives.contrib.security.tasks",
    "djangoplicity.celery.tasks",
]
# Task result backend
CELERY_RESULT_BACKEND = "amqp"
CELERY_BROKER_URL = 'amqp://guest:guest@broker:5672/'
# Avoid infinite wait times and retries
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}
# AMQP backend settings - Required for flower to work as intended
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = 3600
# File to save revoked tasks across workers restart
CELERY_WORKER_STATE_DB = os.path.join(TMP_DIR, 'celery_states')
CELERY_BEAT_SCHEDULE_FILENAME = os.path.join(TMP_DIR, 'celerybeat_schedule')
