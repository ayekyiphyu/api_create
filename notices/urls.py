from django.urls import path
from notices.views import (
    NoticesCreateView,
    NoticesRetrieveUpdateDestroyView,
    NoticeDeleteView,
)

urlpatterns = [
    path('notices/', NoticesCreateView.as_view(), name='notices-list-create'),
    path('notices/<int:pk>/', NoticesRetrieveUpdateDestroyView.as_view(), name='notices-detail'),
    path('notices/<int:pk>/delete/', NoticeDeleteView.as_view(), name='notice-delete'),
]
