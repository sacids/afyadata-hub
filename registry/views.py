from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django.db.models import Q

from .models import PublicProject
from .serializers import PublicProjectSerializer
from .permissions import HasValidInstanceKey


class ProjectDiscoveryView(APIView):
    """
    Manual APIView for Mobile App discovery.
    Provides explicit control over searching and filtering.
    """

    def get(self, request):
        # 1. Start with active projects
        projects = PublicProject.objects.filter(is_active=True).order_by("-created_at")

        # 2. Handle search query manually if present
        search_query = request.query_params.get("search", None)
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(project_code__icontains=search_query)
                | Q(registered_by__country__icontains=search_query)
                | Q(registered_by__name__icontains=search_query)
            )

        # 3. Handle country filter if present
        country_filter = request.query_params.get("country", None)
        if country_filter:
            projects = projects.filter(
                registered_by__country__iexact=country_filter
            )

        # 4. Serialize and Return
        serializer = PublicProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class RegisterProjectView(APIView):
    """
    Explicit APIView for Instance Servers to register projects.
    Uses our custom permission class for API Key authentication.
    """
    
    permission_classes = [HasValidInstanceKey]
    
    def post(self, request):
        serializer = PublicProjectSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            remote_project_id = validated_data.pop('remote_project_id')
            instance = request.instance_auth
            
            # Remove source fields from validated_data if present to avoid conflicts
            validated_data.pop('registered_by', None)
            
            # Update or create based on remote_project_id AND registered_by
            # This ensures if a project is updated, we still get the instance back
            project, created = PublicProject.objects.update_or_create(
                remote_project_id=remote_project_id,
                registered_by=instance,
                defaults=validated_data
            )
            
            # Use the serializer to turn the model instance into JSON
            response_serializer = PublicProjectSerializer(project)
            
            # Set status code: 201 for new, 200 for updated
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            
            # This returns the full JSON representation of the PublicProject
            return Response(response_serializer.data, status=status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)