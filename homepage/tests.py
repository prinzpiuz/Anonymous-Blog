from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, User
from . import forms
from .forms import Blog
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.models import User

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
                      'post_content': 'this tag will not render<a></a>\n\nthis is for test'}

        self.input1 = {'post_tittle': 'aaaaaaaaaaa', 'post_content': '<h1>will</h1><h2>hi</h2>'}

    def test_multiple_para_rendering_and_NO_unsafe_tags(self):
        response = self.client.post(reverse('homepage:create'), self.input, follow=True)
        self.assertContains(response, '<p>this tag will not render&lt;a&gt;&lt;/a&gt;</p>\n\n<p>this is for test</p>',
                            status_code=200)

    def test_TOC(self):
        response = self.client.post(reverse('homepage:create'), self.input1, follow=True)
        self.assertContains(response, '<ul><li>will</li></ul><ul><ul><li>hi</li></ul></ul>', status_code=200)


class LogInTest(TestCase):
    def setUp(self):
        self.input = {
            'username': 'testuser',
            'password': 'secret'}
        self.duplicate = {
            'username': 'testuser',
            'password1': 'secret',
            'password2': 'secret'}
        self.reg = {
            'username': 'testuser1',
            'password1': 'secret.811',
            'password2': 'secret.811'}
        self.input2 = {
            'username': 'testuser3',
            'password': 'secret'}
        self.post = {'post_tittle': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                      'post_content': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<script>alert("Hello");</script>\n\n this is for test'}
        User.objects.create_user(**self.input)

    def test_login(self):
        response = self.client.post(reverse('homepage:login'), self.input, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_with_wrong_credentials(self):
        response = self.client.post(reverse('homepage:login'), self.input2, follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_logout(self):
        self.client.post(reverse('homepage:login'), self.input, follow=True)
        responce = self.client.get(reverse('homepage:logout'))
        self.assertRedirects(responce, reverse('homepage:login'), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_register(self):
        responce = self.client.post(reverse('homepage:register'), self.reg, follow=True)
        self.assertEqual(User.objects.count(), 2)
        self.assertRedirects(responce, reverse('homepage:login'), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(responce.context['user'].is_active)

    # # this will test for uniqness of username if tried to login with same username again page dont redirect
    def test_for_unique_username(self):
        responce = self.client.post(reverse('homepage:register'),self.duplicate, follow=True)

        self.assertContains(responce,'A user with that username already exists.',status_code=200)


    def test_post_creation_of_logged_user(self):
        responce = self.client.post(reverse('homepage:login'), self.input, follow=True)
        response = self.client.post(reverse('homepage:create'), self.post)
        instance = Post.objects.get()
        self.assertRedirects(response, reverse('homepage:post', kwargs={'id': instance.id}), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertTrue(responce.context['user'].is_active)


