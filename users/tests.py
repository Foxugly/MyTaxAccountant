from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile
from django.conf import settings


class UserTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='john', email='jlennon@beatles.com', password='glass onion')
        userprofile1 = UserProfile.objects.create(user=user1, language=settings.LANGUAGES[0])
        user2 = User.objects.create_user(username='paul', email='pmccartney@beatles.com', password='blackburn')
        userprofile2 = UserProfile.objects.create(user=user2, language=settings.LANGUAGES[0])

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        john = User.objects.get(username='john')
        paul = User.objects.get(username="paul")
        self.assertEqual(john.email, 'jlennon@beatles.com')
        self.assertEqual(paul.email, 'pmccartney@beatles.com')
