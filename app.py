from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel, get_locale
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime
from flask import render_template, session

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

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/recupera")
def recupera():
    return render_template("recupera.html")


_ = lambda s: s
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
	# Simulamos datos de usuario venidos de BDD
	user = {
		"name": "Hernan",
		"phone": "123456789",
		"address": "Carrer carrer",
		"email": "hernan@hernan.com",
		"email_verified": False,  # <-- controla el aviso
	}

	plan = {
		"name": "Premium",
		"pages_left": 43,
		"pages_quota": 500,
	}

	# Placeholders y textos de UI (centralizados)
	placeholders = {
		"name": _("Nom"),
		"phone": _("Telèfon"),
		"address": _("Adreça"),
		"email": _("Email"),
	}

	ui = {
		"title": _("El Meu Perfil"),
		"save_button": _("GUARDAR CANVIS"),
		"email_pending": _("Email pendent de verificació"),
		"change_password": _("Modifica la teva contrasenya"),
	}

	if request.method == 'POST':
		# aquí procesas y guardas
		# user.update({...})
		# flash(_("Canvis desats"), "success")
		pass

	return render_template(
		'perfil.html',
		user=user,
		plan=plan,
		placeholders=placeholders,
		ui=ui
	)

def fetch_user_history(user_id: int, limit: int = 20):
    """
    Devuelve la lista de movimientos para el historial del usuario.
    Estructura: [{date, name, url, sent, ok, warn}, ...]
    Sustituye el cuerpo por tu query real.
    """
    # -- EJEMPLO CON DATOS MOCK / CAMBIA POR TU BBDD --
    demo = [
        {"date": datetime(2025, 7, 24, 10, 9), "name": "page_186_right.pdf", "url": "#", "sent": 8, "ok": 8, "warn": 0},
        {"date": datetime(2025, 7, 24,  9, 40), "name": "page_185_right.pdf", "url": "#", "sent": 6, "ok": 5, "warn": 1},
        {"date": datetime(2025, 7, 24,  9, 35), "name": "page_184_right.pdf", "url": "#", "sent": 6, "ok": 4, "warn": 0},
        {"date": datetime(2025, 7, 24,  9, 28), "name": "page_183_right.pdf", "url": "#", "sent": 8, "ok": 4, "warn": 1},
        {"date": datetime(2025, 7, 24,  9, 10), "name": "page_182_right.pdf", "url": "#", "sent":10, "ok":10, "warn": 0},
        {"date": datetime(2025, 7, 24,  8, 55), "name": "page_181_right.pdf", "url": "#", "sent": 8, "ok": 8, "warn": 0},
        {"date": datetime(2025, 7, 24,  8, 42), "name": "page_180_right.pdf", "url": "#", "sent":12, "ok":12, "warn": 0},
    ][:limit]

    # Formatea la fecha como en el historial (dd/mm/YYYY HH:MM)
    formatted = []
    for r in demo:
        formatted.append({
            "date": r["date"].strftime("%d/%m/%Y %H:%M"),
            "name": r["name"],
            "url":  r["url"],
            "sent": r["sent"],
            "ok":   r["ok"],
            "warn": r["warn"],
        })
    return formatted


@app.route("/carga")
def carga():
    # Obtén el id de usuario (usa el método que tengas en tu app)
    user_id = session.get("user_id", 1)
    # user_id = current_user.id  # si usas flask-login

    history = fetch_user_history(user_id, limit=20)

    # Si además quieres pasar un flag para “Veure +”
    history_has_more = len(history) >= 20

    return render_template(
        "carga.html",
        history=history,
        history_has_more=history_has_more,
    )


# (opcional) también puedes dejar plan_view usando el mismo helper
@app.route("/plan")
def plan():
    user_id = session.get("user_id", 1)
    history = fetch_user_history(user_id, limit=20)

    plan = {
        "name": "Premium",
        "pages_used": 43,
        "pages_quota": 500,
        "renewal": "28/07/2025",
    }

    return render_template("plan.html", plan=plan, history=history)

@app.context_processor
def utility_processor():
    def url_for_lang(endpoint, **values):
        values.setdefault('lang', request.args.get('lang', 'es'))
        return url_for(endpoint, **values)
    return dict(url_for_lang=url_for_lang)


if __name__ == "__main__":
    app.run(debug=True)