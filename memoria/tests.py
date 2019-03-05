import time
from unittest.mock import MagicMock

from selenium import webdriver

from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import LiveServerTestCase, TestCase, TransactionTestCase, Client
from django.urls import resolve
from faker import Faker
from django.db.utils import *
from .models import *
from .views import *

# --------------------------------------------------
# UNIT TESTING
class UrlTests(TestCase):
    
    def test_index(self):
        found = resolve('/')
        self.assertEqual(found.func, base_view)

    def test_signup_url(self):
        found = resolve('/signup/')
        self.assertEqual(found.func, signup)

    def test_profile_url(self):
        found = resolve('/profile/')
        self.assertEqual(found.func, user_details)

    def test_books_list_url(self):
        found = resolve('/books/')
        self.assertEqual(found.func, book_list)

    def test_films_list_url(self):
        found = resolve('/films/')
        self.assertEqual(found.func, film_list)

    def test_tvseries_list_url(self):
        found = resolve('/tvseries/')
        self.assertEqual(found.func, tvseries_list)

    def test_books_new_url(self):
        found = resolve('/books/new')
        self.assertEqual(found.func, book_create)

    def test_films_new_url(self):
        found = resolve('/films/new')
        self.assertEqual(found.func, film_create)

    def test_tvseries_new_url(self):
        found = resolve('/tvseries/new')
        self.assertEqual(found.func, tvseries_create)

    def test_book_view_url(self):
        found = resolve('/books/1')
        self.assertEqual(found.func, book_view)

    def test_film_view_url(self):
        found = resolve('/films/1')
        self.assertEqual(found.func, film_view)

    def test_tvseries_view_url(self):
        found = resolve('/tvseries/1')
        self.assertEqual(found.func, tvseries_view)

    def test_book_delete_url(self):
        found = resolve('/books/1/delete')
        self.assertEqual(found.func, book_delete)

    def test_film_delete_url(self):
        found = resolve('/films/1/delete')
        self.assertEqual(found.func, film_delete)

    def test_tvseries_delete_url(self):
        found = resolve('/tvseries/1/delete')
        self.assertEqual(found.func, tvseries_delete)

    def test_book_edit_url(self):
        found = resolve('/books/1/edit')
        self.assertEqual(found.func, book_edit)

    def test_film_edit_url(self):
        found = resolve('/films/1/edit')
        self.assertEqual(found.func, film_edit)

    def test_tvseries_edit_url(self):
        found = resolve('/tvseries/1/edit')
        self.assertEqual(found.func, tvseries_edit)

