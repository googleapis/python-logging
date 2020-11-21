import time
import logging
from flask import Flask
import os

try:
    import google.cloud.logging
except ImportError:
    # import at runtime for GAE environments
    import pip
    import importlib
    import site
    pip.main(['install', '-e', './python-logging'])
    importlib.reload(site)
    import google.cloud.logging

app = Flask(__name__)

client = google.cloud.logging.Client()
client.setup_logging()

@app.route('/')
def print_messages():
    app.logger.debug('debug message')
    app.logger.info('info message')
    app.logger.warning('warning message')
    app.logger.error('error message')
    app.logger.critical('critical message')
    app.logger.critical({'message': 'object message'})
    logger = logging.getLogger()
    handler_str = f"handler types : {[h.__class__.__name__ for h in logger.handlers]}"
    app.logger.critical(handler_str)
    return handler_str

if __name__ == "__main__":
    port = os.getenv('PORT', 8080)

    app.run(debug=True, host='0.0.0.0', port=port)
