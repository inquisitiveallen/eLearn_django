from django.shortcuts import redirect
from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='placeorder'),
    path(r'courses/<int:cour_id>/', views.coursedetail, name='course_detail'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myaccount/', views.myaccount, name='myaccount'),
    path(r'register/', views.register, name='register'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'myaccount//', lambda req: redirect('/myapp/myaccount/')),
    path(r'forgotPassword/', views.forgotPassword, name='forgotPassword'),
]
