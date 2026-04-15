from rest_framework import serializers
from .models import PublicProject


class PublicProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicProject
        fields = [
            "project_code",
            "title",
            "description",
            "instance_url",
            "remote_project_id",
        ]
        read_only_fields = ["project_code"]
