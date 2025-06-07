from django.urls import path
from book_calendar.views import (
    BookingListCreateView, 
    BookingDetailView
    # Remove BookingDeleteView import since we're not using it
)

urlpatterns = [
    # List all bookings and create new booking
    path('calendar/', BookingListCreateView.as_view(), name='booking-list-create'),
    
    # Individual booking operations (GET, PUT, PATCH, DELETE)
    path('calendar/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    
]