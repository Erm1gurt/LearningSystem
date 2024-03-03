from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from django.urls import reverse


# Create your models here.

class User(AbstractUser):
    class Status(models.IntegerChoices):
        STUDENT = 0, 'Студент'
        TEACHER = 1, 'Преподаватель'

    is_teacher = models.BooleanField(choices=Status.choices, default=Status.STUDENT)
    groups = models.ManyToManyField('Groups', blank=True)

    def create_user(self, username, password1, email, first_name, last_name, is_teacher, *args, **kwargs):
        self.username = username
        self.set_password(password1)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_teacher = is_teacher
        self.date_joined = datetime.now()
        self.save()\


class Courses(models.Model):
    class Status(models.IntegerChoices):
        Free = 0, 'Свободный доступ'
        Payment = 1, 'C оплатой'

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    slug = models.SlugField(default=None, unique=True, db_index=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_start = models.DateTimeField(default=None)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Автор не указан')
    price = models.BooleanField(choices=Status.choices, default=Status.Free)
    min_students = models.IntegerField(blank=True, default=1)
    max_students = models.IntegerField(default=30)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', kwargs={'course_slug': self.slug})

    def get_price(self):
        return Courses.Status.labels[self.price]



class Lessons(models.Model):
    lesson_num = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video = models.URLField(default=None)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Автор не указан')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['lesson_num']
        indexes = [
            models.Index(fields=['lesson_num'])
        ]


class Groups(models.Model):
    title = models.CharField(blank=True, max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.PROTECT)
    max_students = models.IntegerField(default=30)
    min_students = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-title']
        indexes = [
            models.Index(fields=['-title'])
        ]


class Customers(models.Model):
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    phone_number = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=True)
    course = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def create_customer(self, first_name, last_name, phone_number, email, course, user):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.course = course
        self.user = user
        self.save()

    def get_absolute_url(self):
        return reverse('customers', kwargs={'user_id': self.user_id})

