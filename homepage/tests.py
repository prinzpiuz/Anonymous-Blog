from django.test import TestCase,Client
from django.urls import reverse
from .models import Post
from . import forms
from .forms import Blog
from django.utils.crypto import get_random_string
from django.utils import timezone


# Create your tests here.
class viewTestCases(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.input = {'post_tittle': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'post_content': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}

    def test_redirect(self):
        response = self.client.post(reverse('homepage:create'), self.input)
        instance = Post.objects.get()

        self.assertRedirects(response, reverse('homepage:post', kwargs={'id': instance.id}), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
    def test_valid_form(self):
        form = Blog({'post_date': timezone.now(), 'post_key': get_random_string(length=9)}, self.input)
        self.assertTrue(form.is_valid())
        submit = form.save()
        self.assertEqual(submit.post_tittle, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.assertEqual(submit.post_content, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
