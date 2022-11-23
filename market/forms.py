from django import forms
from .models import *
from djrichtextfield.widgets import RichTextWidget


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
        'class': 'form-control',
        'step': "0.01"
    }
    )
    )
    description = forms.CharField(widget=RichTextWidget())
    delivery_period = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Product delivery period',
        'type': 'number',
        'name': 'delivery_period',
        'id': 'delivery_period',
        'class': 'form-control'
    }
    )
    )
    # category_type = Category.objects.all().values_list("name", "name")
    # category = forms.CharField(widget=forms.Select(choices=category_type, attrs={
    #     'class': 'form-control',
    #     'name': 'category',
    #
    # }))

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
