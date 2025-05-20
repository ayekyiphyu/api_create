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

# Add CSRF exemption to the login view
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"Attempting login with email: {email}")
        
        # Check if the user exists first
        try:
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                print(f"User with email {email} not found")
                return Response({'error': 'Email not registered'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"Error checking user: {str(e)}")
            return Response({'error': f'Server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # Try to authenticate the user
        try:
            # First try with username=email
            user = authenticate(request, username=email, password=password)
            
            # If that fails, try with email=email
            if user is None:
                user = authenticate(request, email=email, password=password)
                
            if user is not None:
                login(request, user)
                print(f"User successfully logged in: {user.email}")
                print(f"User successfully logged in: {user.username}")
                return Response({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                    }
                }, status=status.HTTP_200_OK)
            else:
                print(f"Authentication failed for {email}")
                print(f"User exists but password is incorrect")
                return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            print(f"Login exception: {str(e)}")
            return Response({'error': f'Login error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Also exempt the logout view from CSRF
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'status': 'success'})
    
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
        



    