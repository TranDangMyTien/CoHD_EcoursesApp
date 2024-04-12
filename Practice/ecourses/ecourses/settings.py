"""
Django settings for ecourses project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hn@ykr48=4+=z30)$sq4rqh&60=vx9r@=8+t-+yrfi^h+o&qvr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# Khai báo áp
INSTALLED_APPS = [
    # Phân hệ chuyên làm về admin
    'django.contrib.admin',
    # Chứng thực và phân quyền
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Hộ trợ các tập tin tĩnh (CSS, hình ảnh, âm thanh,...)
    'django.contrib.staticfiles',

    # Thêm app mới tạo (thêm hàm - để nữa muốn chỉnh sữa thì nó dễ hơn)
    # Lệnh make migrations
    'courses.apps.CoursesConfig',
    'ckeditor',
    'ckeditor_uploader',
    # Phần dùng cho Debug toolbar
    'debug_toolbar',
    # API
    'rest_framework',
    # Phần Swagger
    'drf_yasg',
    # Phần OAuth2
    'oauth2_provider',

]
# Phần dành cho Debug Toolbar
INTERNAL_IPS = [

    '127.0.0.1',

]

REST_FRAMEWORK = {
    # Phần phân trang
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE' : Số Item trên 1 trang
    'PAGE_SIZE': 2,

    # Phần OAuth2
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',)


}


# Security
# Tầng kiểm tra trước khi gửi thông tin từ client đến server
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Chỉ URL gốc, từ đây nó ánh xạ và tìm các URL
ROOT_URLCONF = 'ecourses.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecourses.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# db.sqlite3 tập tin độc lập
# Django có thể tương tác nhiều cơ sở dữ liệu cùng lúc
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # Tạo csdl mới tên là ecoursesdb
        'NAME': 'ecoursesdb',
        'USER': 'root',
        'PASSWORD': 'm1234567890',
        # Mặc định là Localhot
        'HOST': ''
    }
}
#Lấy cái mình tạo thay vì dùng của Django, liên quan đến User
AUTH_USER_MODEL = 'courses.User'

#Tạo phần nối chuỗi
MEDIA_ROOT = '%s/courses/static' % BASE_DIR
# Đường dẫn của ảnh = MEDIA_ROOT + upload_to (Nhớ cài thư viện Pillow)
CKEDITOR_UPLOAD_PATH = "ckeditor/images/"
# URL của CKEditor = MEDIA_ROOT + CKEDITOR_UPLOAD_PATH

import cloudinary

cloudinary.config(
    cloud_name="dvxzmwuat",
    api_key="814652831379359",
    api_secret="BzgebW7M-yEgHzKWgEf176-MK6I"

)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CLIENT_ID = "bIkJhTVro8DpVZtdkn0dyw4nKj5q4GBpl63m8Jrx"
CLIENT_SECRET = "y2IaJE9kwEF6FPzn8GDPwbKNaccXQutL2vwP2L7izuiVSxdK3oGuXiXKv19f3cX2j9U7LFTsxLcUWuVT5GqZm6Cdd9daBC1eOwmlHwIXHMWP1msxlGDLl65wT1BXHek1"
