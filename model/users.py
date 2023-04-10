"""
These imports define the key object
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
These object and definitions are used throughout the Jupyter Notebook.
"""

# Setup of key Flask object (app)
app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
database = 'sqlite:///sqlite.db'  # path and filename of database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()


# This belongs in place where it runs once per project
db.init_app(app)

""" database dependencies to support sqlite examples """
import datetime
from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into a Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL


# Defining the template for users, class definition template. Used to create objects for type user.
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    # Attributes used for future defined users
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _completedLessonOne = db.Column(db.Boolean, unique=False, nullable=False)
    _completedQuiz = db.Column(db.Boolean, unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    # The constructed used to instantiate an object from our user class
    def __init__(self, name, uid, completedQuiz, completedLessonOne, password="123qwerty"):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._completedQuiz = completedQuiz
        self._completedLessonOne = completedLessonOne
        self.set_password(password)
        


    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts uid from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows uid to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid

    # completedQuiz getter
    @property
    def completedQuiz(self):
        return self._completedQuiz
    
    # completedQuiz setter
    @completedQuiz.setter
    def completedQuiz(self, completedQuiz):
        self._completedQuiz = completedQuiz

    # completedLessonOne getter
    @property
    def completedLessonOne(self):
        return self._completedLessonOne
    
    # completedLessonOne setter
    @completedLessonOne.setter
    def completedLessonOne(self, completedLessonOne):
        self._completedLessonOne = completedLessonOne
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional method used for setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method='sha256')

    # check password parameter against stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
       
    
    # output content using str(object) is in human readable form
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "completedQuiz": self.completedQuiz,
            "completedLessonOne": self.completedLessonOne
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="", completedQuiz=False, completedLessonOne=False):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if completedQuiz == True:
            self.completedQuiz = True
        else:
            self.completedQuiz = False
        if completedLessonOne == True:
            self.completedLessonOne = True
        else:
            self.completedLessonOne = False

        db.session.add(self) # performs update when id exists\n",
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
       

"""Database Creation and Testing """


# Builds working user data
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Theo H', uid='TheoH32', password='theo131!', completedQuiz=False, completedLessonOne=False)
        u2 = User(name='Alexa C', uid='littelex', password='pumpkin868', completedQuiz=False, completedLessonOne=False)
        u3 = User(name='Ava C', uid='spiderman', password='apple234', completedQuiz=False, completedLessonOne=False)
        u4 = User(name='Samarth K', uid='chesslover', password='broccoli199', completedQuiz=False, completedLessonOne=False)
        u5 = User(name='Ananya G', uid='ananya123', password='orange346', completedQuiz=False, completedLessonOne=False)
        u6 = User(name='Haseeb B', uid='haseebtheman', password='carrot135', completedQuiz=False, completedLessonOne=False)

        users = [u1, u2, u3, u4, u5, u6]


        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add user to table'''
                object = user.create()
                print(f"Created new uid {object.uid}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {user.uid}, or error.")
                
initUsers()