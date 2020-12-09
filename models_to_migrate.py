from migr import db

Base = db.Model


class User(Base):
    __tablename__ = 'User'

    UserID = db.Column(db.INTEGER)
    Username = db.Column(db.VARCHAR(45), primary_key=True)
    FirstName = db.Column(db.VARCHAR(45))
    LastName = db.Column(db.VARCHAR(45))
    Email = db.Column(db.VARCHAR(45))
    Password = db.Column(db.VARCHAR(45))
    Phone = db.Column(db.VARCHAR(45))
    UserStatus = db.Column(db.INTEGER)


class Course(Base):
    __tablename__ = 'Course'

    ID = db.Column(db.INTEGER)
    Category = db.Column(db.VARCHAR(45))
    Name = db.Column(db.VARCHAR(45), primary_key=True)
    AppliedStudents = db.Column(db.VARCHAR(45), db.ForeignKey(User.Username))
    AppliedStudent = db.relationship(User)


class UserCourses(Base):
    __tablename__ = 'UserCourses'

    ID = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.VARCHAR(45), db.ForeignKey(User.Username))
    User = db.relationship(User)
    Courses_names = db.Column(db.VARCHAR(45), db.ForeignKey(Course.Name))
    Courses = db.relationship(Course)


db.create_all()
