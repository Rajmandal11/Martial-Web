from django import forms

from .models import Booking, ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 98765 43210"}),
            "message": forms.Textarea(attrs={"placeholder": "How can we help you?", "rows": 5}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["name", "email", "phone", "class_style", "preferred_date", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 98765 43210"}),
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Anything we should know? (optional)", "rows": 4}
            ),
        }
        labels = {"class_style": "Choose your style"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["class_style"].empty_label = "Not sure yet — help me choose"
        self.fields["class_style"].required = False
