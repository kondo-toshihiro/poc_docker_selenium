import logging
import logging.handlers
import os
from datetime import datetime

from src import env_variables as env


def get_logger(name: str) -> logging.Logger:
    # console_level = convert_to_int(env.CONSOLE_LOG_LEVEL)
    # file_level = convert_to_int(env.FILE_LOG_LEVEL)
    console_level = env.LOG_LEVEL

    file_level = logging.INFO
    log_level = console_level if console_level < file_level else file_level

    console_log_format = logging.Formatter(
        "%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s")
    file_log_format = logging.Formatter(
        "%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s")
    logger = logging.getLogger(name)

    # console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(console_level)
    stream_handler.setFormatter(console_log_format)
    logger.addHandler(stream_handler)

    # file -> levelはINFO固定
    if os.path.exists("./log") is False:
        os.mkdir('log')
    # Logのファイルローテーションでパーミッションエラーになっていたので、同一ファイルに書き続けるように修正
    # 時折、PCのサインインしなおしで起動されなおすので、問題ないはず
    # file_handler = logging.handlers.TimedRotatingFileHandler(
    #     filename='./log/{:%Y-%m-%d}.log'.format(datetime.now()),
    #     when='MIDNIGHT',
    #     backupCount=31,
    #     encoding='utf-8'
    # )
    file_handler = logging.FileHandler(
        './log/{:%Y-%m-%d}.log'.format(datetime.now()))
    file_handler.setLevel(file_level)
    file_handler.setFormatter(file_log_format)
    logger.addHandler(file_handler)

    logger.setLevel(log_level)
    logger.propagate = False
    return logger
