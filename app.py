from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'  # SQLite database
db = SQLAlchemy(app)

# Model for a to-do item
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)

# Home route to display the to-do list
@app.route('/')
@app.route('/')
def index():
    filter_by = request.args.get('filter', 'all')
    now = datetime.now()

    if filter_by == 'completed':
        todos = Todo.query.filter_by(completed=True).order_by(Todo.due_date).all()
    elif filter_by == 'pending':
        todos = Todo.query.filter_by(completed=False).order_by(Todo.due_date).all()
    else:
        todos = Todo.query.order_by(Todo.due_date).all()

    return render_template('index.html', todos=todos, now=now, filter_by=filter_by)


# Route to add a new to-do item
@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

# Route to delete a to-do item
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Route to edit a to-do item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todo.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():  # Ensure that we're in the app context
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
