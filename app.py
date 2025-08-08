from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel, get_locale
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración de Flask-Mail
load_dotenv()
app.config['MAIL_RECIPIENT'] = os.getenv('MAIL_RECIPIENT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

# Configuración de idiomas
app.config['BABEL_DEFAULT_LOCALE'] = 'ca'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ca', 'es', 'en']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

def select_locale():
    lang = request.args.get('lang')
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        return lang
    return app.config['BABEL_DEFAULT_LOCALE']

babel = Babel(app, locale_selector=select_locale)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellidos = request.form.get("apellidos")
        correo = request.form.get("correo")
        idioma = request.form.get("idioma")
        mensaje = request.form.get("mensaje")
        archivos = request.files.getlist("archivo")

        # Cuerpo del mensaje
        cuerpo = (
            f"Nom complet: {nombre} {apellidos}\n"
            f"Correu electrònic: {correo}\n"
            f"Idioma de resposta: {idioma}\n\n"
            f"Missatge:\n{mensaje}"
        )

        msg = Message(
            subject=f"Nou missatge a TranscripData de {nombre} {apellidos}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_RECIPIENT']],
            body=cuerpo
        )

        # Adjuntar arxius (si hi ha)
        for archivo in archivos:
            if archivo and archivo.filename:
                msg.attach(
                    filename=archivo.filename,
                    content_type=archivo.content_type,
                    data=archivo.read()
                )

        try:
            mail.send(msg)
            flash("Missatge enviat correctament ✅", "success")
            return redirect(url_for("contacto"))
        except Exception as e:
            flash(f"Error en enviar el missatge: {e}", "danger")
            return redirect(url_for("contacto"))

    return render_template("contacto.html")

if __name__ == "__main__":
    app.run(debug=True)