from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facts.db'
db = SQLAlchemy(app)

class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    facts = Fact.query.all()
    return render_template('index.html', facts=facts)

@app.route('/add', methods=['GET', 'POST'])
def add_fact():
    if request.method == 'POST':
        new_fact = request.form['content']
        if new_fact:
            fact = Fact(content=new_fact)
            db.session.add(fact)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_fact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создает базу данных при первом запуске
    app.run(debug=True)