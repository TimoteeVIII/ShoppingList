from django.test import TestCase
from ninja.testing import TestClient
from .api import router
from django.contrib.auth.models import User
from django.urls import reverse


class HealthTest(TestCase):
    def test_health(self) -> None:
        api = TestClient(router)
        response = api.get("health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Healthy Application"})


class LogoutAndLoggedInTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('api-1.0.0:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Successfully Logged Out"})

    def test_logged_in(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('api-1.0.0:check_logged_in'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Logged In"})


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email="email@email.com")

    def test_valid_login(self):
        response = self.client.post(reverse("api-1.0.0:login"), {
            "username": "testuser",
            "password": "password"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Successfully logged in"})

    def test_valid_login_email(self):
        response = self.client.post(reverse("api-1.0.0:login"), {
            "email": "email@email.com",
            "password": "password"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Successfully logged in"})

    def test_invalid_no_email_or_password(self):
        response = self.client.post(reverse("api-1.0.0:login"), {
            "password": "password"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"message": "Not provided email or username"})

    def test_invalid_incorrect_password(self):
        response = self.client.post(reverse("api-1.0.0:login"), {
            "username": "testuser",
            "password": "password2"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"message": "Invalid credentials"})


class ReigsterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email="email@email.com")

    def test_valid_register(self):
        response = self.client.post(reverse("api-1.0.0:register"), {
            "email": "test@test.com",
            "first_name": "Test1",
            "last_name": "Test2",
            "username": "Test3",
            "password": "test"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "User created successfully"})

    def test_invalid_username_taken(self):
        response = self.client.post(reverse("api-1.0.0:register"), {
            "email": "test1@test.com",
            "first_name": "Test1",
            "last_name": "Test2",
            "username": "testuser",
            "password": "test"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"message": "Username taken"})

    def test_invalid_email_taken(self):
        response = self.client.post(reverse("api-1.0.0:register"), {
            "email": "email@email.com",
            "first_name": "Test1",
            "last_name": "Test2",
            "username": "Test32",
            "password": "test"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"message": "Email taken"})