# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.exceptions import PermissionDenied
# from django.shortcuts import get_object_or_404
# from .models import Memo
# from .serializers import MemoSerializer

# class MemoListCreateView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         """List all memos for the authenticated user"""
#         memos = Memo.objects.filter(user=request.user).order_by('-updated_at')
#         serializer = MemoSerializer(memos, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         """Create a new memo for the authenticated user"""
#         serializer = MemoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MemoRetrieveUpdateDestroyView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get_memo(self, pk, user):
#         """Helper method to get a memo and verify ownership"""
#         memo = get_object_or_404(Memo, pk=pk)
#         if memo.user != user:
#             raise PermissionDenied("You don't have permission to access this memo")
#         return memo
    
#     def get(self, request, pk):
#         """Retrieve a memo"""
#         memo = self.get_memo(pk, request.user)
#         serializer = MemoSerializer(memo)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         """Update a memo"""
#         memo = self.get_memo(pk, request.user)
#         serializer = MemoSerializer(memo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         """Delete a memo"""
#         memo = self.get_memo(pk, request.user)
#         memo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# memos/views.py
from rest_framework import generics, permissions
from .models import Memo
from .serializers import MemoSerializer

class MemoListCreateView(generics.ListCreateAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [permissions.AllowAny]

class MemoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [permissions.AllowAny]

class MemoDeleteView(generics.DestroyAPIView):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [permissions.AllowAny]

def perform_create(self, serializer):
    if self.request.user.is_authenticated:
        serializer.save(user=self.request.user)
    else:
        serializer.save(user = None)
    # If the user is not authenticated, save the memo without a user