import logging
import datetime
import sys



class ISO8601UTCTimeFormatter(logging.Formatter):
    converter = datetime.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        current_time = self.converter(record.created).astimezone(datetime.timezone.utc)
        if not datefmt:
            datefmt = "%Y%m%dT%H%M%S.%fZ"
        return current_time.strftime(datefmt)


class ExceptionTracebackSquasherFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formatException(self, ei):
        return ''


class StdOutErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.INFO


class DefaultFormatter(ISO8601UTCTimeFormatter):
    pass


def build_default_root_logger(name=None):
    log_format = "%(asctime)22s, %(levelno)s, %(name)s, %(message)s"
    formatter = DefaultFormatter(fmt=log_format)
    root_logger = logging.getLogger(name)
    root_logger.setLevel(7)
    console_stderr_handler = logging.StreamHandler(sys.stderr)
    console_stderr_handler.setFormatter(formatter)
    root_logger.addHandler(console_stderr_handler)
    return root_logger


def configure_logging(config):
    key = "log_level"
    if key in config:
        value = config[key].upper()
        if hasattr(logging, value):
            root_logger.setLevel(getattr(logging, value))
        else:
            root_logger.error(f"Config key '{key}' value invalid. {value}")


class Log:
    def __init__(self, parent_logger=None, *args, **kwargs):
        self.log = (parent_logger.getChild if parent_logger else logging.getLogger)(self.__class__.__name__)
        self.log.debug("Initializing.")

    @staticmethod
    def method(*args, **kwargs):
        def modify_verbosity(level=logging.DEBUG, log_return=False):
            def modify_fn(fn):
                def modified_fn(self, *args, **kwargs):
                    log_message = f"{fn.__name__}("
                    if args:
                        log_message += ', '.join(map(str, args))
                    if args and kwargs:
                        log_message += ", "
                    if kwargs:
                        log_message += ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                    log_message += ")"
                    self.log.log(level, log_message)
                    result = fn(self, *args, **kwargs)
                    if log_return:
                        log_message += f" => {result}"
                        self.log.log(level, log_message)

                    return result
                return modified_fn
            return modify_fn

        if args and callable(args[0]):
            return modify_verbosity()(args[0])
        elif args:
            return modify_verbosity(*args)
        elif kwargs:
            return modify_verbosity(**kwargs)
