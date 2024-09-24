from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile, Pet, Vet, Post, Like, Message

User = get_user_model()

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, location='Test Location')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.location, 'Test Location')
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_bio_blank(self):
        self.assertEqual(self.profile.bio, '')

    def test_profile_default_role(self):
        self.assertEqual(self.profile.role, 'owner')


class PetModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, location='Test Location')
        self.pet = Pet.objects.create(owner=self.profile, name='Buddy', breed='Golden Retriever', age='2', location='Test Location')

    def test_pet_creation(self):
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.breed, 'Golden Retriever')
        self.assertEqual(str(self.pet), 'Buddy (Golden Retriever) - testuser')

    def test_pet_default_sex(self):
        self.assertEqual(self.pet.sex, 'Unknown')

    def test_pet_bio_blank(self):
        self.assertEqual(self.pet.bio, '')


class VetModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testvet', password='12345')
        self.profile = Profile.objects.create(user=self.user, location='Test Location', role='vet')
        self.vet = Vet.objects.create(profile=self.profile, clinic_name='Test Clinic', specialty='Surgery', years_of_experience=5)

    def test_vet_creation(self):
        self.assertEqual(self.vet.clinic_name, 'Test Clinic')
        self.assertEqual(self.vet.specialty, 'Surgery')
        self.assertEqual(self.vet.years_of_experience, 5)
        self.assertEqual(str(self.vet), 'testvet')

    def test_vet_contact_info_blank(self):
        self.assertEqual(self.vet.contact_info, '')


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(user=self.user, caption='Test Caption')

    def test_post_creation(self):
        self.assertEqual(self.post.caption, 'Test Caption')
        self.assertEqual(self.post.no_of_likes, 0)
        self.assertEqual(str(self.post), 'testuser')

    def test_post_default_no_of_likes(self):
        self.assertEqual(self.post.no_of_likes, 0)

    def test_post_created_at(self):
        self.assertIsNotNone(self.post.created_at)


class LikeModelTest(TestCase):

    def setUp(self):
        self.like = Like.objects.create(post_id='12345', username='testuser')

    def test_like_creation(self):
        self.assertEqual(self.like.post_id, '12345')
        self.assertEqual(self.like.username, 'testuser')
        self.assertEqual(str(self.like), 'testuser')


class MessageModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='sender', password='12345')
        self.user2 = User.objects.create_user(username='receiver', password='12345')
        self.profile1 = Profile.objects.create(user=self.user1, location='Test Location')
        self.profile2 = Profile.objects.create(user=self.user2, location='Test Location')
        self.message = Message.objects.create(sender=self.profile1, receiver=self.profile2, content='Test Message')

    def test_message_creation(self):
        self.assertEqual(self.message.content, 'Test Message')
        self.assertEqual(self.message.is_read, False)
        self.assertEqual(str(self.message), f"Message from sender to receiver at {self.message.timestamp}")

    def test_message_default_is_read(self):
        self.assertFalse(self.message.is_read)

    def test_message_timestamp(self):
        self.assertIsNotNone(self.message.timestamp)