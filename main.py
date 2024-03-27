from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    today = datetime.utcnow()
    return render_template("index.html",task_list=tasks,today=today)

@app.route("/add", methods=["POST"])
def add_task():
    name = request.form["name"]
    description = request.form["description"]
    due_date = datetime.strptime(request.form["due-date"], "%Y-%m-%d")
    new_task = Task(name=name,description=description,due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<int:id>")
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)