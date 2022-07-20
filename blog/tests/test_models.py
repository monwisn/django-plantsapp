from django.test import TestCase
from django.template.defaultfilters import slugify
from blog.models import Post


class ModelsTestCase(TestCase):
    def test_post_has_slug(self):
        """Posts are given slugs correctly when saving"""
        post = Post.objects.create(title='Next post')
        post.author = 'test_user010'
        post.save()

        self.assertEqual(post.slug, slugify(post.title))
