from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User
from market.models import Vendor


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
    # username = forms.CharField(widget=forms.TextInput(attrs={
    #     "class": "form-control",
    #     'name': "username"
    # }))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     "class": "form-control",
    #     'email': "email"
    # }))

    class Meta:
        model = User
        fields = ["username", "email", "about", "image", "phone_number", "location"]


class StoreCreateForm(forms.ModelForm):
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
        'class': 'form-control'
    }
    )
    )
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

    class Meta:
        model = Vendor
        fields = [
            "full_name", "phone_number", "about", "location",
            "twitter_url", "instagram_url", "education", "skills"
        ]
