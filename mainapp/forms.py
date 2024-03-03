from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Lessons, Courses


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_teacher']
        labels = {
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'is_teacher': 'Род деятельности'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такая электронная почта уже занята')
        return email


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ['lesson_num', 'title', 'content', 'video']
        labels = {
            'lesson_num': 'Номер урока',
            'title': 'Название урока',
            'content': 'Лекционный материал',
            'video': 'Ссылка на запись урока',
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['slug', 'title', 'content', 'time_start', 'price', 'min_students', 'max_students']
        labels = {
            'slug': 'URL',
            'title': 'Название курса',
            'content': 'Описание курса',
            'time_start': 'Дата начала обучения',
            'price': 'Стоимость курса',
            'min_students': 'Минимальное кол-во студентов в группе',
            'max_students': 'Максимальное кол-во студентов в группе',
        }
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }


class JoinCourseForm(forms.Form):
    phone_number = forms.RegexField(
        label='укажите свой номер телефона, мы с вами свяжемся',
        regex=r'^\+?\d{11}$',
        error_messages={
        'required': "Номер телефона должен быть в формате: '+79999999999' или '89999999999'"
    })


class AddUserGroup(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['groups']
        labels = {'groups': 'Группы'}


