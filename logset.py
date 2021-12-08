"""
logging 配置
"""

import logging.config
import os

standard_format = '%(asctime)s\t%(levelname)s\t%(threadName)s:%(thread)d\t' \
                  '%(filename)s:%(lineno)d\t%(message)s'

simple_format = '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s'
LOG_DIR = ''
LOG_NAME = 'alarm.log'
# 如果不存在定义的目录就创建一个
# if not os.path.isdir(LOG_DIR):
#     os.mkdir(LOG_DIR)

# log文件的全路径
logfile_path = os.path.join(LOG_DIR, LOG_NAME)
# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        }
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 打印到文件的日志，手机info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,
            'maxBytes': 1024 * 1024 * 5,  # 日志文件大小到5M是进行切割
            'backupCount': 5,  # 备份五次切割后的日志，超过的按时间顺序进行删除
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        'bar': {
            'handlers': ['default'],  # 目前先输出到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}


def load_my_logging_cfg():
    logging.config.dictConfig(LOGGING_DIC)
    logger = logging.getLogger('bar')
    return logger


