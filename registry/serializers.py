from rest_framework import serializers
from .models import PublicProject


class PublicProjectSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='registered_by.country', read_only=True)
    instance_name = serializers.CharField(source='registered_by.name', read_only=True)
    
    class Meta:
        model = PublicProject
        fields = [
            "project_code",
            "title",
            "description",
            "instance_url",
            "remote_project_id",
            "country",
            "instance_name",
        ]
        read_only_fields = ["project_code"]