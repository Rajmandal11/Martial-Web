from django.db import models
from django.utils.text import slugify


class ClassStyle(models.Model):
    """A martial-arts discipline taught at the dojo (Karate, BJJ, ...)."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(
        max_length=120,
        help_text="Static image filename, e.g. class-karate.jpg (in dojo/static/dojo/img/). No uploads needed.",
    )
    icon = models.CharField(
        max_length=60,
        default="🥋",
        help_text="Emoji/short label shown in the style-card badge.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=120, default="Instructor")
    bio = models.TextField()
    specialty = models.CharField(max_length=120)
    image = models.CharField(
        max_length=120,
        help_text="Static image filename, e.g. trainer-1.jpg (in dojo/static/dojo/img/).",
    )
    classes_taught = models.ManyToManyField(ClassStyle, blank=True, related_name="trainers")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    name = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=80, help_text="e.g. 'per month', 'per quarter'.")
    features = models.TextField(help_text="One feature per line.")
    highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    def __str__(self):
        return f"{self.name} — ₹{self.price:g} {self.duration}"


class ScheduleSlot(models.Model):
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]

    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_style = models.ForeignKey(ClassStyle, on_delete=models.CASCADE, related_name="slots")
    trainer = models.ForeignKey(
        Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name="slots"
    )

    class Meta:
        ordering = ["day", "start_time"]

    def __str__(self):
        return (
            f"{self.get_day_display()} {self.start_time:%I:%M %p}–{self.end_time:%I:%M %p} "
            f"· {self.class_style.name}"
        )


class BlogPost(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    excerpt = models.CharField(max_length=300)
    body = models.TextField()
    author = models.CharField(max_length=80, default="Warrior Team")
    published_at = models.DateTimeField()
    image = models.CharField(
        max_length=120,
        blank=True,
        help_text="Optional static image filename (in dojo/static/dojo/img/).",
    )

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    title = models.CharField(max_length=120)
    image = models.CharField(
        max_length=120,
        help_text="Static image filename (in dojo/static/dojo/img/).",
    )
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=120, default="Member")
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} — {self.role}"


class Booking(models.Model):
    """A free-trial class booking request from the website."""

    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("done", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    class_style = models.ForeignKey(ClassStyle, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        style = self.class_style.name if self.class_style else "Any class"
        return f"{self.name} — {style} on {self.preferred_date} ({self.get_status_display()})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message from {self.name} ({self.created_at:%Y-%m-%d})"
