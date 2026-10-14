from django.contrib import admin

from .models import (
    BlogPost,
    Booking,
    ClassStyle,
    ContactMessage,
    GalleryItem,
    MembershipPlan,
    ScheduleSlot,
    Testimonial,
    Trainer,
)


@admin.register(ClassStyle)
class ClassStyleAdmin(admin.ModelAdmin):
    list_display = ("name", "tagline", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "specialty")
    search_fields = ("name", "specialty")
    filter_horizontal = ("classes_taught",)


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration", "highlighted", "order")
    list_editable = ("order", "highlighted")
    list_filter = ("highlighted",)


@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ("day", "start_time", "end_time", "class_style", "trainer")
    list_filter = ("day", "class_style")
    ordering = ("day", "start_time")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "body")
    date_hierarchy = "published_at"


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "caption", "order")
    list_editable = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "class_style", "preferred_date", "status", "created_at")
    list_filter = ("status", "class_style", "preferred_date")
    search_fields = ("name", "email", "phone")
    list_editable = ("status",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "replied")
    list_editable = ("replied",)
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
