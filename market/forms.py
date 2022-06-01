from django import forms
from .models import *


class CreateProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Product Name',
        'type': 'text',
        'name': 'product_name',
        'id': 'product_name',
        'class': 'form-control'
            }
        )
    )
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Product Price',
        'type': 'number',
        'name': 'price',
        'id': 'product_price',
        'class': 'form-control'
    }
    )
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Product Description',
        'type': 'text',
        'name': 'product_description',
        'id': 'product_description',
        'class': 'form-control',
        "rows": 3,
        "required": True
    }
    )
    )
    delivery_period = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Product delivery period',
        'type': 'number',
        'name': 'delivery_period',
        'id': 'delivery_period',
        'class': 'form-control'
    }
    )
    )
    # image = forms.ImageField(widget=forms.FileInput(attrs={
    #
    #     "required": True,
    #     "multiple": True
    # }
    # )
    # )

    class Meta:
        model = Product
        fields = ["name", "price", "category", "description", "delivery_period"]


class CategoryField(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["category"]


class ImageField(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        "name": "images",
        "required": True,
        "multiple": True,
        "type": "file"
    }
    )
    )

    class Meta:
        model = ProductImage
        fields = ["image"]


class ReviewBox(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={
        "name": "product review",
        "placeholder": "Product Review?",
        'type': 'text',
        "rows": 3,
        "required": True
    }))

    class Meta:
        model = ProductReview
        fields = ["review"]
