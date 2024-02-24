import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

# Discord Bot のトークン
DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")

# MYSQL の情報
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# ログファイルの設定
LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_Loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)-s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2": {
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file": {
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "a",
            'formatter': "verbose"
        },
        
    },
    "loggers": {
        "bot": {
            "handlers": ['console'],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            'handlers': ['console2', 'file'],
            "level": "INFO",
            "propagate": False
        },

    }
}

dictConfig(LOGGING_CONFIG)