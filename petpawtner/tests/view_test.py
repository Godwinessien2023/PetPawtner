from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class IndexViewTests(TestCase):
    """
    create IndexViewTests class to test the index view

    setUp method to create a test client and a test user
    Test if the index view requires login:
    Test to ensure that unauthenticated users are redirected to the login page:
    Test if the index view loads successfully for authenticated users:
    Test to ensure that authenticated users can access the index page.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_index_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/signin?next=/')

    def test_index_view_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_context_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['profile'], self.user.profile)



class SignupViewTests(TestCase):
    """
    create SignupViewTests class to test the signup view
    Test if the signup page renders correctly:

    Ensure that the signup page is accessible.
    Test successful signup:

    Ensure a new user can sign up successfully and is redirected to the settings page.
    Test signup with already taken username or email:

    Ensure proper error messages are displayed when the username or email is already taken.
    Test signup with non-matching passwords:

    Ensure an error message is displayed if passwords do not match
    """
    def setUp(self):
        self.client = Client()

    def test_signup_view_renders(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_successful_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password2': 'password123'
        })
        self.assertRedirects(response, reverse('settings'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_with_existing_username(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='12345')
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password2': 'password123'
        })
        self.assertContains(response, 'Username Taken')

    def test_signup_with_non_matching_passwords(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'password2': 'password456'
        })
        self.assertContains(response, 'Passwords do not match')


class SettingsViewTests(TestCase):
    """
    create SettingsViewTests class to test the settings view
    Test if the settings view requires login:

    Ensure that unauthenticated users are redirected to the login page.
    Test settings form submission for vets:

    Ensure that when the user selects the vet role, their profile is updated accordingly, and they are redirected to the index page.
    Test settings form submission for pet owners:

    Ensure that when the user selects the pet owner role, they are redirected to the add_pets page.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)

    def test_settings_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('settings'))
        self.assertRedirects(response, '/signin?next=/settings')

    def test_settings_form_submission_for_vet(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('settings'), {
            'role': 'vet',
            'bio': 'Test bio',
            'location': 'Test location',
            'clinic_name': 'Test Clinic',
            'specialty': 'Test Specialty',
            'years_of_experience': 10,
            'contact_info': '1234567890'
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.role, 'vet')
        self.assertTrue(Vet.objects.filter(profile=self.profile).exists())
        self.assertRedirects(response, reverse('index'))

    def test_settings_form_submission_for_pet_owner(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('settings'), {
            'role': 'owner',
            'bio': 'Test bio',
            'location': 'Test location'
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.role, 'owner')
        self.assertRedirects(response, reverse('add_pets'))



class AddPetsViewTests(TestCase):
    """
    create AddPetsViewTests class to test the add_pets view
    Test if the add_pets view requires login:

    Ensure that unauthenticated users are redirected to the login page.
    Test adding a pet:

    Ensure that a pet owner can add a new pet, and the pet is saved in the database.
    Test adding a pet with missing fields:

    Ensure that an error message is displayed if any of the required fields are missing.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id, role='owner')

    def test_add_pets_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('add_pets'))
        self.assertRedirects(response, '/signin?next=/add_pets')

    def test_adding_a_pet(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'), {
            'name': 'Buddy',
            'breed': 'Golden Retriever',
            'age': '2 years',
            'bio': 'Friendly dog'
        })
        self.assertTrue(Pet.objects.filter(name='Buddy', owner=self.profile).exists())
        self.assertRedirects(response, reverse('index'))

    def test_adding_a_pet_with_missing_fields(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'), {
            'name': 'Buddy',
            'breed': 'Golden Retriever',
            'age': '2 years'
        })
        self.assertContains(response, 'All fields are required')

    def test_adding_a_pet_with_invalid_age(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'), {
            'name': 'Buddy',
            'breed': 'Golden Retriever',
            'age': 'Invalid age',
            'bio': 'Friendly dog'
        })
        self.assertContains(response, 'Invalid age')
    
    def test_adding_a_pet_with_invalid_breed(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'), {
            'name': 'Buddy',
            'breed': 'Invalid breed',
            'age': '2 years',
            'bio': 'Friendly dog'
        })
        self.assertContains(response, 'Invalid breed')
    
    def test_adding_a_pet_with_invalid_name(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'),
                                    {
            'name': 'Invalid name',
            'breed': 'Golden Retriever',
            'age': '2 years',
            'bio': 'Friendly dog'
        })
        self.assertContains(response, 'Invalid name')
    
    def test_adding_a_pet_with_invalid_bio(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'), {
            'name': 'Buddy',
            'breed': 'Golden Retriever',
            'age': '2 years',
            'bio': 'Invalid bio'
        })
        self.assertContains(response, 'Invalid bio')
    
    def test_adding_a_pet_with_invalid_owner(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_pets'), {
            'name': 'Buddy',
            'breed': 'Golden Retriever',
            'age': '2 years',
            'bio': 'Friendly dog',
            'owner': 'Invalid owner'
        })
        self.assertContains(response, 'Invalid owner')


class SigninViewTests(TestCase):
    """
    add SigninViewTests class to test the signin view
    Test if the signin page renders correctly:

    Ensure that the signin page is accessible.
    Test successful signin:

    Ensure a user can sign in successfully and is redirected to the index page.
    Test signin with incorrect credentials:

    Ensure proper error messages are displayed when the user enters incorrect credentials.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_signin_view_renders(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_successful_login(self):
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertRedirects(response, reverse('index'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid Credentials')

    def test_signout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('signin'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('signin'))

    def test_signout_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, '/signin?next=/signout')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/signin?next=/')
    
    def test_signout_view_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('signin'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('signin'))
    
    def test_signout_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, '/signin?next=/signout')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/signin?next=/')

    def test_signout_view_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='00000')
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('signin'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('signin'))


class SignoutViewTests(TestCase):
    """
    define signout view tests class to test the signout view
    Test if the signout view requires login:

    Ensure that unauthenticated users are redirected to the login page.
    Test successful signout:

    Ensure a user can sign out successfully and is redirected to the signin page.
    Test signout with invalid credentials:

    Ensure proper error messages are displayed when the user enters incorrect credentials.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_signout_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, '/signin?next=/signout')

    def test_signout_view_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('signin'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('signin'))
    
    def test_signout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('signin'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('signin'))
    
    def test_signout_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, '/signin?next=/signout')
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/signin?next=/')
    
    def test_signout_view_loads_for_logged_in_user(self):
        self.client.login(username='testuser', password='00000')
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, reverse('signin'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('signin'))
