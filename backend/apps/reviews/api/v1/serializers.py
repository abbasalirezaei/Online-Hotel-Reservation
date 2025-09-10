from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["id", "user_name", "rating", "comment", "created_at", "replies"]

    def get_replies(self, obj):
        children = obj.children.all().order_by("created_at")
        return ReviewSerializer(children, many=True).data
