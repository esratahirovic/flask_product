# Flask Product 

"python -m venv venv" creates venv file  

"source venv/bin/activate" activates the virtual env

use CTRL+C for quit

---

on terminal: (use pip for Windows instead of pip3)

pip3 freeze > requirements.txt

pip3 install -r requirements.txt

---

export FLASK_APP=app (use the file name as app without ".py")

export FLASK_ENV=development

export FLASK_DEBUG=True (for activate the debug mood)

---

on python shell or flask shell we can create the table with following commands;

from app import db

db.create_all()

---

Note : we can also add items on terminal.

exit() for closing the shell


after completing all steps run "flask run" command on terminal.


