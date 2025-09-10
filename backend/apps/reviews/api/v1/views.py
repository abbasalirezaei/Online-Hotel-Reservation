from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from azure.ai.inference.models import SystemMessage, UserMessage

from apps.hotel.models import Hotel
from apps.reviews.models import Review
from .serializers import ReviewSerializer
from .utils import _call_text_summarizer


@api_view(["GET"])
def api_overview(request):
    """
    Endpoint: /api/v1/reviews/overview/

    Provides a quick overview of review-related API endpoints.
    Useful for onboarding, documentation, or development reference.
    """
    return Response(
        {
            "Submit Review for Hotel": "hotel/<hotel_id>/create/",  # POST
            "List Hotel Reviews": "hotel/<hotel_id>/list/",  # GET
            "Overview Endpoint": "overview/",
        }
    )


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
        return Review.objects.filter(hotel__id=hotel_id, parent__isnull=True).order_by(
            "-created_at"
        )


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
        "count": 12
      }
    """
    cache_key = f"hotel_reviews_summary:{hotel_id}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    reviews_qs = Review.objects.filter(hotel_id=hotel_id).order_by("-created_at")[:20]
    if not reviews_qs.exists():
        result = {"summary": "No reviews available.", "count": 0}
        cache.set(cache_key, result, 300)
        return Response(result)

    avg_rating = reviews_qs.aggregate(avg=Avg("rating"))["avg"]

    def clean_text(s, max_len=800):
        t = (s or "").strip()
        return (t[:max_len] + "...") if len(t) > max_len else t

    # Filter out empty or very short comments
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
        "avg_rating (numeric), pros (list of positive points), cons (list of negative points), "
        "top_mentions (list of most-mentioned words/items). Return only valid JSON."
    )

    reviews_text = "\n\n".join(
        [f"Rating: {r['rating']}\nComment: {r['comment']}" for r in reviews_list]
    )
    user_msg = UserMessage(
        f"This is a list of {len(reviews_list)} recent reviews for a hotel:\n\n{reviews_text}\n\n"
        "Provide a concise overall summary, pros, cons, and top mentions. Output must be JSON only."
    )

    try:
        resp = _call_text_summarizer([system, user_msg])
    except Exception as e:
        return Response({"error": "summarizer_failed", "detail": str(e)}, status=500)

    # Attach count and avg_rating if model returned valid JSON
    if isinstance(resp, dict):
        resp.setdefault("count", len(reviews_list))
        resp.setdefault(
            "avg_rating", float(avg_rating) if avg_rating is not None else None
        )
    else:
        resp = {
            "text": str(resp),
            "count": len(reviews_list),
            "avg_rating": float(avg_rating) if avg_rating is not None else None,
        }

    cache.set(cache_key, resp, 1)
    return Response(resp)
