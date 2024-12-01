from flask import current_app

def log_debug_message(message):
    current_app.logger.debug(message)