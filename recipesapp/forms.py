from django import forms
from django.contrib.auth.password_validation import CommonPasswordValidator

from .models import Recipe, Category

class CategoryFilterForm(forms.Form):
    categories = Category.objects.all()
    category_choices = [('', 'Выберите категорию')] + [(category.id, category.name) for category in categories]
    category = forms.ChoiceField(choices=category_choices, required=False)


class RegisterForm(forms.Form):
    login_ = forms.CharField(max_length=50, label='Логин',
                            widget=forms.TextInput(attrs={'required': 'True'}))
    first_name = forms.CharField(max_length=50, label='Имя',
                            widget=forms.TextInput(attrs={'required': 'True'}))
    last_name = forms.CharField(max_length=50, label='Фамилия',
                            widget=forms.TextInput(attrs={'required': 'True'}))
    password = forms.CharField(max_length=50, label='Пароль',
                               widget=forms.PasswordInput(attrs={'required': 'True'}))
    confirm_password = forms.CharField(max_length=50, label='Подтверждение пароля',
                                       widget=forms.PasswordInput(attrs={'required': 'True'}))
    email = forms.EmailField(label='email')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают. Попробуйте еще раз.")

        return cleaned_data


class RecipeForm(forms.ModelForm):
    image = forms.ImageField(label='Загрузить изображение')
    cook_time = forms.IntegerField(label='Время готовки, мин.')

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cook_steps', 'ingredients', 'cook_time', 'image', 'category', 'complexity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'cook_steps': forms.Textarea(attrs={'rows': 6}),
            'ingredients': forms.Textarea(attrs={'rows': 6}),
            'category': forms.Select(choices=Category.objects.all()),
            'complexity': forms.Select(choices=[('easy', 'Легко'), ('middle', 'Среднее'), ('hard', 'Трудно')])
        }

        labels = {
            'name': 'Название',
            'description': 'Описание',
            'cook_steps': 'Этапы приготовления',
            'ingredients': 'Ингредиенты',
            'complexity': 'Сложность приготовления',
            'category': 'Категория',
        }