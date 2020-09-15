from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), unique=True)

    def __int__(self, todo):
        self.todo = todo


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'todo')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

db.create_all()


@app.route('/todo', methods=['POST'])
def add_todo():
    todo = request.json['todo']
    new_todo = Todo(todo=todo)
    db.session.add(new_todo)
    db.session.commit()

    return product_schema.jsonify(new_todo)


@app.route('/todo', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = products_schema.dump(all_todos)
    return jsonify(result)


@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    return product_schema.jsonify(todo)


@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)

    get_data = request.json['todo']
    todo.todo = get_data

    db.session.commit()
    return product_schema.jsonify(todo)


@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return product_schema.jsonify(todo)


if __name__ == '__main__':
    app.run(debug=True)
