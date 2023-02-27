from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for student"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'STUDENT':
        StudentProfile.objects.create(user=instance)


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.TEACHER)


class Teacher(User):
    base_role = User.Role.TEACHER
    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Teacher"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user


@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'TEACHER':
        TeacherProfile.objects.create(user=instance)