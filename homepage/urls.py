from django.urls import path
from homepage.views import Create, post, Edit, Posts, Register, LoginUser, LogOut, Mine, LogedInUserEdit

app_name = 'homepage'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('', Create.as_view(), name='create'),
    path('post/<id>/', post, name='post'),
    path('<id>/edit/', LogedInUserEdit.as_view(), name='loginedit'),
    path('<id>/edit/<skey>', Edit.as_view(), name='edit'),
    path('posts/', Posts.as_view(), name='posts'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('mine/', Mine.as_view(), name='mine')

]
