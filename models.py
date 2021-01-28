from migrate import db
# from app import db
from werkzeug.security import generate_password_hash

Base = db.Model

class User(db.Model):
    __tablename__ = 'User'

    # UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, autoincrement=True)
    Username = db.Column(db.String(45), primary_key=True, nullable=False)
    FirstName = db.Column(db.String(45), nullable=False)
    LastName = db.Column(db.String(45), nullable=False)
    Email = db.Column(db.String(45))
    Password = db.Column(db.String(256))
    Phone = db.Column(db.String(45))
    UserStatus = db.Column(db.String(45))
    # courses = db.relationship('Course', backref='User', lazy=True)

    # db.UniqueConstraint(Username)

    def get_roles(self):
        return self.UserStatus


class Course(db.Model):
    __tablename__ = 'Course'

    ID = db.Column(db.Integer)
    Category = db.Column(db.String(45))
    Name = db.Column(db.String(45), primary_key=True)
    CourseHeadUsername = db.Column(db.String(45), db.ForeignKey(User.Username), nullable=False)
    # db.UniqueConstraint(CourseHeadUsername)
    # CourseHead = db.relationship(User)

    def get_course(self):
        result = {
            'id': self.ID,
            'category': self.Category,
            'name': self.Name,
            'course_head_username': self.CourseHeadUsername
        }
        return result


class UserCourses(db.Model):
    __tablename__ = 'UserCourses'

    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), db.ForeignKey(User.Username))
    User = db.relationship(User)
    Courses_names = db.Column(db.String(45), db.ForeignKey(Course.Name), nullable=False)
    Courses = db.relationship(Course)
    requestStatus = db.Column(db.String(45))

db.drop_all()
db.create_all()

# teacher1 = User(
#     Username="vykl",
#     FirstName="Yaroslav",
#     LastName="Vyklyuk",
#     Email="vykl@gmail.com",
#     Password="sad4564fsdads",
#     Phone="+380 68 xxx-xx-xx",
#     UserStatus="teacher")
# student1 = User(
#     Username="nstr",
#     FirstName="ivnhsnk",
#     LastName="damn",
#     Email="son@where.did",
#     Password="youfoundthis",
#     Phone="+380 68 xxx-xx-xx",
#     UserStatus="student")
# db.session.add_all([teacher1, student1])
# db.session.commit()

# testcourse = Course(
#     ID=1,
#     Category='tech',
#     Name='testcourse',
#     CourseHeadUsername='vykl'
#     )
# # teacher2 = User("Yaroslav", date)
# db.session.add_all([testcourse])
# db.session.commit()
