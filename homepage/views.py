from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views import View

from . import forms
from .models import Post

from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.crypto import get_random_string


def post(request, id):
    p = get_object_or_404(Post, id=id)
    return render(request, 'homepage/post.html', {'post': p})


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
            q.save()
            url = reverse('homepage:edit', kwargs={'id': q.id, 'skey': q.post_key})
            # print(url)
            messages.success(request, mark_safe("<a href='{url}'>{url}</a>".format(url=url)))
            return redirect('homepage:post', id=q.id)
        return render(request, 'homepage/home.html', {'form': form})


class Edit(View):

    def get(self, request, id, skey):
        post = get_object_or_404(Post, id=id, post_key=skey)
        form = forms.BlogEdit(instance=post)
        return render(request, 'homepage/home.html', {'form': form, 'post': post})

    def post(self, request, id, skey):
        pos = get_object_or_404(Post, id=id, post_key=skey)
        form = forms.BlogEdit(request.POST, instance=pos)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return redirect('homepage:post', id=instance.id)
        return render(request, 'homepage/home.html', {'form': form, 'post': pos})

class Posts(View):
    def get(self, request):
        q=Post.objects.all()
        hi = {
            "posts": q
        }
        return render(request, 'homepage/posts.html',hi)