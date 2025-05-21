from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView

class GetCSRFToken(APIView):
    """View to get a CSRF token"""
    def get(self, request):
        # Get the CSRF token for the current session
        token = get_token(request)
        return Response({'csrfToken': token})