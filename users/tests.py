from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from users.models import Profile
from users.views import RegistrationView
from users.forms import SignUpForm

UserObj = get_user_model()


class ProfileTest(TestCase):

    def test_profile_creation(self):
        user = UserObj.objects.create_user(
            email="taskbuster@test.com", password="django-tutorial")
        user.username = "taskbuster"
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.__str__(), user.email)


# class ProfileRegistrationFormsTest(TestCase):
#
#     def test_invalid_forms(self):
#
#         invalid_data_dicts = [
#             # Non-alphanumeric username.
#             {
#                 'data':{
#                     'username': 'foo/bar',
#                     'first_name': "waht",
#                     "last_name": "what",
#                     'email': 'foo@example.com',
#                     "birth_date": "2000-10-10",
#                     'password1': 'secret3123',
#                     'password2': 'secret3123'},
#                 'error':
#                     ('username', [u'{"username": [{"message": "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.", "code": "invalid"}]}'])
#             },
#             # Mismatched passwords.
#             {
#                 'data': {
#                     'username': 'foo',
#                     'email': 'foo@example.com',
#                     "birth_date": "2000-10-10",
#                     'first_name': "waht",
#                     "last_name": "what",
#                     'password1': 'alksjdflaks',
#                     'password2': 'baragsdfds'
#                         },
#                 'error':
#                     ('__all__', [r'''{"password2": [{"message": "The two password fields didn\u2019t match.", "code": "password_mismatch"}]}'''])
#             },
#             # Too common password
#             {
#                 'data':
#                     {'username': 'foo',
#                      'email': 'foo@example.com',
#                      "birth_date": "2000-10-10",
#                      'first_name': "waht",
#                      "last_name": "what",
#                      'password1': 'asdfasdf',
#                      'password2': 'asdfasdf'},
#                 'error':
#                     ('password2', ['{"password2": [{"message": "This password is too common.", "code": "password_too_common"}]}'])
#             },
#             # Too short password
#             {
#                 'data': {
#                         'username': 'fo12o12',
#                         'email': 'fofadso@example.com',
#                         "birth_date": "2000-10-10",
#                         'first_name': "waht",
#                         "last_name": "what",
#                         'password1': 'foo',
#                         'password2': 'foo'
#                         },
#                 'error':
#                     ('password2', ['{"password2": [{"message": "This password is too short. It must contain at least 8 characters.", "code": "password_too_short"}]}'])
#             },
#             # Password too similar to the username
#             {
#                 'data': {
#                     'username': 'foofoofoo1',
#                     'email': 'fofadso@example.com',
#                     "birth_date": "2000-10-10",
#                     'first_name': "waht",
#                     "last_name": "what",
#                     'password1': 'foofoofoo1',
#                     'password2': 'foofoofoo1'
#                         },
#                 'error':
#                     ('password2', [
#                         '{"password2": [{"message": "The password is too similar to the username.", "code": "password_too_similar"}]}'])
#             },
#             # Password too similar to email
#             {
#                 'data': {
#                     'username': 'fo12o12',
#                     'email': 'foofoofoo@example.com',
#                     "birth_date": "2000-10-10",
#                     'first_name': "waht",
#                     "last_name": "what",
#                     'password1': 'foofoofoo',
#                     'password2': 'foofoofoo'
#                         },
#                 'error':
#                     ('password2', [
#                         '{"password2": [{"message": "The password is too similar to the email address.", "code": "password_too_similar"}]}'])
#             }
#             ]
#
#         for invalid_dict in invalid_data_dicts:
#             form = SignUpForm(data=invalid_dict['data'])
#             self.assertEqual(form.errors.as_json(), invalid_dict['error'][1][0])
#             self.failIf(form.is_valid())
#
#         user1 = UserObj.objects.create(email="taskbuster22@test.com", password="django-tutorial")
#
#         form = SignUpForm(data={
#                     'username': 'taskbuster22',
#                     'email': 'taskbuster22@test.com',
#                     "birth_date": "2000-10-10",
#                     'first_name': "waht",
#                     "last_name": "what",
#                     'password1': 'foofgfgoo11',
#                     'password2': 'foofgfgoo11'
#                         },)
#         self.assertEqual('{"username": [{"message": "User already exists.", "code": ""}]}', form.errors.as_json())
#         self.failIf(form.is_valid())
#
#     def test_valid_form(self):
#         form = SignUpForm(data={'username': "twhataaa",
#                                 'password1': 'django-tutorial1',
#                                 'password2': 'django-tutorial1',
#                                 'first_name': "test",
#                                 "last_name": "test",
#                                 "email": "teste@test.pl",
#                                 "birth_date": "2000-10-10"})
#         self.failUnless(form.is_valid())


