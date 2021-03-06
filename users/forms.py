from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User
from market.models import Vendor


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


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
        fields = ["username", "email", "about", "image", "phone_number"]


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

    class Meta:
        model = Vendor
        fields = [
            "full_name", "phone_number", "about", "location",
            "twitter_url", "instagram_url", "education", "skills"
        ]


class StoreCreateFormEducationField(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ["education"]
