from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "hotel", "rating", "created_at", "parent")
    list_filter = ("rating", "created_at", "hotel")
    search_fields = ("user__username", "hotel__name", "comment")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("user", "hotel", "rating", "comment", "parent")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


admin.site.register(Review, ReviewAdmin)
