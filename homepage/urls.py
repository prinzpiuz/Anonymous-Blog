from django.urls import path

from homepage.views import Create,posts,Edit
app_name='homepage'

urlpatterns = [
    path('',Create.as_view(),name='create'),
    path('post/<int:id>/',posts,name='posts'),
    path('<id>/edit/<skey>',Edit.as_view(),name='edit')
    ]
