# from rest_framework import generics, permissions
# from notices.models import Notice
# from notices.serializers import NoticeSerializer

# class NoticesCreateView(generics.ListCreateAPIView):
#     serializer_class = NoticeSerializer
#     permission_classes = [permissions.AllowAny]  # 全ユーザーに許可

#     def get_queryset(self):
#         return Notice.objects.all()


from rest_framework import generics, permissions
from notices.models import Notice
from notices.serializers import NoticeSerializer

class NoticesCreateView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]
    #permission_classes = [permissions.IsAuthenticated] #is authenticated user must be define

class NoticeEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notice.objects.filter(created_by=self.request.user)


class NoticesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


    def get_queryset(self):
        return Notice.objects.all()


class NoticeDeleteView(generics.DestroyAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        # 自分のメモだけ削除対象にする
        return Notice.objects.filter(user=self.request.user)
