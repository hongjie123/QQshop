"""
Django settings for Qshop project.

Generated by 'django-admin startproject' using Django 2.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(6)6dyd@mk(6rc=)=u^2(5=zim#8192rp*175*7lcv7trgq@s+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'QUser',
    'Shop',
    'djcelery',
    'ckeditor',
    'ckeditor_uploader',
    'Buyer',
]

#中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Qshop.middleware.MiddleWareIp', #自己写的，功能是禁止127.0.0.1访问
]

# 缓存(自写)
# CACHES={      #内存缓存，使用本地的内存作为缓存
#     'default':{
#         'BACKEND':'django.core.cache.backends.locmem.LocMemCache', #缓存的类型
#         'LOCATION':'hello', #变量：缓存的名字，文件缓存：就是文件名，数据库缓存就是数据库的名字
#         'TIMEOUT':300, #缓存时间，默认300秒，如果为None，代表永不过期
#         'OPTIONS':{
#             'MAX_ENTRIES':300, #最大缓存个数，默认也是300个
#             'CULL_FREQUENCY':3 #到达最大缓存数之后，删除缓存的比例，默认是3
#         }
#     }
# }

# CACHES={      #文件缓存
#     'default':{
#         'BACKEND':'django.core.cache.backends.filebased.FileBasedCache', #缓存的类型
#         'LOCATION':os.path.join(BASE_DIR,"cache_file"), #变量：缓存的名字，文件缓存：就是文件名，数据库缓存就是数据库的名字
#         'TIMEOUT':300, #缓存时间，默认300秒，如果为None，代表永不过期
#         'OPTIONS':{
#             'MAX_ENTRIES':300, #最大缓存个数，默认也是300个
#             'CULL_FREQUENCY':3 #到达最大缓存数之后，删除缓存的比例，默认是3
#         }
#     }
# }
# CACHES={      #数据库缓存
#     'default':{
#         'BACKEND':'django.core.cache.backends.db.DatabaseCache', #缓存的类型
#         'LOCATION':'cache_table', #变量：缓存的名字，文件缓存：就是文件名，数据库缓存就是数据库的名字
#         'TIMEOUT':300, #缓存时间，默认300秒，如果为None，代表永不过期
#         'OPTIONS':{
#             'MAX_ENTRIES':300, #最大缓存个数，默认也是300个
#             'CULL_FREQUENCY':3 #到达最大缓存数之后，删除缓存的比例，默认是3
#         }
#     }
# }
CACHES={      #memcached服务器
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache', #缓存的类型
        'LOCATION':'127.0.0.1:11211', #变量：缓存的名字，文件缓存：就是文件名，数据库缓存就是数据库的名字
        'TIMEOUT':300, #缓存时间，默认300秒，如果为None，代表永不过期
        # 'OPTIONS':{
        #     'MAX_ENTRIES':300, #最大缓存个数，默认也是300个
        #     'CULL_FREQUENCY':3 #到达最大缓存数之后，删除缓存的比例，默认是3
        # }
    }
}

ROOT_URLCONF = 'Qshop.urls'

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
        #自定义模板语法之标签是用到
        # "libraries":{
        #     "get_four":"Buyer.templatetags.ourTag"
        #
        # }
        },
    },
]

WSGI_APPLICATION = 'Qshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "qshop",
#         'HOST': "10.10.101.42",
#         'PASSWORD': "123456",
#         'USER': "root"
#     },
#     'slave': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "qshop",
#         'HOST': "10.10.101.213",
#         'PASSWORD': "123456",
#         'USER': "root"
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"static")
]

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,"static")

# STATIC_ROOT=os.path.join(BASE_DIR,"static")

#自定义邮件设置
MAIL_USER="2276473611"
MAIL_SENDER="2276473611@qq.com"
MAIL_PASSWORD="syjzdoeyogwfdiae"
MAIL_SERVER="smtp.qq.com"
MAIL_PORT=465

#celery框架异步任务配置
import djcelery

djcelery.setup_loader()#初始化celery异步任务

BROKER_URL="redis://127.0.0.1:6379/1" #任务存放的redis容器地址
CELERY_IMPORTS=('CeleryTask.tasks') #具体存放celery任务的地方
CELERY_TIMEZONE='Asia/Shanghai' #celery定时任务使用的时区
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler' #celery的处理器


from celery.schedules import timedelta
content="远方爱你的人"
CELERYBEAT_SCHEDULE={
    u"测试任务1":{
        "task":"CeleryTask.tasks.add",
        "schedule":timedelta(seconds=1)
    },
    u"测试任务2":{
        "task":"CeleryTask.tasks.sendMail",
        "schedule":timedelta(seconds=10),
        "args":(content,"2276473611@qq.com")
    }
}


#ckeditor
CKEDITOR_UPLOAD_PATH="upload"
CKEDITOR_IMAGE_BACKEND="pillow"

#设置分页，每页显示2条数据
PAZE_SIZE=2