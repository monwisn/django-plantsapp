from django.test import TestCase

from authentication.models import User
from galleries.models import Gallery, Status


class TestAppModels(TestCase):

    def test_model_str(self):
        user = User.objects.create_user(
            username="myusername",
            password="mypassword",
            email="abc@testmail.com"
        )
        self.client.user = user

        title = Gallery.objects.create(
            title="Title Testing",
            description='Test',
            author=user,
            status=Status.PUBLISHED,
            slug='Title-Testing'
        )
        self.assertEqual(str(title), 'Title Testing')

