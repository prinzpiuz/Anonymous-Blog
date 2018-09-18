from django.urls import path

from homepage.views import Create, post, Edit, Posts

app_name = 'homepage'

urlpatterns = [
    path('', Create.as_view(), name='create'),
    path('post/<id>/', post, name='post'),
    path('<id>/edit/<skey>', Edit.as_view(), name='edit'),
    path('posts/', Posts.as_view(), name='posts')
]
