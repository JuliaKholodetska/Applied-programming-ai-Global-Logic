from models_to_migrate import *


# db.create_all()

user = User(UserID=1, Username="rost", FirstName="Pantyo", LastName="Rostyslav", Email="@mail.com", Password='sadsdads', Phone="213231312", UserStatus="1")
user1 = User(UserID=2, Username="rosst", FirstName="Passntyo", LastName="Rosatyslav", Email="@mdail.com", Password='sadfsdads', Phone="21323231312", UserStatus="1")

course = Course(ID=2, Category="IT", Name="GoodCourse", AppliedStudent=user)
# course1 = Course(ID=3, Category="ITS", Name="GoodCoursFSe", AppliedStudent=user1)
course2 = Course(ID=4, Category="ITD", Name="GoodCourssfe", AppliedStudent=user)
course = Course(ID=3, Category="IT", Name="GoodCourse", AppliedStudent=user1)

# UserCourse = UserCourses(ID=3, User=user1, Courses=course1)
UserCourse1 = UserCourses(ID=4, User=user, Courses=course)
db.session.add(user)
# db.session.add(user1)
db.session.add(course)
# db.session.add(course1)
db.session.add(course2)
# db.session.add(UserCourse)
db.session.add(UserCourse1)

db.session.commit()
