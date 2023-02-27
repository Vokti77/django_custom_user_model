from django.contrib import admin
from user.models import User, StudentProfile, TeacherProfile

admin.site.register(User)
# admin.site.register(Student)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)