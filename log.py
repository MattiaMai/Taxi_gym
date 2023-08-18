import logging
import sys
import board

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
        temp = configuration.get('logginglevel')
        lvl = LoggerFactory.diction[temp]
        logging.basicConfig(filename=logname, filemode='w', level=lvl, format="%(name)s;%(levelname)s;%(message)s")

    @staticmethod
    def shutdown():
        logging.shutdown()


class Loggable:
    def __init__(self, nname):
        self.name = nname
        self.logger = logging.getLogger(nname)
        self.env = Blackboard().get('enviro')

    def getname(self):
        return self.name

    def info(self, msg):
        self.internal(msg, self.logger.info)

    def warning(self, msg):
        self.internal(msg, self.logger.warning)

    def critical(self, msg):
        self.internal(msg, self.logger.critical)

    def debug(self, msg):
        self.internal(msg,self.logger.debug)

    def error(self, msg):
        self.internal(msg,self.logger.error)

    def internal(self,msg,func):
        tosend = str(self.env.now) + ';' + msg
        if not sys.is_finalizing():
            func(tosend)
