from rest_framework import serializers
from .models import StudentProfiles,FacultyProfiles

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfiles
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyProfiles
        fields = '__all__'
        