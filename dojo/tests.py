"""Smoke tests: every page loads, forms work, login + member area work."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Booking, ClassStyle, ContactMessage


class SiteSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)
        cls.style = ClassStyle.objects.get(slug="karate")
        # Give the demo user a booking so the member area has something to show.
        Booking.objects.create(
            name="Demo Member",
            email="demo@warriormartialarts.com",
            phone="+919876543210",
            class_style=cls.style,
            preferred_date=date.today() + timedelta(days=7),
        )

    # -- pages return 200 ---------------------------------------------------
    def test_public_pages_200(self):
        urls = [
            reverse("dojo:home"),
            reverse("dojo:about"),
            reverse("dojo:classes"),
            reverse("dojo:class_detail", args=[self.style.slug]),
            reverse("dojo:schedule"),
            reverse("dojo:schedule") + "?style=karate",
            reverse("dojo:trainers"),
            reverse("dojo:membership"),
            reverse("dojo:gallery"),
            reverse("dojo:blog"),
            reverse("dojo:contact"),
            reverse("dojo:booking"),
            reverse("dojo:login"),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200, url)
        # blog detail for each seeded post
        from .models import BlogPost

        for post in BlogPost.objects.all():
            with self.subTest(post=post.slug):
                self.assertEqual(
                    self.client.get(reverse("dojo:blog_detail", args=[post.slug])).status_code, 200
                )

    def test_home_has_reference_sections(self):
        html = self.client.get(reverse("dojo:home")).content.decode()
        for needle in ["DISCIPLINE.", "CHOOSE YOUR STYLE", "WE BUILD WARRIORS",
                       "READY TO START YOUR JOURNEY?", "KARATE", "MUAY THAI"]:
            self.assertIn(needle, html)

    def test_no_placeholder_text(self):
        for name in ["home", "about", "classes", "schedule", "trainers",
                     "membership", "gallery", "blog", "contact", "booking", "login"]:
            html = self.client.get(reverse(f"dojo:{name}")).content.decode().lower()
            self.assertNotIn("lorem", html, name)
            self.assertNotIn("todo", html, name)

    # -- booking ------------------------------------------------------------
    def test_booking_valid(self):
        before = Booking.objects.count()
        resp = self.client.post(
            reverse("dojo:booking"),
            {
                "name": "Test Student",
                "email": "student@example.com",
                "phone": "+911234567890",
                "class_style": self.style.pk,
                "preferred_date": (date.today() + timedelta(days=3)).isoformat(),
                "message": "First class!",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Booking.objects.count(), before + 1)
        self.assertEqual(self.client.get(reverse("dojo:booking_success")).status_code, 200)

    def test_booking_invalid(self):
        before = Booking.objects.count()
        resp = self.client.post(reverse("dojo:booking"), {"name": "", "email": "not-an-email"})
        self.assertEqual(resp.status_code, 200)  # form re-rendered with errors
        self.assertEqual(Booking.objects.count(), before)

    def test_booking_style_prefill(self):
        resp = self.client.get(reverse("dojo:booking") + "?style=karate")
        self.assertEqual(resp.status_code, 200)

    # -- contact ------------------------------------------------------------
    def test_contact_valid(self):
        before = ContactMessage.objects.count()
        resp = self.client.post(
            reverse("dojo:contact"),
            {"name": "Curious Parent", "email": "parent@example.com",
             "phone": "", "message": "Do you have kids batches?"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), before + 1)
        self.assertEqual(self.client.get(reverse("dojo:contact_success")).status_code, 200)

    # -- auth / member area -------------------------------------------------
    def test_login_and_member_area(self):
        login_ok = self.client.login(username="demo", password="warrior123")
        self.assertTrue(login_ok)
        resp = self.client.get(reverse("dojo:member_area"))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn("Karate", html)  # demo user's booking lists the class
        self.assertIn("October 19, 2026", html)

    def test_member_area_requires_login(self):
        resp = self.client.get(reverse("dojo:member_area"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("dojo:login"), resp["Location"])

    def test_admin_login_page_loads(self):
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)

    def test_seed_idempotent(self):
        counts_before = {
            "styles": ClassStyle.objects.count(),
            "users": get_user_model().objects.count(),
        }
        call_command("seed_demo", verbosity=0)
        self.assertEqual(ClassStyle.objects.count(), counts_before["styles"])
        self.assertEqual(get_user_model().objects.count(), counts_before["users"])
