import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&qx#$qj*+^spuyr#r6var$smxy=+4@+=a6@n5lp3n!5_6wk&=t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'system',
    'log',
    'schedule',
    'job',
    'workflow',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            ],
        },
    },
]

WSGI_APPLICATION = 'setting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thomson',
        'USER': 'root',
        'PASSWORD': 'root',
        #'USER': 'thomson',
        #'PASSWORD': 'thomson@$@',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Session timeout (minute)
# AUTO_LOGOUT_DELAY = 1
AUTO_LOGOUT_DELAY = 1440

# Thomson config
HOTS_THOMSON={
    'thomson-hcm':
    {
        'user' : 'nguyennt9',
        'passwd' : '123456',
        'host'  :   '172.29.3.189',
        'url' : 'http://%s/services/Maltese' % ('172.29.3.189'),
    },
    'thomson-lab':
    {
        'user' : 'iptv_tool',
        'passwd' : '123456',
        'host'  : '172.17.5.110',
        'url' : 'http://%s/services/Maltese' % ('172.17.5.110'),
    }
}


# login redirect
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