class SignupTests(TestCase):
    def testSignupValid(self):
        data = {'username':'john_wayne',
                'password':'pass1234',
                'password_confirmation':'pass1234'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, True)

    def testSignupLongUsername(self):
        data = {'username':'abcdefghijklmnopqrstuvwxyz',
                'password':'pass1234',
                'password_confirmation':'pass1234'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

    def testSignupNoPassword(self):
        data = {'username': 'john_wayne',
                'password': 'pass1234'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)


    def testSignUpShortPassword(self):
        data = {'username': 'john_wayne',
                'password': 'pas',
                'password_confirmation': 'pas'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

    def testSignupShortName(self):
        data = {'username': 'jo',
                'password': 'pass1234',
                'password_confirmation': 'pass1234'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

    def testSignupNameWithSpace(self):
        data = {'username': 'joe key',
                'password': 'pass1234',
                'password_confirmation': 'pass1234'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

    def testSignupNotMatchingPasswords(self):
        data = {'username': 'john_wayne',
                'password': 'pass1234',
                'password_confirmation': 'pass1243'}
        f = SignupForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

class LoginTests(TestCase):
    def testLoginValid(self):
        data = {'username': 'john_wayne',
                'password': 'pass1234'}
        f = LoginForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, True)

    def testLoginNoPassword(self):
        data = {'username': 'john_wayne',
                'password': ''}
        f = LoginForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

    def testLoginNoData(self):
        data = {'username': '',
                'password': ''}
        f = LoginForm(data)
        status = f.is_valid() and f.is_data_valid()
        self.assertEqual(status, False)

# ---------------------------------------------------
# INTEGRATIONTESTS
class UserCreationTests(TestCase):
    def testUserCreationFull(self):
        user = User(username="test_user123", password="test_password123")
        user.save()
        self.assertEqual(user, User.objects.get(username="test_user123"))

    def testUserCreationExisted(self):
        user1 = User(username="test_user123", password="test_password123")
        user2 = User(username="test_user123", password="test_password321")
        user1.save()
        try:
            user2.save()
            self.assertEqual(True, False)
        except:
            self.assertEqual(True, True)

class RecordsCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')

    def tearDown(self):
        self.user.delete()

    def testBookCreationFull(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['name'] = 'Some book name'
        request.POST['comment'] = 'Some book comment'

        response = book_create(request)
        self.assertEqual(Book.objects.count(), 1)
        new_book = Book.objects.first()
        self.assertEqual(new_book.name, 'Some book name')

    def testBookCreationNoComment(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['name'] = 'Some book name2'

        response = book_create(request)
        self.assertEqual(Book.objects.count(), 1)
        new_book = Book.objects.first()
        self.assertEqual(new_book.name, 'Some book name2')

    def testBookCreationEmpty(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user

        response = book_create(request)
        self.assertEqual(Book.objects.count(), 0)

    def testBookCreationNoTitle(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['comment'] = 'Some book comment'

        response = book_create(request)
        self.assertEqual(Book.objects.count(), 0)


    def testFilmCreationFull(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['name'] = 'Some film name'
        request.POST['comment'] = 'Some film comment'

        response = film_create(request)
        self.assertEqual(Film.objects.count(), 1)
        new_film = Film.objects.first()
        self.assertEqual(new_film.name, 'Some film name')

    def testFilmCreationNoComment(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['name'] = 'Some film name2'

        response = film_create(request)
        self.assertEqual(Film.objects.count(), 1)
        new_film = Film.objects.first()
        self.assertEqual(new_film.name, 'Some film name2')

    def testFilmCreationEmpty(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user

        response = film_create(request)
        self.assertEqual(Film.objects.count(), 0)

    def testFilmCreationNoTitle(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['comment'] = 'Some film comment'

        response = film_create(request)
        self.assertEqual(Film.objects.count(), 0)


    def testTVSCreationFull(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['name'] = 'Some tvs name'
        request.POST['comment'] = 'Some tvs comment'

        response = tvseries_create(request)
        self.assertEqual(TVSeries.objects.count(), 1)
        new_tvs = TVSeries.objects.first()
        self.assertEqual(new_tvs.name, 'Some tvs name')

    def testTVSCreationNoComment(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['name'] = 'Some tvs name2'

        response = tvseries_create(request)
        self.assertEqual(TVSeries.objects.count(), 1)
        new_tvs = TVSeries.objects.first()
        self.assertEqual(new_tvs.name, 'Some tvs name2')

    def testTVSCreationEmpty(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        response = tvseries_create(request)
        self.assertEqual(TVSeries.objects.count(), 0)

    def testTVSCreationNoTitle(self):
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.user
        request.POST['comment'] = 'Some tvs comment'

        response = tvseries_create(request)
        self.assertEqual(TVSeries.objects.count(), 0)


class ShowAddedRecordsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123')

    def tearDown(self):
        self.user.delete()

    def testShowAddedBook(self):
        Book.objects.create(author=self.user, name="book1", comment='')
        Book.objects.create(author=self.user, name="book2", comment='some comment for book2')
        Book.objects.create(author=self.user, name="book3", comment='.')

        request = HttpRequest()
        request.user = self.user
        responce = book_list(request)

        self.assertIn('book1', responce.content.decode())
        self.assertIn('book2', responce.content.decode())
        self.assertIn('book3', responce.content.decode())

    def testShowAddedFilm(self):
        Film.objects.create(author=self.user, name="film1", comment='')
        Film.objects.create(author=self.user, name="film2", comment='some comment for book2')
        Film.objects.create(author=self.user, name="film3", comment='.')

        request = HttpRequest()
        request.user = self.user
        responce = film_list(request)

        self.assertIn('film1', responce.content.decode())
        self.assertIn('film2', responce.content.decode())
        self.assertIn('film3', responce.content.decode())

    def testShowAddedTVS(self):
        TVSeries.objects.create(author=self.user, name="tvs1", comment='')
        TVSeries.objects.create(author=self.user, name="tvs2", comment='some comment for tvs2')
        TVSeries.objects.create(author=self.user, name="tvs3", comment='.')

        request = HttpRequest()
        request.user = self.user
        responce = tvseries_list(request)

        self.assertIn('tvs1', responce.content.decode())
        self.assertIn('tvs2', responce.content.decode())
        self.assertIn('tvs3', responce.content.decode())

# -----------------------------------------------------
# SYSTEMTESTS

# Total: 3 tests
# Types: 3
class systemAccountTests(TransactionTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)
        self.fake = Faker()

    def tearDown(self):
        self.driver.quit()

    def test_signup(self):
        
        self.driver.get("http://localhost:8000/signup/")
        self.driver.find_element_by_name('username').send_keys(self.fake.name().replace(" ", "_"))
        self.driver.find_element_by_name('password1').send_keys("test_pass_123")
        self.driver.find_element_by_name('password2').send_keys("test_pass_123")
        self.driver.find_element_by_class_name('some_button').click()

        self.assertEqual("http://localhost:8000/profile/", self.driver.current_url)

    def test_login(self):

        self.driver.get("http://localhost:8000/login/")
        self.driver.find_element_by_name('username').send_keys("test_name")
        self.driver.find_element_by_name('password').send_keys("test_pass_123")
        self.driver.find_element_by_class_name('some_button').click()

        self.assertEqual("http://localhost:8000/profile/", self.driver.current_url)

    def test_logout(self):
        self.driver.get("http://localhost:8000/login/")
        self.driver.find_element_by_name('username').send_keys("test_name")
        self.driver.find_element_by_name('password').send_keys("test_pass_123")
        self.driver.find_element_by_class_name('some_button').click()

        self.driver.find_element_by_name('exit_button').click()
        self.assertEqual("http://localhost:8000/", self.driver.current_url)

# Total: 4 tests
# Types: 4
class systemAdminTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.fake = Faker()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()


    def test_add_user_via_admin(self):
        self.driver.get("http://localhost:8000/admin/")
        self.driver.find_element_by_id("id_username").send_keys("anna")
        self.driver.find_element_by_id("id_password").send_keys("ananas1997")

        self.driver.find_element_by_xpath('//input[@value="Войти"]').click()
        self.driver.get("http://localhost:8000/admin/auth/user/add")


        self.driver.find_element_by_id("id_username").send_keys(self.fake.name().replace(" ", "_"))
        password = self.fake.password()
        self.driver.find_element_by_id("id_password1").send_keys(password)
        self.driver.find_element_by_id("id_password2").send_keys(password)


        self.driver.find_element_by_id("user_form").submit()
        self.assertIn("Добавить пользователь", self.driver.title)

    def test_add_book_via_admin(self):
        self.driver.get("http://localhost:8000/admin/")
        self.driver.find_element_by_id("id_username").send_keys("anna")
        self.driver.find_element_by_id("id_password").send_keys("ananas1997")


        self.driver.find_element_by_xpath('//input[@value="Войти"]').click()
        self.driver.get("http://localhost:8000/admin/memoria/book/add/")


        self.driver.find_element_by_id("id_author").send_keys("anna")
        self.driver.find_element_by_id("id_name").send_keys(self.fake.words(nb=3, ext_word_list=None, unique=False))
        self.driver.find_element_by_id("id_comment").send_keys(self.fake.text())


        self.driver.find_element_by_id("book_form").submit()
        self.assertIn("Добавить", self.driver.title)

    def test_add_film_via_admin(self):
        self.driver.get("http://localhost:8000/admin/")
        self.driver.find_element_by_id("id_username").send_keys("anna")
        self.driver.find_element_by_id("id_password").send_keys("ananas1997")


        self.driver.find_element_by_xpath('//input[@value="Войти"]').click()
        self.driver.get("http://localhost:8000/admin/memoria/film/add/")


        self.driver.find_element_by_id("id_author").send_keys("anna")
        self.driver.find_element_by_id("id_name").send_keys(self.fake.words(nb=3, ext_word_list=None, unique=False))
        self.driver.find_element_by_id("id_comment").send_keys(self.fake.text())


        self.driver.find_element_by_id("film_form").submit()
        self.assertIn("Добавить", self.driver.title)

    def test_add_tvseries_via_admin(self):
        self.driver.get("http://localhost:8000/admin/")
        self.driver.find_element_by_id("id_username").send_keys("anna")
        self.driver.find_element_by_id("id_password").send_keys("ananas1997")


        self.driver.find_element_by_xpath('//input[@value="Войти"]').click()
        self.driver.get("http://localhost:8000/admin/memoria/tvseries/add/")


        self.driver.find_element_by_id("id_author").send_keys("anna")
        self.driver.find_element_by_id("id_name").send_keys(self.fake.words(nb=3, ext_word_list=None, unique=False))
        self.driver.find_element_by_id("id_comment").send_keys(self.fake.text())


        self.driver.find_element_by_id("tvseries_form").submit()
        self.assertIn("Добавить", self.driver.title)


# Total: 4 tests
# Types: 4
class systemUserTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.fake = Faker()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

    def test_add_book_via_user(self):
        self.driver.get("http://localhost:8000/login/")
        self.driver.find_element_by_name('username').send_keys("test_name")
        self.driver.find_element_by_name('password').send_keys("test_pass_123")
        self.driver.find_element_by_class_name('some_button').click()

        self.driver.find_element_by_name("books_list_button").click()
        self.driver.find_element_by_name("add_button").click()

        self.driver.find_element_by_id("id_name").send_keys(self.fake.words(nb=3, ext_word_list=None, unique=False))
        self.driver.find_element_by_id("id_comment").send_keys(self.fake.text())


        self.driver.find_element_by_class_name('some_button').click()
        self.assertEqual("http://localhost:8000/books/", self.driver.current_url)

    def test_add_film_via_user(self):
        self.driver.get("http://localhost:8000/login/")
        self.driver.find_element_by_name('username').send_keys("test_name")
        self.driver.find_element_by_name('password').send_keys("test_pass_123")
        self.driver.find_element_by_class_name('some_button').click()

        self.driver.find_element_by_name("films_list_button").click()
        self.driver.find_element_by_name("add_button").click()

        self.driver.find_element_by_id("id_name").send_keys(self.fake.words(nb=3, ext_word_list=None, unique=False))
        self.driver.find_element_by_id("id_comment").send_keys(self.fake.text())


        self.driver.find_element_by_class_name('some_button').click()
        self.assertEqual("http://localhost:8000/films/", self.driver.current_url)

    def test_add_tvseries_via_user(self):
        self.driver.get("http://localhost:8000/login/")
        self.driver.find_element_by_name('username').send_keys("test_name")
        self.driver.find_element_by_name('password').send_keys("test_pass_123")
        self.driver.find_element_by_class_name('some_button').click()

        self.driver.find_element_by_name("tvseries_list_button").click()
        self.driver.find_element_by_name("add_button").click()

        self.driver.find_element_by_id("id_name").send_keys(self.fake.words(nb=3, ext_word_list=None, unique=False))
        self.driver.find_element_by_id("id_comment").send_keys(self.fake.text())


        self.driver.find_element_by_class_name('some_button').click()
        self.assertEqual("http://localhost:8000/tvseries/", self.driver.current_url)

