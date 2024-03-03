import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from .models import Courses, Lessons
from .forms import LoginUserForm, RegisterUserForm, CreateLessonForm, CreateCourseForm, JoinCourseForm, AddUserGroup
from .models import User, Groups, Customers


# Create your views here.

def homepage(request):
    context = {'page': request.path, 'user': request.user}
    return render(request, 'homepage.html', context)


@login_required
def course(request, course_slug=None, lesson_id=None):
    courses, lessons, lesson, join_move = None, None, None, None
    courses_list = Courses.objects.all()

    if course_slug:
        courses = get_object_or_404(Courses, slug=course_slug)

        pattern = request.user.id != courses.author_id and courses.pk not in map(lambda x: x.course_id,
                                                                                 request.user.groups.all())

        if not pattern:
            lessons = courses.lessons_set.all()
        else:
            join_move = True

        if lesson_id:
            if pattern:
                return Http404
            lesson = get_object_or_404(Lessons, lesson_num=lesson_id, course_id=courses.pk)

    context = {
        'page': '/course',
        'user': request.user,
        'courses_li': courses_list,
        'courses': courses,
        'lessons': lessons,
        'lesson': lesson,
        'join': join_move
    }

    return render(request, 'course.html', context)


@login_required
def create_lesson(request, course_slug):
    courses = get_object_or_404(Courses, slug=course_slug)
    form = CreateLessonForm()

    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            data.course_id = courses.pk
            data.save()
            return redirect(courses.get_absolute_url())

    context = {
        'page': '/course',
        'user': request.user,
        'courses': courses,
        'create': True,
        'form': form
    }
    return render(request, 'course.html', context)


def join_course(request, course_slug):
    courses = get_object_or_404(Courses, slug=course_slug)
    form = None



    if request.method == 'POST':
        form = JoinCourseForm(request.POST)
        if form.is_valid():
            customer = Customers()
            customer.create_customer(request.user.first_name, request.user.last_name, form.cleaned_data['phone_number'],
                                     request.user.email, courses, request.user)
            return HttpResponse(
                '<p>Заявка отправлена, менеджер с вами свяжется в ближайшее время</p><a href="../../home">На главную</a>')
    elif courses.price:
        form = JoinCourseForm()
    else:
        group = Groups.objects.filter(course=courses)[0]
        if group.max_students != group.min_students:
            pass
            group.max_students -= 1
            group.save()
        else:
            group_num = int(re.search('\d*$', group.title).group())
            group = Groups()
            group.title = f'{courses.slug}{group_num + 1}'
            group.min_students = courses.min_students
            group.max_students = courses.max_students - 1
            group.course = courses
            group.save()

        request.user.groups.add(group)

    context = {
        'title': f'Присоедениться к курсу: {courses.title}',
        'page': '/course',
        'user': request.user,
        'courses': courses,
        'form': form
    }
    return render(request, 'join.html', context)


def add_course(request):
    form = CreateCourseForm()
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            cd = form.cleaned_data
            group = Groups()
            group.title = f"{cd['slug']}1"
            group.max_students = cd['max_students']
            group.min_students = cd['min_students']
            data.author = request.user
            data.save()
            group.course_id = data.id
            group.save()
            return redirect('course')

    context = {
        'page': request.path,
        'user': request.user,
        'form': form
    }
    return render(request, 'add_course.html', context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация', 'page': '/login'}

    def get_success_url(self):
        return reverse('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    extra_context = {'title': 'Регистрация', 'page': '/register'}

    def get_success_url(self):
        return reverse('login')


def logout_user(request):
    logout(request)
    return redirect('login')


def customers(request, user_id=None):
    user, form = None, None
    if user_id:
        user = User.objects.get(pk=user_id)
        form = AddUserGroup()

        if request.method == 'POST':
            form = AddUserGroup(request.POST)
            if form.is_valid():
                form.save()


    customer = Customers.objects.all()
    context = {
        'title': 'Клиенты',
        'page': request.path,
        'user': request.user,
        'customers': customer,
        'user_info': user,
        'form': form
    }
    return render(request, 'customers.html', context)