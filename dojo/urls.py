from django.urls import path

from . import views

app_name = "dojo"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("classes/", views.classes_list, name="classes"),
    path("classes/<slug:slug>/", views.class_detail, name="class_detail"),
    path("schedule/", views.schedule, name="schedule"),
    path("trainers/", views.trainers, name="trainers"),
    path("membership/", views.membership, name="membership"),
    path("gallery/", views.gallery, name="gallery"),
    path("blog/", views.blog_list, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
    path("contact/thanks/", views.contact_success, name="contact_success"),
    path("free-trial/", views.booking, name="booking"),
    path("free-trial/success/", views.booking_success, name="booking_success"),
    path("login/", views.WarriorLoginView.as_view(), name="login"),
    path("logout/", views.WarriorLogoutView.as_view(), name="logout"),
    path("member/", views.member_area, name="member_area"),
]
