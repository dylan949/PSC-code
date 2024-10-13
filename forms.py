from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class CustomerForm(FlaskForm):
    global_event = SelectField('Select Global Event', choices=[
        ("earthquake_china", "Massive earthquake affecting China's ports"),
        ("iran_israel_war", "Iran and Israel waging war, blocking the Red Sea"),
        ("panama_canal_block", "Panama Canal blocked due to drought"),
        ("malacca_strait_tension", "Increased tension in the Strait of Malacca")
    ], validators=[DataRequired()])

