# reviews/views.py
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404

from apps.hotel.models import Hotel
from apps.reviews.models import Review
from .serializers import ReviewSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_overview(request):
    """
    Endpoint: /api/v1/reviews/overview/

    Provides a quick overview of review-related API endpoints.
    Useful for onboarding, documentation, or development reference.
    """
    return Response({
        "Submit Review for Hotel": "hotel/<hotel_id>/create/",  # POST
        "List Hotel Reviews": "hotel/<hotel_id>/list/",       # GET
        "Overview Endpoint": "overview/"
    })


class CreateHotelReviewView(generics.CreateAPIView):
    """
    Endpoint: POST /reviews/hotel/<hotel_id>/create/
    Allows an authenticated user to submit a review for a hotel
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get("hotel_id")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer.save(user=self.request.user, hotel=hotel)


class HotelReviewListView(generics.ListAPIView):
    """
    Endpoint: GET /reviews/hotel/<hotel_id>/list/
    Returns a list of all reviews for a hotel, including parent-child relations
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_id")
        return Review.objects.filter(hotel__id=hotel_id, parent__isnull=True).order_by("-created_at")
