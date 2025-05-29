from django.urls import path
from notices.views import NoticesCreateView, NoticesRetrieveUpdateDestroyView

urlpatterns = [
  path('notices/',NoticesCreateView.as_view(), name='notices-list-create'),
  path('notices/<int:pk>/', NoticesRetrieveUpdateDestroyView.as_view(), name='notices-detail'),
]