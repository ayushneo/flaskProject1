from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ayush@0307@localhost:3306/Playground'
db=SQLAlchemy(app)

class Student(db.Model):
    s_roll = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30))
    s_class = db.Column(db.String(10))
    marks= db.Column(db.Integer)

    def __init__(self,name,s_class,marks):
        self.name=name
        self.s_class=s_class
        self.marks=marks

    def __repr__(self):
        return '<Roll %d>' %self.s_roll

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

db.create_all()

class StudentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Student
        sqla_session = db.session
    s_roll=fields.Number(dump_only=True)
    name= fields.String(required=True)
    s_class=fields.String(required=True)
    marks=fields.Number(required=True)

@app.route('/students',methods=['GET'])
def index():
    get_students = Student.query.all()
    students_schema=StudentSchema(many=True)
    students= students_schema.dump(get_students)
    return make_response(jsonify({"Students": students}))

@app.route('/students',methods=['POST'])
def create_student():
    data = request.get_json()
    student_schema=StudentSchema()
    students=student_schema.load(data)
    result = student_schema.dump(students.create()).data
    return make_response(jsonify({"students": result}),201)


if __name__ == "__main__":
    app.run(debug=True)