class UsersViewsTest(TestCase):
    longMessage = True
    view_class = RegistrationView

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserObj.objects.create_user(email="test@gmail.com", password="django-tutorial")
        self.user.profile.username = 'test'
        self.user.save()

    def test_login(self):
        resp = self.client.post('/users/login/', {'email': 'test@gmail.com', 'password': 'django-tutorial'})
        self.assertEqual(self.client.session['_auth_user_id'], '1')

    def test_logged_out_home_page(self):
        response = self.client.get("/users/home/")
        self.assertEqual(response.status_code, 200)

    def test_logged_out_auth_pages(self):
        register_response = self.client.get("/users/register/")
        login_response = self.client.get("/users/login/")
        self.assertEqual(register_response.status_code, 200)
        self.assertEqual(login_response.status_code, 200)

    def test_logged_in_auth_pages(self):
        self.client.post('/users/login/', {'email': "test@gmail.com", 'password': "django-tutorial"})
        register_response = self.client.get("/users/register/")
        login_response = self.client.get("/users/login/")
        self.assertRedirects(login_response, '/users/profile/test/', status_code=302, target_status_code=200)
        self.assertRedirects(register_response, '/users/profile/test/', status_code=302, target_status_code=200)

    # email="taskbuster@test.com", password="django-tutorial"

    def test_redirect_after_existing_user_login(self):
        resp = self.client.post('/users/login/', {'email': 'test@gmail.com', 'password': 'django-tutorial'})
        self.assertRedirects(resp, "/users/profile/test/", status_code=302, target_status_code=200)
        self.assertEqual(resp.status_code, 302)

    # def test_anonymous_user_login(self):
    #     response = self.client.post("/users/login/", {
    #         "email": "whatever@test.com",
    #         "password": "django-tutorial"
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.is_rendered, True)
    #
    def test_anonymous_user_register(self):
        response = self.client.post("/users/register/", {
            "user": UserObj,
            'username': "taskbuster12",
            'password1': 'django-tutorial1',
            'password2': 'django-tutorial1',
            'first_name': "testd",
            "last_name": "tesft",
            "email": "testfe@test.pl",
            "birth_date": "2000-10-10"
        })
        self.assertIn(response.status_code, [301, 302], "User registration request was not redirected.")
        self.assertEqual(response.url, f"/users/profile/taskbuster12/")

    def test_existing_user_register(self):
        data = {'username': "taskbuster",
                'password1': 'django-tutorial1',
                'password2': 'django-tutorial1',
                'first_name': "test",
                "last_name": "test",
                "email": "test@gmail.com",
                "birth_date": "2000-10-10"}
        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.is_rendered, True)

    def test_logged_out_profile_page(self):
        response = self.client.get("/users/profile/test/")
        self.assertRedirects(response, '/users/login/', status_code=302, target_status_code=200)

    def test_logged_in_profile_page(self):
        response1 = self.client.post("/users/login/", {
            "email": "test@gmail.com",
            "password": "django-tutorial"
        })
        response2 = self.client.get("/users/profile/test/")
        self.assertEqual(response2.status_code, 200)

    def test_logout(self):
        self.client.post('/users/login/', {'email': "test@gmail.com", 'password': "django-tutorial"})
        self.assertEqual(self.client.session['_auth_user_id'], '1')
        response = self.client.get('/users/logout/')
        self.assertIn(response.status_code, [301, 302])
        self.assertFalse("_auth_user_id" in self.client.session.keys())

