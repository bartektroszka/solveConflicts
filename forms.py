from flask_wtf import FlaskForm
from wtforms import StringField

class TerminalCommunication(FlaskForm):
  # Here we will have a form to insert code to execute in terminal
  command = StringField('Command to execute')