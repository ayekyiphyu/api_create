from django.http import JsonResponse
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from memos.models import Memo
from memos.serializers import MemoSerializer
from .serializers import RegisterSerializer, User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        user = None

        # usernameでログイン
        if username:
            user = authenticate(request, username=username, password=password)

        # emailでログイン
        if user is None and email:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "is_superuser": user.is_superuser,
                }
            })
        else:
            return Response({"error": "Incorrect credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class currentUserView(APIView):
    # Manually check authentication inside method
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                "is_superuser": user.is_superuser,
            })
        else:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class TestLoginView(View):
    def post(self, request):
        return JsonResponse({'message': 'CSRF exempt works'})


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    # Open to anyone, but check authentication manually inside method

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'status': 'success', 'message': 'Successfully logged out'})
        else:
            return Response({'status': 'error', 'message': 'Not logged in'}, status=400)


class AuthRootView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        user = request.user
        if user.is_authenticated:
            return Response({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'csrf_token': csrf_token,
            })
        else:
            return Response({
                'csrf_token': csrf_token,
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
            }, status=status.HTTP_401_UNAUTHORIZED)
