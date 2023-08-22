import logging
import sys


class LoggerFactory:
    diction = {
        'info': logging.INFO,
        'critical': logging.CRITICAL,
        'debug': logging.DEBUG,
        'error': logging.ERROR,
        'warning': logging.WARNING
    }

    @staticmethod
    def setup(configuration):
        temp = configuration.get('logging_level')
        logging_level = LoggerFactory.diction[temp]
        logging_filename = configuration.get('output_folder') + configuration.get('log_filename')
        logging.basicConfig(filename=logging_filename, filemode='a', level=logging_level, format="%(asctime)s;%("
                                                                                                 "levelname)s;%("
                                                                                                 "name)s;%(message)s")

    @staticmethod
    def shutdown():
        logging.shutdown()


def internal_logging(msg, func):
    if not sys.is_finalizing():
        func(msg)


class Loggable:
    def __init__(self, nname):
        self.name = nname
        self.logger = logging.getLogger(nname)

    def getname(self):
        return self.name

    def info(self, msg):
        internal_logging(msg, self.logger.info)

    def warning(self, msg):
        internal_logging(msg, self.logger.warning)

    def critical(self, msg):
        internal_logging(msg, self.logger.critical)

    def debug(self, msg):
        internal_logging(msg, self.logger.debug)

    def error(self, msg):
        internal_logging(msg, self.logger.error)
