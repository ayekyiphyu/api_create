from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsOwnerOrReadOnly

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # 👈 anyone can read
        return [permissions.IsAuthenticated()]  # 👈 only logged-in users can create

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # 全ての予約を取得可能（表示用）
        return Booking.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 自分の予約のみ削除可能
        if instance.user != request.user:
            return Response(
                {'error': '他のユーザーの予約は削除できません。'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(
            {'message': 'Booking deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # 自分の予約のみ更新可能
        if instance.user != request.user:
            return Response(
                {'error': '他のユーザーの予約は編集できません。'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # 自分の予約のみ部分更新可能
        if instance.user != request.user:
            return Response(
                {'error': '他のユーザーの予約は編集できません。'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)


