import time
import logging

def main(request):
    # request is required for GCF
    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')
    logging.critical('critical message')
    logging.critical({'message': 'object message'})
    logger = logging.getLogger()
    handler_str = "handler types : {}".format(
        [{h.__class__.__name__: h.__doc__} for h in logger.handlers])
    logging.critical(handler_str)
    return handler_str

if __name__ == '__main__':
    while True:
        main(None)
        time.sleep(15)
