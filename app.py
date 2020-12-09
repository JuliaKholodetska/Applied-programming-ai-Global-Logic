from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# from flask_restful import Api
# from wsgiref.simple_server import make_server
# from app import app, db
from werkzeug.security import generate_password_hash

from models import *
from flask import request, jsonify, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='j27333', server='localhost', database='test')
db = SQLAlchemy(app)

engine = db.engine
Base = db.Model


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/v1/hello-world-28!')
def number_display():
    return 'Hello, World - 28', 200


@app.route('/user/', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    firstname = request.json.get('firstname', None)
    lastname = request.json.get('lastname', None)
    password = request.json.get('password', None)

    if username and password and firstname and lastname:
        new_user = User(userName=username, firstName=firstname, lastName=lastname, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(status='created'), 200
    else:
        return jsonify(status='Bad data'), 204


# @app.route('/user/<int:id>', methods=['POST'])
# def create_user(id):
#
#     username = request.json.get('username', None)
#     firstname = request.json.get('firstname', None)
#     lastname = request.json.get('lastname', None)
#     password = request.json.get('password', None)
#
#     if username and password and firstname and lastname :
#         new_user = User(iduser=id ,userName=username, firstName=firstname, lastName=lastname, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify(status='created'), 200
#     else:
#         return jsonify(status='Bad data'), 204


@app.route('/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def userId(id):
    user = User.query.filter_by(iduser=id).first()
    if user is None:
        return jsonify(status='not found user'), 404

    if request.method == 'GET':
        return jsonify(status='current User', name=user.userName, firstname=user.firstName, lastname=user.lastName), 200

    if request.method == 'PUT':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)

        if username and password and firstname and lastname:
            user.userName = username
            user.lastName = lastname
            user.firstName = firstname
            user.password = generate_password_hash(password)
            #  return 200
            db.session.commit()
            return jsonify(status='updated', name=user.userName, firstname=user.firstName, lastname=user.lastName), 202
        else:
            return jsonify(status='Bad data'), 204
    if request.method == 'DELETE':
        # db.session.delete(user)
        # db.session.commit()
        db.session.execute(f'''DELETE FROM user WHERE {id}=iduser; ''')
        return jsonify(status='deleted'), 201
    else:
        return jsonify('User not found'), 404
    # if request.method == 'DELETE':
    #     db.session.delete(user)
    #     db.session.commit()
    #     return jsonify(status='deleted', name=user.userName, firstname=user.firstName, lastname=user.lastName), 201


#
# @app.route('/user/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user = User.query.filter_by(iduser=id).first()
#     if request.method == 'DELETE':
#             # db.session.delete(user)
#             # db.session.commit()
#             db.session.execute(f'''DELETE FROM user WHERE {id}=iduser; ''')
#             return jsonify(status='deleted'), 201
#     else:
#         return jsonify('User not found'), 404

def login_user(username, password):  # noqa: E501
    """Logs user into the system
     # noqa: E501
    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str
    :rtype: str
    """
    return 'do some magic!'


def logout_user():  # noqa: E501
    """Logs out current logged in user session
     # noqa: E501
    :rtype: None
    """
    return 'do some magic!'


@app.route('/credit/', methods=['POST'])
def create_credit():
    startdate = request.json.get('startdate', None)
    finishdate = request.json.get('finishdate', None)
    sum = request.json.get('sum', None)
    percent = request.json.get('percent', None)
    status = request.json.get('status', None)
    bank = Bank.query.filter_by(name='Privat').first()
    bank_id = bank.idbank
    if bank.budget < sum:
        return jsonify({"can't get credit": "badget of bank is empty", "status": "Bad request"}), 400

    if startdate and finishdate and sum and percent and status:
        new_credit = Credit(startDate=startdate, finishDate=finishdate, sum=sum, percent=percent, status=status,
                            bankId=bank_id)
        db.session.add(new_credit)
        db.session.commit()
        result = {
            "data": {
                "startDate": startdate,
                "finishDate": finishdate,
                "sum": sum,
                "percent": percent,
                "status": status,
                "bank_name": bank.name
            },
            "status": "Created"
        }
        return jsonify(result), 201
    else:
        return jsonify(status='Bad data'), 204


@app.route('/credit/<int:id>', methods=['GET', 'PUT'])
def creditId(id):
    credit = Credit.query.filter_by(idcredit=id).first()
    if credit is None:
        return jsonify(status='not found Credit'), 404
    if request.method == 'GET':
        return jsonify(status='current Credit', startdate=credit.startDate, finishdate=credit.finishDate,
                       sum=credit.percent, status_of_credite=credit.status), 200

    if request.method == 'PUT':
        startdate = request.json.get('startdate', None)
        finishdate = request.json.get('finishdate', None)
        sum = request.json.get('sum', None)
        percent = request.json.get('percent', None)
        status = request.json.get('status', None)

        if startdate and finishdate and sum and percent and status:
            credit.startDate = startdate
            credit.finishDate = finishdate
            credit.sum = sum
            credit.percent = percent
            credit.status = status
            #   return 200
            db.session.commit()
            return jsonify(status='updated', startdate=credit.startDate, finishdate=credit.finishDate, sum=credit.sum,
                           percent=credit.percent, statusc=credit.status), 202
        else:
            return jsonify(status='Bad data'), 204


# with make_server('', 5000, app) as server:
# print("pracue yra")

# server.serve_forever()

# if __name__ == "__main__":
app.run(debug=True)
