from flask import Flask,request,jsonify
from flask_marshmallow import Marshmallow
from marshmallow import schema,fields
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud_example.db'
db = SQLAlchemy(app)
ma=Marshmallow(app)

class Task(db.Model):
   id=db.Column(db.Integer(),primary_key=True)
   name=db.Column(db.String(200))
   age=db.Column(db.String(100))
   
   def __init__(self, name, age):
        self.name = name
        self.age = age
   
class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task

    id = ma.auto_field()
    name = ma.auto_field()
    age = ma.auto_field()


@app.route('/task',methods=['GET'])
def task_get():
    task=Task.query.all()
    task_shema=TaskSchema(many=True)
    return jsonify(task_shema.dump(task))

@app.route('/task/<int:id>',methods=['GET'])
def tasks_get(id):
    task=Task.query.all(id)
    if task:
        task_shema=TaskSchema()
        return jsonify(task_shema.dump(task))
    return jsonify({'message': 'Task not found'}), 404

@app.route('/task',methods=['post'])
def task_create():
    data=request.json
    new_task=Task(name=data['name'],age=data['age'])
    db.session.add(new_task)
    db.session.commit()
    task_shema=TaskSchema()
    return jsonify(task_shema.dump(new_task))

@app.route('/task/<int:id>',methods=['put'])
def task_update(id):
    task=Task.query.get(id)
    if task:
        data=request.json
        task.name=data['name']
        task.age=data['age']
        db.session.commit()
        task_shema=TaskSchema()
        return jsonify(task_shema.dump(task))
    return jsonify({'message': 'Task not found'}), 404


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)