from django.urls import path
from authentication import views
from book_calendar.views import BookingListCreateView,BookingDetailView

urlpatterns = [
    path('calendar/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('calendar/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('calendar/all/', views.AllBookingsView.as_view(), name='all-bookings'),
]
