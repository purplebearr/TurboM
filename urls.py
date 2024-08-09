from url_patterns import url_patterns
import controllers

def get_controller(controller_name):
    return getattr(controllers, controller_name.split('.')[-1])
