from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.main_page, name='main_page'),
    path('recipe_add/', views.recipe_add, name='recipe_add'),
    path('recipe_show/<int:pk>', views.recipe_show, name='recipe_show'),
    path('recipes_all', views.all_recipes, name='recipe_all'),
    path('recipe_search/', views.recipe_search, name='recipe_search'),
]