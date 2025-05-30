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
    permission_classes = [permissions.IsAuthenticated] #is authenticated user must be define

# Retrieve, update or delete a specific notice by id
class NoticesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


    def get_queryset(self):
        return Notice.objects.all()