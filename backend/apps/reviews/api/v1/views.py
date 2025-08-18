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


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def hotel_reviews_summary(request, hotel_id):
    """
    GET /reviews/hotel/<hotel_id>/summary/
    Returns a short summary of up to N latest reviews, cached for 5 minutes.
    Response JSON shape (example):
      {
        "summary": "...",
        "avg_rating": 4.2,
        "positive_points": ["..."],
        "negative_points": ["..."],
        "top_mentions": ["..."],
        "count": 12,
        "hotel_name": "Hotel Paradise"
      }
    """
    cache_key = f"hotel_reviews_summary:{hotel_id}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    reviews_qs = Review.objects.filter(
        hotel_id=hotel_id).order_by("-created_at")[:20]
    if not reviews_qs.exists():
        result = {"summary": "No reviews available.", "count": 0}
        cache.set(cache_key, result, 300)
        return Response(result)

    avg_rating = reviews_qs.aggregate(avg=Avg("rating"))["avg"]

    def clean_text(s, max_len=800):
        t = (s or "").strip()
        return (t[:max_len] + "...") if len(t) > max_len else t

    reviews_list = [
        {"rating": r.rating, "comment": clean_text(r.comment)}
        for r in reviews_qs
        if r.comment and len(r.comment.strip()) > 10
    ]

    if not reviews_list:
        result = {"summary": "No meaningful reviews available.", "count": 0}
        cache.set(cache_key, result, 300)
        return Response(result)

    system = SystemMessage(
        "You are an assistant that summarizes hotel reviews in English. "
        "Return output as JSON only with fields: summary (short text), "
        "avg_rating (numeric), positive_points (list of positive aspects), "
        "negative_points (list of negative aspects), top_mentions (list of most-mentioned words/items). "
        "Return only valid JSON."
    )

    reviews_text = "\n\n".join(
        [f"Rating: {r['rating']}\nComment: {r['comment']}" for r in reviews_list])
    user_msg = UserMessage(
        f"""This is a list of {len(reviews_list)} recent reviews for a hotel:

{reviews_text}

Please provide:
- A short overall summary of the reviews
- A list of positive points mentioned by users
- A list of negative points mentioned by users
- A list of the most frequently mentioned keywords or items

Return the result as valid JSON with fields:
summary, positive_points, negative_points, top_mentions.
"""
    )

    try:
        resp = _call_text_summarizer([system, user_msg])
    except Exception as e:
        return Response({"error": "summarizer_failed", "detail": str(e)}, status=500)

    if isinstance(resp, dict):
        resp.setdefault("count", len(reviews_list))
        resp.setdefault("avg_rating", float(avg_rating)
                        if avg_rating is not None else None)
    else:
        resp = {
            "text": str(resp),
            "count": len(reviews_list),
            "avg_rating": float(avg_rating) if avg_rating is not None else None
        }

    # Add hotel name to response
    try:
        hotel_name = Hotel.objects.get(id=hotel_id).name
        resp["hotel_name"] = hotel_name
    except Hotel.DoesNotExist:
        resp["hotel_name"] = None

    # Cache for 5 minutes
    cache.set(cache_key, resp, 1)
    return Response(resp)
