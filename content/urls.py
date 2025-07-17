from django.urls import path, include

from content import views


urlpatterns = [

    path('',views.homepage),
    path('profile/<slug:slug>',views.profilepage),
    path('post/<slug:slug>',views.postpage),
    path('search',views.search),
    path('login/',views.loginpage),
    path('signup',views.handleSignup),
    path('loginhandle',views.handlelogin),
    path('logout',views.handlelogout),
    path('edit-profile',views.editprofile),
    path('postComment', views.postComment),
    path('like/<slug:slug>/', views.like_post, ),
    path('createpost/', views.create_post, ),
    path('follow/<str:username>/', views.follow_user,),


]
