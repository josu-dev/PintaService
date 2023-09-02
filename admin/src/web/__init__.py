from flask import Flask, render_template


def create_app(env='development', static_folder='../../static'):
    app = Flask(__name__, static_folder=static_folder)

    @app.get('/')
    def home():
        return render_template('home.html')
        
    @app.get('/about')
    def about():
        return render_template('about.html')
    
    @app.get('/contact')
    def contact():
        return render_template('contact.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code='404', error_message='Página no encontrada'), 404

    return app
