LOGGING = {
	'version':1,
	'disable_existing_loggers': False,
	'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
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
	'':{
		'error_logger':{
			'handlers':['console', 'errors_file', 'info_file', 'proj_log_file'],
			'level':'DEBUG',
			'propagate':True,
		}
	},
}