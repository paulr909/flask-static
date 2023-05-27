import datetime
from urllib.parse import urlparse, urlunparse

from decouple import config
from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    request,
    url_for,
    send_from_directory,
)
from flask_mail import Mail, Message
from waitress import serve

from forms import ContactForm

app = Flask(__name__)

settings = {
    "DEBUG": config("DEBUG", default=False, cast=bool),
    "SECRET_KEY": config("SECRET_KEY"),
    "WTF_CSRF_ENABLED": True,
    "MAIL_SERVER": "smtp.sendgrid.net",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": "apikey",
    "MAIL_PASSWORD": config("SENDGRID_API_KEY"),
    "RECAPTCHA_PUBLIC_KEY": config("RECAPTCHA_PUBLIC_KEY"),
    "RECAPTCHA_PRIVATE_KEY": config("RECAPTCHA_PRIVATE_KEY"),
}

app.config.update(settings)
mail = Mail(app)
current_year = datetime.date.today().year


@app.before_request
def redirect_www():
    """Redirect www requests to non www"""
    url_parts = urlparse(request.url)
    if url_parts.netloc == "www.your-domain.com":
        url_parts_list = list(url_parts)
        url_parts_list[1] = "your-domain.com"
        return redirect(urlunparse(url_parts_list), code=301)


@app.route("/")
def index():
    return render_template("index.html", title="Flask Static", year=current_year)


@app.route("/tech-used")
def tech():
    return render_template("tech.html", title="Technologies Used", year=current_year)


@app.route("/contact", methods=("GET", "POST"))
def contact():
    form = ContactForm()
    if request.method == "POST":
        if not form.validate():
            flash("All fields are required")
            return render_template(
                "contact.html", title="Contact Form", year=current_year, form=form
            )
        else:
            msg = Message(
                subject="Flask Static- Contact Form",
                sender="mail@your-domain.com",
                recipients=["your-email@mail.com"],
            )
            msg.body = """ 
From: %s 
Email: %s
Industry: %s 
Message: %s """ % (
                form.name.data,
                form.email.data,
                form.industry.data,
                form.message.data,
            )
            mail.send(msg)
            return redirect(url_for("contact"))
    elif request.method == "GET":
        return render_template(
            "contact.html", title="Contact Form", year=current_year, form=form
        )


@app.route("/interests")
def interests():
    return render_template("interests.html", title="Tech Interests", year=current_year)


@app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", title="Error 404 Page Not Found", year=current_year
        ),
        404,
    )


@app.errorhandler(403)
def page_forbidden(e):
    return (
        render_template("403.html", title="Error 403 Forbidden", year=current_year),
        403,
    )


@app.errorhandler(500)
def internal_server_error(e):
    return (
        render_template(
            "500.html", title="500 Internal Server Error", year=current_year
        ),
        500,
    )


@app.route("/sitemap.xml")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
