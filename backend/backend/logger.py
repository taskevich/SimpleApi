import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler


def setup_logger(name: str, level: str, filepath: str = None, mode: str = 'a',
                 console: bool = True, day_rotating: bool = False) -> logging.Logger:
    """Настройка логгера.

    Аргументы:
        – name: имя логгера;
        – level: уровень вывода;
        Доступны: DEBUG, INFO, WARNING, ERROR, CRITICAL
        – filepath: имя файла для логгирования, не обязательно;
        – mode: режим открытия файла, без filepath и с rotating игнорируется;
        - console: добавлять ли обработчик для вывода в консоль;
        – day_rotating: флаг для использования TimedRotatingFileHandler
        с периодом логгирования один день - один файл вместо RotatingFileHandler,
        который создает новый файл при перезапуске. Без filepath игнорируется.

    Возвращаемое значение:
        – логгер.
    """
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-5s] %(message)s', '%d.%m.%Y %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.handlers = []

    if console:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if filepath:
        if day_rotating:
            handler = TimedRotatingFileHandler(filepath, when='midnight', backupCount=14, encoding='utf8')
        else:
            # handler = FileHandler(filepath, mode)
            handler = RotatingFileHandler(filepath, mode, backupCount=5, encoding='utf8')
            handler.doRollover()

        def my_namer(default_name: str):
            # This will be called when doing the log rotation
            # default_name is name.log.YYYY-MM-DD -> name.YYYY-MM-DD.log
            base_filename, ext, date = default_name.split(".")
            return f"{base_filename}.{date}.{ext}"

        handler.namer = my_namer
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger("[simpleapi-backend]", "INFO")
