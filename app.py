from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import *
from flask import request, jsonify, json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


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


auth = HTTPBasicAuth()
with app.app_context():
    Users = User.query.all()
    res = dict()
    for i in range(len(Users)):
        res[Users[i].Username] = generate_password_hash(Users[i].Password)
    #users = json(res)
# users = {
#     "john": generate_password_hash("hello"),
#     "susan": generate_password_hash("bye")
# }


@auth.verify_password
def verify_password(username, password):
    if username in res and check_password_hash(res.get(username), password):
        return username


@auth.get_user_roles
def get_user_roles(username):
    user = User.query.filter_by(Username=username).first()
    return user.get_roles()
# @app.route('/')
# def main_page():
#     return "Hello, World!"
#
#
# @app.route('/api/v1/hello-world-13')
# def option():
#     return "Hello, World 13!"


@app.route('/user/', methods=['POST'])
def create_user():
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')
    userStatus = request.json.get('userStatus', 'student')

    user = User.query.filter_by(Username=username).first()
    users = User.query.all()

    if user and user.Username == username:
        return jsonify(status='Current user is already exists'), 400
    if username and password and firstname and lastname and email and phone and userStatus:
        crd_user = User(UserID=len(users) + 1, Username=username, FirstName=firstname, LastName=lastname, Email=email,
                        Password=password, Phone=phone, UserStatus=userStatus)
        db.session.add(crd_user)
        db.session.commit()
        res[username]=generate_password_hash(password)
        return jsonify(status='created', id=crd_user.UserID, username=crd_user.Username, firstName=firstname, lastName=lastname,
                        email=email, password=crd_user.Password, phone=phone, userSatus=userStatus), 201
    else:
        return jsonify(status='Bad data'), 400


