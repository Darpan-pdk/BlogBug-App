
from django.urls import path,include
from . import views


urlpatterns = [
    #path('', views.test),
    path('', views.ulogin),
    path('signup/', views.signup),
    path('home/', views.home),
    path('newpost/', views.newpost),
    path('mypost/', views.mypost),
    path('signout/', views.signOut),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('accounts/', include('allauth.urls')),
    
    
]

