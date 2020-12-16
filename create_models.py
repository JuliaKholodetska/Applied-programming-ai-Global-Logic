from models import *
import datetime

db.create_all()

user = User(UserID=1, Username="rost", FirstName="Rostyslav", LastName="Pantyo", Email="rostr@gmail.com", Password='sadsdads', Phone="+380 68 xxx-xx-xx", UserStatus="student")
user1 = User(UserID=2, Username="yarko", FirstName="Yaroslav", LastName="Karabin", Email="yarko@gmail.com", Password='fff89f54sd', Phone="+380 68 xxx-xx-xx", UserStatus="student")

user1_t = User(UserID=3, Username="yurii", FirstName="Yurii", LastName="Kryvenchuk", Email="yurii@gmail.com", Password='sdfkljgbh87878', Phone="+380 68 xxx-xx-xx", UserStatus="teacher")
user2_t = User(UserID=4, Username="vykl", FirstName="Yaroslav", LastName="Vyklyuk", Email="vykl@gmail.com", Password='sad4564fsdads', Phone="+380 68 xxx-xx-xx", UserStatus="teacher")

course = Course(ID=1, Category="OS", Name="Operating Systems", CourseHead=user1_t)
course2 = Course(ID=2, Category="PP", Name="Applied programming", CourseHead=user2_t)

UserCourse1 = UserCourses(ID=1, User=user, Courses=course, requestStatus="approved")
UserCourse2 = UserCourses(ID=2, User=user1, Courses=course, requestStatus="approved")
UserCourse3 = UserCourses(ID=3, User=user, Courses=course2, requestStatus="approved")
UserCourse4 = UserCourses(ID=4, User=user1, Courses=course2, requestStatus="approved")

# db.session.add(user)
# db.session.add(user1)
# db.session.add(user1_t)
# db.session.add(user2_t)
# db.session.add(course)
# db.session.add(course2)
db.session.add(UserCourse1)
db.session.add(UserCourse2)
db.session.add(UserCourse3)
db.session.add(UserCourse4)

db.session.commit()
