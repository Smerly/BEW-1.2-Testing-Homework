import os
from unittest import TestCase

from datetime import date
 
from books_app.extensions import app, db, bcrypt
from books_app.models import Book, Author, User, Audience

"""
Run these tests with the command:
python -m unittest books_app.main.tests
"""

#################################################
# Setup
#################################################

def create_books():
    a1 = Author(name='Harper Lee')
    b1 = Book(
        title='To Kill a Mockingbird',
        publish_date=date(1960, 7, 11),
        author=a1
    )
    db.session.add(b1)

    a2 = Author(name='Sylvia Plath')
    b2 = Book(title='The Bell Jar', author=a2)
    db.session.add(b2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        # TODO: Write a test for the signup route. It should:
        create_user()
        # - Make a POST request to /signup, sending a username & password
        user_info = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/signup', data=user_info)
        # - Check that the user now exists in the database
        user = User.query.filter_by(username='me1').one()
        self.assertIn(user.username, 'me1')
        

    def test_signup_existing_user(self):
        # TODO: Write a test for the signup route. It should:
        create_user()
        # - Create a user
        user_info = {
            'username': 'me1',
            'password': 'password',
        }
        # - Make a POST request to /signup, sending the same username & password
        response = self.app.post('/signup', data=user_info)
        # - Check that the form is displayed again with an error message
        
        response_text = response.get_data(as_text=True)
        # self.assertEqual(response.status_code, 200)
        self.assertIn(response_text, 'That username is taken. Please choose a different one')
        


    def test_login_correct_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        user_info = {
            'username': 'asd',
            'password': 'asd',
        }
        
        # - Make a POST request to /login, sending the created username & password
        self.app.post('/login', data=user_info)
        response = self.app.get('/', follow_redirects=True)
        response_text = response.get_data(as_text=True)
        # - Check that the "login" button is not displayed on the homepage
        self.assertIn('<a href="/login">Log In</a>', response_text)
        

    def test_login_nonexistent_user(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        user_info = {
            'username': 'me239u48238490',
            'password': 'password',
        }
        # - Make a POST request to /login, sending a username & password
        response = self.app.post('/login', data=user_info)
        response_text = response.get_data(as_text=True)
        # - Check that the login form is displayed again, with an appropriate error
        self.assertIn('No user with that username. Please try again', response_text)

    def test_login_incorrect_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        user_info = {
            'username': 'asd',
            'password': 'password123123sdgyudgqwuyvfi',
        }
        # - Make a POST request to /login, sending a username & password
        response = self.app.post('/login', data=user_info)
        response_text = response.get_data(as_text=True)
        # - Check that the login form is displayed again, with an appropriate error
        self.assertIn('Password doesn\'t match. Please try again', response_text)

    def test_logout(self):
        # TODO: Write a test for the logout route. It should:
        # - Create a user
        user_info = {
            'username': 'asd',
            'password': 'asd',
        }
        # - Log the user in (make a POST request to /login)
        self.app.post('/login', data=user_info)
        # - Make a GET request to /logout
        self.app.get('/logout', follow_redirects=True)
        # - Check that the "login" button appears on the homepage
        response = self.app.get('/', follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('<a href="/login">Log In</a>', response_text)
        pass
