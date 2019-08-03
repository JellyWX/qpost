from flask import flash

class Grade():
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    DANGER = 'danger'
    WARNING = 'warning'
    INFO = 'info'
    LIGHT = 'light'
    DARK = 'dark'

class Alert():

    def __init__(self, text: str, grade: str=Grade.PRIMARY):
        self.text: str = text

        self.grade: str = grade

    def __repr__(self):
        return '''<div class="alert alert-{}">{}</div>'''.format(self.grade, self.text)

def Primary(text):
    flash(Alert(text, grade=Grade.PRIMARY))

def Secondary(text):
    flash(Alert(text, grade=Grade.SECONDARY))

def Success(text):
    flash(Alert(text, grade=Grade.SUCCESS))

def Danger(text):
    flash(Alert(text, grade=Grade.DANGER))

def Warning(text):
    flash(Alert(text, grade=Grade.WARNING))

def Info(text):
    flash(Alert(text, grade=Grade.INFO))

def Light(text):
    flash(Alert(text, grade=Grade.LIGHT))

def Dark(text):
    flash(Alert(text, grade=Grade.DARK))
