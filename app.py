from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)

# Configuración de idiomas
app.config['BABEL_DEFAULT_LOCALE'] = 'ca'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ca', 'es', 'en']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

def select_locale():
    lang = request.args.get('lang')
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        return lang
    return app.config['BABEL_DEFAULT_LOCALE']

babel = Babel(app, locale_selector=select_locale)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)