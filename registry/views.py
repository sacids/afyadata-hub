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
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(project_code__icontains=search_query)
            )

        # 3. Serialize and Return
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
            # Save while linking to the instance identified by the API Key
            # request.instance_auth was set by our HasValidInstanceKey permission
            serializer.save(registered_by=request.instance_auth)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
