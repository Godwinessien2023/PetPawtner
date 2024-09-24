from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Post, Pet, Like

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.post = Post.objects.create(user=self.user, caption='Test Post')
        self.pet = Pet.objects.create(owner=self.profile, name='Test Pet', breed='Test Breed', age=1)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_settings_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_add_pets_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_pets'), {
            'name': 'New Pet',
            'breed': 'New Breed',
            'age': 2,
            'bio': 'New Bio',
            'location': 'New Location',
            'profileimg': None
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name='New Pet').exists())

    def test_signin_view(self):
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

    def test_post_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post'), {
            'image_upload': None,
            'caption': 'New Post'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(caption='New Post').exists())

    def test_like_post_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('like_post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.like_set.count(), 1)

    def test_search_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_signout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)

    # Additional tests
    def test_home_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/home')

    def test_profile_view_404_if_user_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', args=['nonexistentuser']))
        self.assertEqual(response.status_code, 404)

    def test_settings_view_post_update_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('settings'), {
            'role': 'owner',
            'bio': 'Updated Bio',
            'location': 'Updated Location',
            'profileimg': None
        })
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated Bio')

    def test_add_pets_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_pets'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin?next=/add_pets')

    def test_signin_view_invalid_credentials(self):
        response = self.client.post(reverse('signin'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin')

    def test_post_view_missing_fields(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post'), {
            'caption': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(caption='').exists())

    def test_like_post_view_unlike(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.get(reverse('like_post'), {'post_id': self.post.id})
        response = self.client.get(reverse('like_post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.like_set.count(), 0)

    def test_search_view_no_results(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('search'), {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No results found')

    def test_signout_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin')

    # More additional tests
    def test_signup_view_password_mismatch(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_signup_view_username_taken(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username Taken')

    def test_signup_view_email_taken(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'testuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email Taken')

    def test_profile_view_no_posts(self):
        self.client.login(username='testuser', password='testpassword')
        Post.objects.all().delete()
        response = self.client.get(reverse('profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts yet')

    def test_settings_view_invalid_role(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('settings'), {
            'role': 'invalidrole',
            'bio': 'Updated Bio',
            'location': 'Updated Location',
            'profileimg': None
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid role')

    def test_add_pets_view_missing_fields(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_pets'), {
            'name': '',
            'breed': 'New Breed',
            'age': 2,
            'bio': 'New Bio',
            'location': 'New Location',
            'profileimg': None
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Pet.objects.filter(breed='New Breed').exists())

    def test_post_view_no_image(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post'), {
            'caption': 'New Post'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Both image and caption are required')

    def test_like_post_view_invalid_post_id(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('like_post'), {'post_id': 999})
        self.assertEqual(response.status_code, 404)

    def test_search_view_empty_query(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No results found')

    def test_signout_view_post_method(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signin')
        