from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name = "home"),
    path('books/', views.book_list, name='book_list'),
    path('users/',views.user_list,name = 'user_list'),
    path('register/',views.register,name = 'register'),
    path('login/',views.login,name = 'login'),
    path('user/home/',views.user_home,name='user_home'),
    path('logout/',views.logout,name = 'logout'),
    path('user/home/books/',views.browse_books,name = 'browse_books')
]