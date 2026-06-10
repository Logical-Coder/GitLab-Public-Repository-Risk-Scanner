from rest_framework.views import APIView
from rest_framework.response import Response

from scanner.serializers import ScanSerializer
from gitlab.services.gitlab_service import GitLabService

from scanner.services.scan_service import (
    ScanService
)
class ScanView(APIView):

    def get(self, request):

        service = GitLabService()

        projects = service.get_user_projects(
            "gitlab-org"
        )

        print("Projects:", projects)

        return Response(projects)

    def post(self, request):

        serializer = ScanSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        target_type = serializer.validated_data[
            "target_type"
        ]

        target_name = serializer.validated_data[
            "target_name"
        ]

        scan_service = ScanService()

        result = scan_service.execute_scan(
            target_type,
            target_name
        )

        return Response(result)

class HealthView(APIView):

    def get(self, request):

        return Response(
            {
                "status": "UP"
            }
        )