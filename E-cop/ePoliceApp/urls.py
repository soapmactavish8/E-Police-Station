from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('logout/', logout, name='logout'),

    # REGISTER PAGE AND FUNCTIONALITY
    path('register_page/', register_page, name='register_page'),
    path('register/', register, name='register'),

    # LOGIN PAGE AND FUNCTIONALITY
    path('login_page/', login_page, name='login_page'),
    path('login/', login, name='login'),

    # FORGOT PASSWORD PAGE AND FUNCTIONALITY
    path('forgot_pass_page/', forgot_pass_page, name='forgot_pass_page'),
    path('forgot_pass/', forgot_pass, name='forgot_pass'),

    # SEND OTP, OTP PAGE, VERIFIY OTP AND FUNCTIOALITY
    path('otp_page/', otp_page, name='otp_page'), 
    #path('verify_otp/', verify_otp, name='verify_otp'),
    path('verify_otp/<str:verify_for>/',verify_otp, name='otp_verify'),
    
    # PROFILE PAGE AND UPDATE FUNCTIOALITY
    path('profile_page/', profile_page, name='profile_page'), 
    path('profile_update/', profile_update, name='profile_update'),
    path('change_password/', change_password, name='change_password'),

    # DEPARTMENT FUNCTIONS
    path('add_station/', add_station, name='add_station'),
    path('remove_station/<int:pk>/', remove_station, name='remove_station'),


    # SUSPECT DETAILS
    path('create_suspect_list/', create_suspect_list, name='create_suspect_list'),
    path('petcaretaker_content/', petcaretaker_content, name='petcaretaker_content'),
    path('remove_suspect_detail/<int:pk>/', remove_suspect_detail, name='remove_suspect_detail'),
    
  

]