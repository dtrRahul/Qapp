from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('services', views.services,name="services"),
    path('index/', views.index, name="index"),
    path('appointment/', views.appointment, name="appointment"),
    path('saloons', views.saloons, name="saloons"),
    path('contact', views.contact,name="contact"),
    path('adduser/', views.booking, name="adduser"),
    path('whatsapp/', views.whatsapp, name="whatsapp"),
    path('sms/', views.sms, name='sms'),
    path('check_username_exist/', views.check_username_exist, name='check_username_exist'),
    path('check_email_exist/', views.check_email_exist, name='check_email_exist'),
    # path('fb_chat/', views.fb_chat, name='fb_chat'),
    path('admi/', views.admin,name="administrator"),
    path('login/', views.login, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path('user_data/', views.user_data, name="userdata"),
    path('user/<uid>/', views.user, name='user'),
    path('delete_customer/<int:pid>/', views.delete_customer, name='delete_customer'),
    path('delete/<int:id>', views.destroy),
    path('reschedule/<uid>', views.reschedule, name="reschedule"),
    path('rescheduled/<uid>', views.rescheduled_user, name="rescheduled"),

]


