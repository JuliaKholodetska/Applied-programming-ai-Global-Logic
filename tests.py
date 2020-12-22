# import sys
# sys.path.append('./models')
import base64
from flask import Flask, jsonify
from datetime import datetime
from flask_testing import TestCase
import unittest
from app import app, get_user_roles
from migrate import db
import json

from models import User, Course, UserCourses


class TestingViews(TestCase):

    # creates instance of flask app
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        teacher1 = User(
            Username="vykl",
            FirstName="Yaroslav",
            LastName="Vyklyuk",
            Email="vykl@gmail.com",
            Password="sad4564fsdads",
            Phone="+380 68 xxx-xx-xx",
            UserStatus="teacher")
        student1 = User(
            Username="nstr",
            FirstName="ivnhsnk",
            LastName="damn",
            Email="son@where.did",
            Password="youfoundthis",
            Phone="+380 68 xxx-xx-xx",
            UserStatus="student")
        db.session.add_all([teacher1, student1])
        db.session.commit()

        testcourse = Course(
            ID=1,
            Category='tech',
            Name='testcourse',
            CourseHeadUsername='vykl'
        )
        # teacher2 = User("Yaroslav", date)
        db.session.add_all([testcourse])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def open_with_auth(self, url, method, username, password, json=None):
        return self.client.open(url,
                                method=method,
                                headers={
                                    'Authorization': 'Basic ' +
                                    base64.b64encode(
                                        bytes(username + ":" + password, 'ascii')).decode('ascii')
                                },
                                json=json
                                )

    def test_user_in_session(self):
        self.assertIn(db.session.query(User).get('vykl'), db.session)

    def test_get_user_role(self):
        self.assertEqual(User.query.filter_by(
            Username='nstr').first().get_roles(), 'student')

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World!', response.data)

    def test_first_lab(self):
        response = self.client.get('/api/v1/hello-world-28!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, World - 28', response.data)

    def test_create_user(self):
        data = {

            'username': 'test_username',
            'firstname': 'test_firstname',
            'lastname': 'test_lastname',
            'email': 'test_email',
            'password': 'test_password',
            'phone': 'test_phone'
        }
        res = self.client.open('/user/', method='POST', json=data)
        self.assertEqual(res.json.get('status'), 'created')
        self.assertIsNotNone(db.session.query(User).get('test_username'))

        res2 = self.client.open('/user/', method='POST', json={'username':'nstr'})
        self.assertEqual(res2.json.get('status'), 'Current user already exists')

        res3 = self.client.open('/user/', method='POST', json={})
        self.assertEqual(res3.json.get('status'), 'Bad data')

    def test_get_user_by_username(self):
        user = db.session.query(User).get('nstr')
        # getting my own username without auth
        res = self.client.open('/user/nstr', method='GET')
        self.assertEqual(res.data, b'Unauthorized Access')
        # getting my own username with auth
        res = self.open_with_auth('/user/nstr', 'GET', 'nstr', 'youfoundthis')
        self.assertEqual(jsonify(status='current User', id=user.UserID, username=user.Username, firstName=user.FirstName, lastName=user.LastName,
                                 email=user.Email, password=user.Password, phone=user.Phone, userSatus=user.UserStatus).data, res.data)
        # getting others username
        res = self.open_with_auth('/user/vykl', 'GET', 'nstr', 'youfoundthis')
        self.assertEqual(res.json.get('status'), 'Access denied')

    def test_delete_user_by_username(self):
        user = db.session.query(User).get('nstr')
        self.assertIsNotNone(user)
        res = self.open_with_auth('/user/nstr', 'DELETE', 'nstr', 'youfoundthis')
        deletedUser = db.session.query(User).get('nstr')
        self.assertIsNone(deletedUser)
        self.assertIsNone(db.session.query(UserCourses).filter(UserCourses.username == user.Username).scalar())
        self.assertEqual(res.json.get('status'), 'deleted')

    def test_put_user_by_username(self):
        # change myself:
        user = db.session.query(User).get('nstr')
        data = {
            "username": "changedusername",
            "firstname": "changedfirstname",
            "lastname": "changedlastname",
            "email": "changedemail",
            "password": "changedpassword",
            "phone": "changedphone"
        }
        res = self.open_with_auth('/user/nstr', 'PUT', 'nstr', 'youfoundthis', json=data)
        changeduser = db.session.query(User).get('changedusername')
        self.assertEqual(changeduser.LastName, 'changedlastname')
        self.assertStatus(res, 201)

    def test_userCourses(self):
        res = self.open_with_auth('/user/nstr/courses/', 'GET', 'nstr', 'youfoundthis')
        self.assertNotEqual(res.json.get('status'), 'Access denied')
    def test_apply_for_course(self):
        res = self.open_with_auth(
            '/user/nstr/apply/testcourse', 'POST', 'nstr', 'youfoundthis')
        self.assertStatus(res, 200)
        course = db.session.query(UserCourses).filter(UserCourses.username == 'nstr').scalar()
        self.assertIsNotNone(course)
        self.assertEqual(course.requestStatus, 'waiting')

    def test_create_course(self):
        data = {
            'category': 'fck',
            'name': 'test2',
            'course_head_username':'vykl'
        }
        res = self.open_with_auth('/course/', 'POST', 'vykl', 'sad4564fsdads', json=data)
        self.assertEqual(res.json.get('status'), 'created')
        self.assertEqual(db.session.query(Course).get('test2').Category, 'fck')

        res2 = self.open_with_auth('/course/', 'POST', 'nstr', 'youfoundthis', json=data)
        self.assertEqual(res2.data, b'Unauthorized Access')

        res3 = self.open_with_auth('/course/', 'POST', 'vykl', 'sad4564fsdads', json=dict())
        self.assertStatus(res3, 404)

    def test_get_all_courses(self):
        res = self.open_with_auth('/courses/', 'GET', 'vykl', 'sad4564fsdads')
        count = db.session.query(Course).count()
        if count == 0:
            self.assertEqual(res.json.get('status'), 'No courses found')
        else:
            self.assert200(res)

    def test_get_cource_by_name(self):
        res = self.open_with_auth('/course/testcourse/', 'GET', 'vykl', 'sad4564fsdads')
        self.assert200(res)

        res2 = self.open_with_auth('/course/notexisting/', 'GET', 'vykl', 'sad4564fsdads')
        self.assertEqual(res2.json.get('status'), 'Course not found')

    def test_put_cource_by_name(self):
        data = {
            "category": "changed_category",
            "name": "changed_name"
        }
        res = self.open_with_auth(
            '/course/testcourse/', 'PUT', 'vykl', 'sad4564fsdads', json=data)
        self.assertEqual(res.json.get('status'), 'updated')
        self.assertEqual(db.session.query(Course).get('changed_name').Category, data['category'])

        res2 = self.open_with_auth(
            '/course/changed_name/', 'PUT', 'vykl', 'sad4564fsdads', json={'name':"changed_name"})
        self.assertEqual(res2.json.get('status'), 'Current course already exists')

        res3 = self.open_with_auth(
            '/course/nonexisting/', 'PUT', 'vykl', 'sad4564fsdads')
        self.assertEqual(res3.json.get('status'), 'Course not found')

    def test_delete_cource_by_name(self):
        res = self.open_with_auth(
            '/course/testcourse/', 'DELETE', 'vykl', 'sad4564fsdads')
        self.assertEqual(res.json.get('status'), 'deleted')
        self.assertIsNone(db.session.query(Course).get('testcourse'))

    def test_val_requests(self):
        usrname = 'nstr'
        crsname = 'testcourse'
        res = self.open_with_auth(
            '/course/' + usrname + '/' + crsname + '/', 'PUT', 'vykl', 'sad4564fsdads')
        self.assertEqual(res.json.get('status'), 'Request not found')

        self.open_with_auth(
            '/user/nstr/apply/testcourse', 'POST', 'nstr', 'youfoundthis')
        
        res2 = self.open_with_auth('/course/' + usrname + '/' + crsname +
                                  '/', 'PUT', 'vykl', 'sad4564fsdads', json={'baddata': 'approved'})
        self.assertEqual(res2.json.get('status'), 'Bad data')

        self.open_with_auth(
            '/user/nstr/apply/testcourse', 'POST', 'nstr', 'youfoundthis')
        res3 = self.open_with_auth('/course/' + usrname + '/' + crsname +
                                  '/', 'PUT', 'vykl', 'sad4564fsdads', json={'request_status': 'approved'})
        self.assertEqual(res3.json.get('status'), 'updated')

    # def test_get_user_roles(self):
        # self.assertEqual(get_user_roles('nstr'), 'student')


if __name__ == '__main__':
    unittest.main()
