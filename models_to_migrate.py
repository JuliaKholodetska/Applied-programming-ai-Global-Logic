from migr import db

BaseModel = db.Model


class User(BaseModel):
    __tablename__ = 'User'

    UserID = db.Column(db.INTEGER, autoincrement=True)
    Username = db.Column(db.VARCHAR(45), primary_key=True, nullable=False)
    FirstName = db.Column(db.VARCHAR(45), nullable=False)
    LastName = db.Column(db.VARCHAR(45), nullable=False)
    Email = db.Column(db.VARCHAR(45))
    Password = db.Column(db.VARCHAR(256))
    Phone = db.Column(db.VARCHAR(45))
    UserStatus = db.Column(db.VARCHAR(45))

    def get_roles(self):
        return self.UserStatus


class Course(BaseModel):
    __tablename__ = 'Course'

    ID = db.Column(db.INTEGER)
    Category = db.Column(db.VARCHAR(45))
    Name = db.Column(db.VARCHAR(45), primary_key=True)
    CourseHeadUsername = db.Column(db.VARCHAR(45), db.ForeignKey(User.Username))
    CourseHead = db.relationship(User)

    def get_course(self):
        result = {
            'id': self.ID,
            'category': self.Category,
            'name': self.Name,
            'course_head_username': self.CourseHeadUsername
        }
        return result


class UserCourses(BaseModel):
    __tablename__ = 'UserCourses'

    ID = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.VARCHAR(45), db.ForeignKey(User.Username))
    User = db.relationship(User)
    Courses_names = db.Column(db.VARCHAR(45), db.ForeignKey(Course.Name))
    Courses = db.relationship(Course)
    requestStatus = db.Column(db.VARCHAR(45))

db.create_all()
