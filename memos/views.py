
from rest_framework import generics, permissions
from .models import Memo
from .serializers import MemoSerializer

class MemoListCreateView(generics.ListCreateAPIView):
    serializer_class = MemoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 自分のメモだけ取得
        return Memo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 作成時に自動でログインユーザーを紐付け
        serializer.save(user=self.request.user)

class MemoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 自分のメモだけ取得・編集・削除できる
        return Memo.objects.filter(user=self.request.user)

class MemoDeleteView(generics.DestroyAPIView):
    serializer_class = MemoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 自分のメモだけ削除対象にする
        return Memo.objects.filter(user=self.request.user)