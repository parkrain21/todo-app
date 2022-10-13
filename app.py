from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize flask object and database configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create tables inside the todo database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

# App routes
@app.route('/')
def index():
    todo_list = Todo.query.all()
    total_todo = len(todo_list)
    total_completed = Todo.query.filter_by(complete=True).count()
    return render_template('base.html', todo_list=todo_list, total_todo=total_todo, total_completed=total_completed)

@app.route('/about')
def about():
    return "About Page"


# ------- Implement CRUD operations ------- #
@app.route('/add', methods=["POST"])                    # See form object on the base.html file, the data submitted goes here
def add():
    title = request.form.get('title')                   # Fetches the submitted data upon clicking the button
    new_todo = Todo(title=title, complete=False)        # Add the data to the db
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))                   # Refresh the page, then render the <tr> as per index() route above.

@app.route('/update/<int:todo_id>')                    
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')                    
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)