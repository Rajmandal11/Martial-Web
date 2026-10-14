from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import BookingForm, ContactForm
from .models import (
    BlogPost,
    Booking,
    ClassStyle,
    GalleryItem,
    MembershipPlan,
    ScheduleSlot,
    Testimonial,
    Trainer,
)


def home(request):
    return render(
        request,
        "dojo/home.html",
        {
            "class_styles": ClassStyle.objects.all()[:5],
            "testimonials": Testimonial.objects.all()[:3],
        },
    )


def about(request):
    return render(
        request,
        "dojo/about.html",
        {
            "trainers": Trainer.objects.all()[:4],
            "testimonials": Testimonial.objects.all(),
        },
    )


def classes_list(request):
    return render(request, "dojo/classes.html", {"class_styles": ClassStyle.objects.all()})


def class_detail(request, slug):
    style = get_object_or_404(ClassStyle, slug=slug)
    slots = style.slots.select_related("trainer").all()
    return render(
        request,
        "dojo/class_detail.html",
        {"style": style, "slots": slots, "related": ClassStyle.objects.exclude(pk=style.pk)[:3]},
    )


def schedule(request):
    styles = ClassStyle.objects.all()
    active = request.GET.get("style")
    slots = ScheduleSlot.objects.select_related("class_style", "trainer").all()
    if active:
        slots = slots.filter(class_style__slug=active)
    days = [("MON", "Monday"), ("TUE", "Tuesday"), ("WED", "Wednesday"),
            ("THU", "Thursday"), ("FRI", "Friday"), ("SAT", "Saturday")]
    week = [(code, label, slots.filter(day=code)) for code, label in days]
    return render(
        request,
        "dojo/schedule.html",
        {"week": week, "styles": styles, "active": active or ""},
    )


def trainers(request):
    return render(
        request, "dojo/trainers.html", {"trainers": Trainer.objects.prefetch_related("classes_taught").all()}
    )


def membership(request):
    return render(request, "dojo/membership.html", {"plans": MembershipPlan.objects.all()})


def gallery(request):
    return render(request, "dojo/gallery.html", {"items": GalleryItem.objects.all()})


def blog_list(request):
    return render(request, "dojo/blog_list.html", {"posts": BlogPost.objects.all()})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    others = BlogPost.objects.exclude(pk=post.pk)[:3]
    return render(request, "dojo/blog_detail.html", {"post": post, "others": others})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dojo:contact_success")
    else:
        form = ContactForm()
    return render(request, "dojo/contact.html", {"form": form})


def contact_success(request):
    return render(request, "dojo/contact_success.html")


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save()
            request.session["last_booking_id"] = booking_obj.pk
            return redirect("dojo:booking_success")
    else:
        form = BookingForm()
        prefill = request.GET.get("style")
        if prefill:
            try:
                form.fields["class_style"].initial = ClassStyle.objects.get(slug=prefill).pk
            except ClassStyle.DoesNotExist:
                pass
    return render(request, "dojo/booking.html", {"form": form})


def booking_success(request):
    booking_obj = None
    pk = request.session.pop("last_booking_id", None)
    if pk:
        booking_obj = Booking.objects.select_related("class_style").filter(pk=pk).first()
    return render(request, "dojo/booking_success.html", {"booking": booking_obj})


class WarriorLoginView(auth_views.LoginView):
    template_name = "dojo/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        # "Remember me" unchecked -> session expires when the browser closes.
        if not self.request.POST.get("remember_me"):
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 14)  # 2 weeks
        return super().form_valid(form)


class WarriorLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("dojo:home")


@login_required
def member_area(request):
    bookings = Booking.objects.select_related("class_style").filter(
        email__iexact=request.user.email
    )
    return render(request, "dojo/member_area.html", {"bookings": bookings})


def handler404(request, exception):
    return render(request, "dojo/404.html", status=404)
