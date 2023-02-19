from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, TimeField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    map_link = StringField(label='Cafe Location Put the URL below', validators=[DataRequired(), URL()])
    opening_time = StringField(label="Opening Time", validators=[DataRequired()])
    closing_time = StringField(label="Closing Time", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating", default=("☕"), choices=[("☕"), ("☕☕"), ("☕☕☕"), ("☕☕☕☕"), ("☕☕☕☕☕")], validators=[DataRequired()])
    wifi_strength = SelectField(label="Wi-fi Strength", default=("❌"), choices=[("❌"),("💪"), ("💪💪"), ("💪💪💪"), ("💪💪💪💪"), ("💪💪💪💪💪")], validators=[DataRequired()])
    power_socket = SelectField(label="Power Socket Availability", default=("❌"), choices=[("❌"),("🔌"), ("🔌🔌"), ("🔌🔌🔌"), ("🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌")], validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html", bootstrap=bootstrap)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf-8", newline='') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.map_link.data},"
                           f"{form.opening_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_strength.data},"
                           f"{form.power_socket.data}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form, bootstrap=bootstrap)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, bootstrap=bootstrap)


if __name__ == '__main__':
    app.run(debug=True)
