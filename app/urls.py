from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('gallery', gallery, name='gallery'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('instructor', instructor, name='instructor'),
    path('registerSuccess', registerSuccess, name='registerSuccess'),
    path('contactSuccess', contactSuccess, name='contactSuccess'),
    re_path(r'^courseDetail/(?P<id>[0-9]+)', courseDetail, name='courseDetail'),
    path('standAlone', standAlone, name='standAlone'),
    path('freeCourse', freeCourse, name='freeCourse'),
    path('investor', investor, name='investor'),
    path('logout',LogoutView.as_view(next_page='/'),name='logout'),
    path('forgotPassword', forgotPassword, name='forgotPassword'),
    path('resetPassword/<token>/', resetPassword, name='resetPassword'),
    path('Success', Success,name="Success"),
    path('contact', contact,name="contact"),
    path('sendForgotpass', sendForgotpass, name='sendForgotpass'),
    path('invalidLink', invalidLink, name='invalidLink'),
    path('changePassword', changePassword, name='changePassword'),
]