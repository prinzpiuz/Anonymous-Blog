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
        form = Blog(self.input)
        self.assertTrue(form.is_valid())

    def test_non_valid_form(self):
        form = Blog()
        self.assertFalse(form.is_valid())
    def test_tittle_gt_body(self):
        form = Blog({'post_tittle':'length of title greater than length of body','post_content':'less than tittle'})
        self.assertFalse(form.is_valid())
    def test_tittle_ls_body(self):
        form = Blog({'post_tittle':'length of tittle','post_content':'less than tittle.now content is graeter than the length of the body'})
        self.assertTrue(form.is_valid())
    def test_char_len_lt_10(self):
        form = Blog({'post_tittle':'leng','post_content':'less th'})
        self.assertFalse(form.is_valid())
class Editlinl(TestCase):
    def setUp(self):
        self.post = Post.objects.create(post_tittle='testing purpose', post_date=timezone.now(),
                                        post_content='this is for testing purpose fo edit link', post_key='123456789')
        self.post.save()
        self.wkey = 'kwoppokdk'


    def test_edit_linK(self):
        response = self.client.get(reverse('homepage:edit',kwargs={'id': self.post.id, 'skey': self.post.post_key}))
        self.assertContains(response,'testing purpose',status_code=200)
        wresponse = self.client.get(reverse('homepage:edit', kwargs={'id': self.post.id, 'skey': self.wkey}))
        self.assertEqual(wresponse.status_code,404)

