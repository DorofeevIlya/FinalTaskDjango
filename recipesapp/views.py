import logging
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import RegisterForm, RecipeForm, CategoryFilterForm
from .models import Recipe

logger = logging.getLogger(__name__)


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Логин или пароль неверны')
            return render(request, 'recipesapp/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'recipesapp/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login_ = form.cleaned_data.get('login_')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')


            if not User.objects.filter(username=login_).exists():
                print(f'записываем в базу {login_} {password} {email}')
                user = User.objects.create_user(username=login_, email=email, password=password
                                                )
            else:
                messages.error(request, 'Пользователь с таким email уже существует. Выберите другой')
                return render(request, 'recipesapp/register.html', {'form': form})

            messages.success(request, 'Регистрация завершена успешно')
            return redirect('login')

        else:
            error_text = form.errors['__all__']
            messages.error(request, error_text)
            return render(request, 'recipesapp/register.html', {'form': form})

    else:
        form = RegisterForm()
    return render(request, 'recipesapp/register.html', {'form': form})


def main_page(request):
    user = request.user
    results_qty = 3
    latest_recipes = Recipe.objects.order_by('-created_at')[:results_qty]
    print(latest_recipes)
    context = {
        'title': 'Главная',
        'username': user.username,
        'latest_recipes': latest_recipes,
    }
    return render(request, 'recipesapp/main.html', context)


def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, f'Рецепт {recipe.id} добавлен')
            return redirect('recipe_add')
    else:
        form = RecipeForm()

    context = {
        'title': 'Добавить рецепт',
        'form': form,
    }

    if request.user.is_authenticated:
        return render(request, 'recipesapp/add_recipe.html', context)
    else:
        messages.success(request, 'Необходима авторизация')
        return redirect('login')


def recipe_show(request, pk):
    recipe_find = Recipe.objects.filter(id=pk).first()
    if recipe_find is None:
        messages.error(request, 'Рецепт не найден')
        return render(request, 'recipesapp/blank.html')
    else:
        ingredients_list = recipe_find.ingredients.split('\n')
        cook_steps_list = recipe_find.cook_steps.split('\n')
        complexity_list = recipe_find.complexity.split('\n')
        context = {
            'recipe': recipe_find,
            'ingredients_list': ingredients_list,
            'cook_steps_list': cook_steps_list,
            'complexity_list': complexity_list,

        }
        return render(request, 'recipesapp/recipe_show.html', context)


def all_recipes(request):
    user = request.user
    latest_recipes = Recipe.objects.all()
    print(latest_recipes)
    context = {
        'title': 'Все рецепты',
        'username': user.username,
        'latest_recipes': latest_recipes,
    }
    return render(request, 'recipesapp/recipe_all.html', context)


def recipe_search(request):
    if request.method == 'POST':
        form = CategoryFilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            if category == '':
                search_recipes = Recipe.objects.all()
            else:
                search_recipes = Recipe.objects.filter(category=category)
            context = {
                'title': 'Результаты поиска',
                'form': form,
                'find_recipes': search_recipes,
            }
    else:
        form = CategoryFilterForm()
        context = {
            'title': 'Поиск рецепта',
            'form': form,
        }

    return render(request, 'recipesapp/search_recipes.html', context)