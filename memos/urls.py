from django.urls import path
from .views import MemoDeleteView, MemoListCreateView, MemoRetrieveUpdateDestroyView

urlpatterns = [
   path('', MemoListCreateView.as_view(), name='memo-list-create'),
   path('<int:pk>/', MemoRetrieveUpdateDestroyView.as_view(), name='memo-detail'),
   path('<int:pk>/delete/', MemoDeleteView.as_view(), name='memo-delete'),
]