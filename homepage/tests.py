from django.test import TestCase, Client
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
        self.input = {'post_tittle': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                      'post_content': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<script>alert("Hello");</script>\n\n this is for test'}

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

    def test_tittle_greater_than_body(self):
        form = Blog({'post_tittle': 'length of title greater than length of body', 'post_content': 'less than tittle'})
        self.assertFalse(form.is_valid())

    def test_tittle_less_than_body(self):
        form = Blog({'post_tittle': 'length of tittle',
                     'post_content': 'less than tittle.now content is graeter than the length of the body'})
        self.assertTrue(form.is_valid())

    def test_char_len_less_than_10(self):
        form = Blog({'post_tittle': 'leng', 'post_content': 'less th'})
        self.assertFalse(form.is_valid())



class Editlink(TestCase):


    def setUp(self):
        self.post = Post.objects.create(post_tittle='testing purpose',
                                        post_date=timezone.now(),
                                        post_content='this is for testing \n\n purpose fo edit link',
                                        post_key='123456789')
        self.post.save()
        self.wrong_key = 'kwoppokdk'

    def test_edit_linK(self):
        response = self.client.get(reverse('homepage:edit',
                                           kwargs={'id': self.post.id, 'skey': self.post.post_key}))
        self.assertContains(response, 'testing purpose', status_code=200)
        wrong_response = self.client.get(reverse('homepage:edit', kwargs={'id': self.post.id, 'skey': self.wrong_key}))
        self.assertEqual(wrong_response.status_code, 404)

    def test_post(self):
        edit_input = {'post_tittle': 'length of tittle',
                      'post_content': 'less than tittle.now content is graeter than the length of the body'}
        response = self.client.post(reverse('homepage:edit', kwargs={'id': self.post.id, 'skey': self.post.post_key}),
                                    edit_input)
        self.assertRedirects(response, reverse('homepage:post', kwargs={'id': self.post.id}), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        wrong_response = self.client.post(reverse('homepage:edit', kwargs={'id': self.post.id, 'skey': self.wrong_key}))
        self.assertEqual(wrong_response.status_code, 404)

class Rendering(TestCase):

    def setUp(self):
        self.input = {'post_tittle': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                      'post_content': 'this tag will not render<a>\n\nthis is for test'}

        self.input1 = {'post_tittle': 'aaaaaaaaaaa', 'post_content': '<h1>will</h1><h2>hi</h2>'}


    def test_multiple_para_rendering_and_NO_unsafe_tags(self):
        response = self.client.post(reverse('homepage:create'), self.input, follow=True)
        self.assertContains(response, '<p>this tag will not render&lt;a&gt;</p>', status_code=200)

    def test_TOC(self):
        response = self.client.post(reverse('homepage:create'), self.input1, follow=True)
        self.assertContains(response, '<ul><li>will</li></ul><ul><ul><li>hi</li></ul></ul>', status_code=200)