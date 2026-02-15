from django.contrib import admin
from .models import StudentProfiles, Course, Enrollment
# Register your models here.


admin.site.register(StudentProfiles)
admin.site.register(Course)
admin.site.register(Enrollment)
