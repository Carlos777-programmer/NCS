from rest_framework import serializers
from .models import Project, QuoteSubmission

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class QuoteSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteSubmission
        fields = '__all__'