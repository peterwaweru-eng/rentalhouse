# rentals/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [

                  path('', views.index, name="index"),
                  path('index/', views.index, name="index"),
                  path('advt_form/', views.advt_form, name="advt_form"),
                  path('copy_advt_form/', views.copy_advt_form, name="rent_in"),
                  path('show_house/', views.show_house, name="show_house"),
                  path('register/', views.register, name="register"),
                  path('user_login/', views.user_login, name="user_login"),
                  path('logout/', views.user_logout, name="logout"),
                  path('rating_analysis', views.rating_analysis, name="rating_analysis"),
                  path('register/', views.register, name='register'),
                  path('logout/', views.user_logout, name='logout'),
                  path('special/', views.special, name='special'),





]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
