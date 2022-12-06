from django.test import TestCase
from django.template.defaultfilters import slugify
# from model_bakery import baker  # fixture for testing
# from pprint import pprint

from authentication.models import User
from blog.models import Post, Category


class ModelsTestCase(TestCase):

    # # autogenerate data with bakery:
    # def setUp(self):
    #     self.post = baker.make('blog.Post')
    #     pprint(self.post.__dict__)

    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase"""

        user = User.objects.create_user(username="myusername", password="mypassword", email="abc@testmail.com")
        user2 = User.objects.create_user(username="myusername2", password="mypassword2", email="abcd@testmail.com")

        cls.category = Category.objects.create(
            title='test category',
            description='test',
            slug='test-category',
        )

        cls.post = Post.objects.create(
            title='Next post',
            description='Test post',
            author=user,
            place='Test place',
            category=cls.category,
            status='Draft',
        )

        cls.post.save()
        cls.post.likes.set([user.pk, user2.pk])
        cls.post.save()

    def test_post_likes(self):
        self.assertEqual(self.post.likes.count(), 2)

    def test_post_has_slug(self):
        self.assertEqual(self.post.slug, slugify(self.post.title))


    # def test_post_has_slug_and_post_likes(self):
    #     """Posts are given slugs correctly when saving"""
    #
    #     user = User.objects.create_user(
    #         username="myusername",
    #         password="mypassword",
    #         email="abc@testmail.com"
    #     )
    #     self.client.user = user
    #
    #     user2 = User.objects.create_user(
    #         username="myusername2",
    #         password="mypassword2",
    #         email="abcd@testmail.com"
    #     )
    #     self.client.user = user2
    #
    #     category = Category.objects.create(title='test category', description='test', slug='test-category')
    #
    #     post = Post.objects.create(title='Next post',
    #                                description='Test post',
    #                                author=user2,
    #                                place='Test place',
    #                                category=category,
    #                                status='Draft',
    #                                )
    #     post.save()
    #     post.likes.set([user.pk, user2.pk])
    #     post.save()
    #
    #     self.assertEqual(post.slug, slugify(post.title))
    #     self.assertEqual(post.likes.count(), 2)


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        Category.objects.create(title='Test', description='test category model')

    def test_title_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_description_label_fail(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Description')

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_title_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_title_max_length_fail(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_description_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('description').max_length
        self.assertEqual(max_length, 300)

    def test_slug_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(category.get_absolute_url(), '/blog/category-detail/1')

    def test_get_absolute_url_fail(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), '/blog/category_detail/1')

