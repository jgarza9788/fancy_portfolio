


#basic stuff
import os
DIR = os.path.dirname(os.path.realpath(__file__))

# portfolio data
from util.portfolio import portfolio
p = portfolio()

# used to compare strings / search
from fuzzywuzzy import fuzz

# regex
import re

# flask and forms
from flask import Flask, make_response, render_template, request, url_for, redirect, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TelField, SubmitField
from wtforms.validators import DataRequired, Email


file = os.path.join(DIR,'util',"secret_key.txt")
sk = ""
with open(file, "r",encoding="utf-8") as f:
    sk = f.readlines()[0]


app = Flask(__name__)
app.secret_key = sk


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/theme", methods=["GET", "POST"])
def theme():
    theme = request.form["theme"]
    page =  request.form["page"]
    print(theme,page)
    res = make_response(redirect(url_for(page)))
    res.set_cookie("theme", theme)
    # print(res)
    # return "ok"
    return res


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html",portfolio_data=p.data,query="")

@app.route("/portfolio/")
def portfolio_blank():
    return redirect(url_for("portfolio"))

@app.route("/portfolio/<query>", methods=['GET', 'POST'])
def portfolio_query(query):

    print(query)

    if len(query) < 2:
        return redirect(url_for("portfolio"))

    query = query.lower()

    pl = []
    for i in p.data:
        if query in str(i).lower():
            pl.append(i)
        else:
            temp = re.sub(r'[^A-Za-z]+',',',str(i).lower())
            for w in re.split(',',temp):
                # print(w)
                if fuzz.ratio(query, w) > 85:
                    pl.append(i)
                    break;
    
    return render_template("portfolio.html",portfolio_data=pl,query=query)

@app.route("/resume")
def resume():
    return render_template("resume.html")


class ContactForm(FlaskForm):
    name = StringField('Name')
    email = StringField(label='Email', validators=[DataRequired(), Email() ])
    phone = TelField(label="Phone#", validators=[DataRequired() ])
    message = TextAreaField('Message')
    submit = SubmitField(label="Send")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    print(request.method)

    form = ContactForm()

    print(form.validate_on_submit())

    if form.validate_on_submit():

        from util import Config
        cd = Config.Config().data

        from email.message import EmailMessage
        import ssl
        import smtplib

        print(form.name.data)
        print(form.email.data)
        print(form.phone.data)
        print(form.message.data)

        em = EmailMessage()
        em['From'] = cd['email']
        em['To'] = 'JGarza9788@gmail.com'
        em['Subject'] = 'contact from website'
        body = """
            name: {name}
            email: {email}
            phone: {phone}
            message: {message}
                """.format(
                    name=form.name.data, 
                    email=form.email.data,
                    phone=form.phone.data,
                    message=form.message.data,
                    )
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(cd['email'],cd['password'])
            smtp.sendmail(
                em['From'], em['To'], em.as_string()
                )


    return render_template("contact.html",form=form)




if __name__ == "__main__":

#     # prep work
#     from util.github_scrapper import get_github
#     ggh = get_github(repo_link="https://github.com/stars/jgarza9788/lists/portfolio",visible=False)
#     ggh.scrape()
#     from util.portfolio import process_portfolio
#     process_portfolio()


    # app.run(debug=True, host= '192.168.1.130', port="8800")
    # app.run(debug=True)
    app.run(debug=True, host= '192.168.1.200', port="8880")