# controllers.py
from template_engine import render_template

def index(params):
    context = {
        'title': 'Home',
        'message': 'Welcome to our MVC Framework!',
        'items': ['Python', 'MVC', 'Web Development']
    }
    return render_template('index.html', context)

def about(params):
    context = {
        'title': 'About',
        'content': 'This is a simple about page.'
    }
    return render_template('about.html', context)
