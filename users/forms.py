from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User
from market.models import Vendor
from djrichtextfield.widgets import RichTextWidget


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     print(email)
    #     check_email = User.objects.filter(email=email).exists()
    #     if check_email:
    #         raise forms.ValidationError("Email already exists.")


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'name': "username",
        "id": "username",
        'placeholder': 'Username',

    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        'name': "email",
        "id": "email",
        'placeholder': 'Email Address',

    }))
    about = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'About',
        'type': 'text',
        'name': 'about',
        'id': 'about',
        'class': 'form-control',
        "rows": 3,
    }
    )
    )
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "form-control",
        'name': "phone_number",
        'type': 'number',
        "id": "phone_number",
        'placeholder': 'Phone Number',

    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'name': "location",
        'type': 'text',
        "required": False,
        'placeholder': 'Location',
        "class": "form-control",
        "id": "location"

    }))

    class Meta:
        model = User
        fields = ["username", "email", "about", "image", "phone_number", "location"]


class StoreCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # Customize the queryset of the foreign key field
    #     self.fields['user'].queryset = User.objects.all()
    #
    #     # Add other attributes to the form
    #     self.fields['user_username'] = forms.CharField(widget=forms.TextInput(attrs={
    #         "class": "form-control",
    #         'name': "username",
    #         "id": "username",
    #         'placeholder': 'Username',
    #
    #     }))
    #     self.fields['user_email'] = forms.EmailField(widget=forms.EmailInput(attrs={
    #         "class": "form-control",
    #         'name': "email",
    #         "id": "email",
    #         'placeholder': 'Email Address',
    #
    #     }))

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Full name',
        'type': 'text',
        'name': 'full_name',
        'id': 'full_name',
        'class': 'form-control'
    }
    )
    )
    location = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Location',
        'type': 'text',
        'name': 'Location',
        'id': 'Location',
        'class': 'form-control'
    }
    )
    )
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'type': 'text',
        'name': 'phone_number',
        'id': 'phone_number',
        'class': 'form-control',
        'maxlength': 11
    }
    )
    )
    about = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Bio',
        'type': 'text',
        'name': 'about',
        'id': 'about',
        'class': 'form-control',
        "rows": 3,
    }
    )
    )
    instagram_url = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Instagram URL',
        'type': 'url',
        'name': 'instagram_url',
        'id': 'instagram_url',
        'class': 'form-control',
    }
    )
    )
    twitter_url = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Twitter URL',
        'type': 'url',
        'name': 'twitter_url',
        'id': 'twitter_url',
        'class': 'form-control',
    }
    )
    )
    skills = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Skills',
        'type': 'text',
        'name': 'skills',
        'id': 'skills',
        'class': 'form-control'
    }
    )
    )
    EDUCATION_TYPES = (
        (1, "B.Sc."), (2, "M.Sc."), (3, "M.A."), (4, "M.Sc."), (5, "LLB"), (6, "Others"),
    )
    education = forms.CharField(widget=forms.Select(choices=EDUCATION_TYPES, attrs={
        'class': 'form-control',
        'name': 'education',

    }))
    withdrawal_pin = forms.CharField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'Withdrawal Pin',
            'type': 'password',
            'name': 'withdrawal_pin',
            'id': 'withdrawal_pin',
            'class': 'form-control',
            'maxlength': 4
        }
    ))

    class Meta:
        model = Vendor
        fields = [
            "full_name", "phone_number", "about", "location",
            "twitter_url", "instagram_url", "education", "skills", "withdrawal_pin", "image"
        ]
