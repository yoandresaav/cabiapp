LOGGING = {
	'version':1,
	'disable_existing_loggers': False,
	'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
		'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
	'formatters':{
		'large':{
			'format':'%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  '
		},
		'tiny':{
			'format':'%(asctime)s  %(message)s  '
		}
	},
	'handlers':{
		# Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
		'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
		'null': {
            'class': 'logging.NullHandler',
            'filters': ['require_debug_false'],
        },
		'errors_file':{
			'level':'ERROR',
		    'class': 'logging.FileHandler',
			'filename':'logs/ErrorLoggers.log',
			'formatter':'large',
		},
		'info_file':{
			'level':'INFO',
		    'class':'logging.handlers.TimedRotatingFileHandler',
			'when':'midnight',
			'interval':1,
			'filename':'logs/InfoLoggers.log',
			'formatter':'large',
		},
		'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/Project.log',
            'formatter': 'large'
        },
	},
	'loggers':{
		'error_logger':{
			'handlers':['console'],
			'propagate':False,
		},
		# Don't send invalid host error messages to ADMINS.
        # https://docs.djangoproject.com/en/dev/topics/logging/#django-security
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'admins': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
	},
}