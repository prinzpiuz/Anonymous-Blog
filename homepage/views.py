from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from . import forms
from .models import Post
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string
from bs4 import BeautifulSoup


def post(request, id):
    p = get_object_or_404(Post, id=id)
    text = ''
    url = reverse('homepage:loginedit', kwargs={'id': p.id})
    q = p.post_content
    soup = BeautifulSoup(q)
    s = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for item in s:
        i = int(str(item)[2])
        text += i * '<ul>' + '<li>' + item.text + '</li>' + '</ul>' * i

    return render(request, 'homepage/post.html', {'post': p, 'table_of_contents': text, 'url': url})


class Create(View):
    def get(self, request):
        form = forms.Blog()
        return render(request, 'homepage/home.html', {'form': form})

    def post(self, request):
        form = forms.Blog(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.post_date = timezone.now()
            q.post_key = get_random_string(length=9)

            if request.user.is_authenticated:
                q.post_author = request.user
                q.save()
                return redirect('homepage:post', id=q.id)
            else:
                q.save()
                url = reverse('homepage:edit', kwargs={'id': q.id, 'skey': q.post_key})
                messages.success(request, mark_safe("<a href='{url}'>{url}</a>".format(url=url)))
                return redirect('homepage:post', id=q.id)
        return render(request, 'homepage/home.html', {'form': form})


class LogedInUserEdit(View):
    def get(self, request, id):
        author = request.user
        post = get_object_or_404(Post, id=id, post_author=author)
        form = forms.Blog(instance=post)
        return render(request, 'homepage/home.html', {'form': form, 'post': post})

    def post(self, request, id):
        author = request.user
        pos = get_object_or_404(Post, id=id, post_author=author)
        form = forms.Blog(request.POST, instance=pos)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return redirect('homepage:post', id=instance.id)
        return render(request, 'homepage/home.html', {'form': form, 'post': pos})


class Edit(View):

    def get(self, request, id, skey):
        post = get_object_or_404(Post, id=id, post_key=skey)
        form = forms.Blog(instance=post)
        if request.user.is_authenticated and post.post_author == None:
            url = reverse('homepage:claim', kwargs={'id': post.id})
            return render(request, 'homepage/claim.html', {'form': form, 'post': post, 'url': url})
        else:
            return render(request, 'homepage/home.html', {'form': form, 'post': post})

    def post(self, request, id, skey):
        pos = get_object_or_404(Post, id=id, post_key=skey)
        form = forms.Blog(request.POST, instance=pos)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return redirect('homepage:post', id=instance.id)
        return render(request, 'homepage/home.html', {'form': form, 'post': pos})


def claim(request, id):
    user = request.user
    pos = Post.objects.get(id=id)
    pos.post_author = user
    pos.save()
    return redirect('homepage:post', id=id)


class Mine(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            w = Post.objects.filter(post_author=user)
            data = {
                "posts": w
            }
            return render(request, 'homepage/mine.html', data)


class Posts(View):
    def get(self, request):
        q = Post.objects.all()
        hi = {
            "posts": q
        }
        return render(request, 'homepage/posts.html', hi)


class Register(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'homepage/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage:login')
        return render(request, 'homepage/register.html', {'form': form})


class LoginUser(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'homepage/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage:create')
        return render(request, 'homepage/login.html', {'form': form})


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('homepage:login')
