from django import forms
from .models import *
from djrichtextfield.widgets import RichTextWidget
from ckeditor.fields import RichTextFormField
from django.forms import ModelForm, inlineformset_factory


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
    description = RichTextFormField(widget=forms.Textarea(attrs={
        'placeholder': 'Product Description',
        'type': 'text',
        'name': 'product_description',
        'id': 'product_description',
        'class': 'form-control'
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
    # category_type = Category.objects.all().values_list("id", "name")
    # category = forms.CharField(widget=forms.Select(choices=[item for item in category_type], attrs={
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
        "type": "file",
        "accept": "image/*"
    }
    )
    )

    class Meta:
        model = ProductImage
        fields = ["image"]


ImgFormSet = inlineformset_factory(
    parent_model=Product, model=ProductImage,
    fields=['image'], extra=0,
)


class ReviewBox(forms.ModelForm):
    RATING_TYPES = (
        (1, "★☆☆☆☆ (1/5)"), (2, "★★☆☆☆ (2/5)"), (3, "★★★☆☆ (3/5)"),
        (4, "★★★★☆ (4/5)"), (5, "★★★★★ (5/5)")
    )

    rating = forms.CharField(widget=forms.Select(choices=RATING_TYPES, attrs={
        'class': 'form-control',
        'name': 'education',

    }))

    review = forms.CharField(widget=forms.Textarea(attrs={
        "name": "product review",
        "placeholder": "Product Review?",
        'type': 'text',
        "rows": 3,
        "required": True
    }))

    class Meta:
        model = ProductReview
        fields = ["rating", "review"]