@app.route('/user/<username>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required(role='student')
def userId(username):
    logged_user = auth.current_user()
    if logged_user != username:
        return jsonify(status='Access denied'), 403
    user = User.query.filter_by(Username=username).first()

    if user is None:
        return jsonify(status='User not found'), 404

    if request.method == 'GET':
        return jsonify(status='current User', id=user.UserID, username=user.Username, firstName=user.FirstName, lastName=user.LastName,
                        email=user.Email, password=user.Password, phone=user.Phone, userSatus=user.UserStatus), 200

    if request.method == 'PUT':
        username = request.json.get('username')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')

        if username or password or firstname or lastname or email or phone:
            if username:
                user.Username = username
            if lastname:
                user.LastName = lastname
            if firstname:
                user.FirstName = firstname
            if email:
                user.Email = email
            if password:
                user.Password = password
            if phone:
                user.Phone = phone
            db.session.query(User).filter_by(UserID=user.UserID).update(
                dict(Username=user.Username, FirstName=user.FirstName, LastName=user.LastName,
                        Email=user.Email, Password=user.Password, Phone=user.Phone))
            db.session.commit()
            result = {
                "data": {
                    "id": user.UserID,
                    "username": user.Username,
                    "firstName": user.FirstName,
                    "lastName": user.LastName,
                    "email": user.Email,
                    "password": user.Password,
                    "phone": user.Phone,
                    "userStatus": user.UserStatus
                },
                "status": "Updated"
            }
            return jsonify(result), 201
        else:
            return jsonify(status='Bad request'), 400

    if request.method == 'DELETE':
        # db.session.delete(user)
        courses = UserCourses.query.filter(UserCourses.username == username).all()
        for course in courses:
            current_db_session1 = db.session.object_session(course)
            current_db_session1.delete(course)
            current_db_session1.commit()
        current_db_session2 = db.session.object_session(user)
        current_db_session2.delete(user)
        current_db_session2.commit()
        return jsonify(status='deleted'), 200


@app.route('/user/<username>/courses/', methods=['GET'])
@auth.login_required(role='student')
def userCourses(username):
    logged_user = auth.current_user()
    if logged_user != username:
        return jsonify(status='Access denied'), 403
    courses = UserCourses.query.filter(UserCourses.username == username).all()
    user = User.query.filter_by(Username=username).first()
    res = dict()
    for i in range(len(courses)):
        if courses[i].requestStatus == 'approved':
            res[i + 1] = courses[i].Courses_names
    if len(courses):
        return jsonify(res), 200
    elif user:
        return jsonify(status="This user haven't applied for any course yet"), 200
    else:
        return jsonify('User not found'), 404


@app.route('/user/<username>/apply/<course_name>/', methods=['POST'])
@auth.login_required(role='student')
def apply_for_course(username, course_name):
    logged_user = auth.current_user()
    if logged_user != username:
        return jsonify(status='Access denied'), 403
    userc = UserCourses.query.filter((UserCourses.username == username) & (UserCourses.Courses_names == course_name)).first()
    user = User.query.filter_by(Username=username).first()
    course = Course.query.filter_by(Name=course_name).first()
    users_of_current_crs = UserCourses.query.filter(UserCourses.Courses_names == course_name).all()
    num_of_rows = UserCourses.query.all()
    if not user:
        return jsonify(status="This user have not even created"), 404
    if not course:
        return jsonify(status="Course not found"), 404
    if userc:
        return jsonify(status="This user have already applied for this course"), 403
    else:
        afc = UserCourses(ID=len(num_of_rows) + 1, username=username, Courses_names=course_name, requestStatus="waiting")
        db.session.add(afc)
        db.session.commit()
        return jsonify(status="request sent", id=afc.ID, username=afc.username,
                       course_name=afc.Courses_names, requestStatus=afc.requestStatus), 200


@app.route('/course/', methods=['POST'])
@auth.login_required(role='teacher')
def create_course():
    category = request.json.get('category')
    name = request.json.get('name')
    course_head_username = request.json.get('course_head_username')

    course = Course.query.filter_by(Name=name).first()
    courses = Course.query.all()
    user = User.query.filter_by(Username=course_head_username).first()

    if course and course.Name == name:
        return jsonify(status='Current course is already exists'), 400
    if not user:
        return jsonify(status="This user have not even created"), 404
    if category and name and course_head_username:
        crd_course = Course(ID=len(courses) + 1, Category=category, Name=name, CourseHeadUsername=course_head_username)
        db.session.add(crd_course)
        db.session.commit()
        return jsonify(status='created', id=crd_course.ID, category=category, name=name, courseHeadUsername=course_head_username), 201
    else:
        return jsonify(status='Bad data'), 400


@app.route('/courses/', methods=['GET'])
@auth.login_required(role='teacher')
def create_all_courses():
    courses = Course.query.all()
    courses_list = []
    for cor in courses:
        courses_list.append(Course.get_course(cor))
    if len(courses_list) == 0:
        return jsonify(status='No courses found')
    else:
        return jsonify([i for i in courses_list]), 200


@app.route('/course/<course_name>/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required(role='teacher')
def update_course(course_name):
    find_course = Course.query.filter_by(Name=course_name).first()
    if not find_course:
        return jsonify(status="Course not found"), 404

    if request.method == 'GET':
        return jsonify(status='current User', id=find_course.ID, category=find_course.Category, name=find_course.Name,
                           courseHeadUsername=find_course.CourseHeadUsername), 200

    if request.method == 'PUT':
        category = request.json.get('category')
        name = request.json.get('name')
        course_head_username = request.json.get('course_head_username')

        course = Course.query.filter_by(Name=name).first()
        user = User.query.filter_by(Username=course_head_username).first()
        if course and course.Name == name:
            return jsonify(status='Current course is already exists'), 400
        if not user:
            return jsonify(status="This user have not even created"), 404
        if category or name or course_head_username:
            if category:
                find_course.Category = category
            if name:
                find_course.Name = name
            if course_head_username:
                find_course.CourseHeadUsername = course_head_username
            db.session.query(Course).filter_by(ID=find_course.ID).update(
                dict(Category=find_course.Category, Name=find_course.Name,
                     CourseHeadUsername=find_course.CourseHeadUsername))
            db.session.commit()
            return jsonify(status='updated', id=find_course.ID, category=find_course.Category, name=find_course.Name,
                           courseHeadUsername=find_course.CourseHeadUsername), 201
        else:
            return jsonify(status='Bad data'), 400

    if request.method == 'DELETE':
        current_db_sessions = db.session.object_session(find_course)
        current_db_sessions.delete(find_course)
        current_db_sessions.commit()
        return jsonify(status='deleted'), 200


@app.route('/course/<username>/<course_name>/', methods=['PUT'])
@auth.login_required(role='teacher')
def val_requests(username, course_name):
    cur_request = UserCourses.query.filter((UserCourses.username == username) & (UserCourses.Courses_names == course_name)).first()
    requests = UserCourses.query.filter(UserCourses.Courses_names == course_name).all()
    if not cur_request:
        return jsonify(status="Request not found"), 404

    request_status = request.json.get('request_status')
    if request_status:
        if request_status == 'approved':
            if len(requests) < 5:
                cur_request.requestStatus = request_status
            else:
                return jsonify(message='Limit of applied student is reached'), 423
        elif request_status == 'declined':
            cur_request.requestStatus = request_status
        else:
            return jsonify(status='Bad data'), 400
        db.session.query(UserCourses).filter_by(ID=cur_request.ID).update(
            dict(requestStatus=request_status))
        db.session.commit()
        return jsonify(status='updated', id=cur_request.ID, username=cur_request.username, Courses_names=cur_request.Courses_names,
                       request_status=request_status), 200
    else:
        return jsonify(status="Bad data"), 400
app.run(debug=True)
