from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .serializers import RegisterSerializer, User
from django.contrib.auth.hashers import check_password
import json

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

class LoginView(APIView):
    def post(self, request):
        # Print the raw request body for debugging
        print("Received login data:", request.body.decode('utf-8'))
        
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"Attempting login with email: {email}")
        
        # First approach: Try Django's authenticate but with debug
        user = authenticate(request, username=email, password=password)
        if user is None:
            user = authenticate(request, email=email, password=password)
        
        # If authenticate failed, try direct approach
        if user is None:
            try:
                # Get the user directly
                user_obj = User.objects.get(email=email)
                print(f"Found user: {user_obj.email}, id: {user_obj.id}")
                print(f"Password from request: {password[:1]}*****")  # Print first char only for security
                
                # IMPORTANT: Manual password check with debug
                password_valid = check_password(password, user_obj.password)
                print(f"Password valid: {password_valid}")
                
                if password_valid:
                    # Manually log the user in
                    user = user_obj
                    login(request, user)
                    print(f"Manual login successful for {email}")
                else:
                    print(f"Password invalid for user {email}")
                    # Check if password is stored correctly
                    print(f"Password hash in DB starts with: {user_obj.password[:10]}...")
                    return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                print(f"User with email {email} not found")
                return Response({'error': 'Email not registered'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print(f"Login exception: {str(e)}")
                return Response({'error': f'Login error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # If we have a user by this point (either from authenticate or manual check)
        if user is not None:
            # Make sure the user is logged in
            login(request, user)
            print(f"User successfully logged in: {user.email}")
            
            # Check if session was created
            print(f"Session ID: {request.session.session_key}")
            
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            print("Unknown authentication failure")
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'status': 'success'})
    
class AuthRootView(APIView):
    def get(self, request):
        return Response({
            'login': '/api/auth/login/',
            'logout': '/api/auth/logout/',
        })