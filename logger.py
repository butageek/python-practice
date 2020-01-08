import logging


# init log object
log = logging.getLogger()

# set format of displayed messages and logging level
# display date/time messages: '%(asctime)s'
# display level name: '%(levelname)s'
# display message: '%(message)s'
# logging levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
# the default level is 'WARNING'
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] - %(message)s', level='DEBUG')

# example output
log.debug('debug message')
log.info('info message')
log.warning('warning message')
log.error('error message')
log.critical('critical message')
