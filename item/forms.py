from django import forms
from .models import Item


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'category']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Name'}))

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Description'}))

    price = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Price'}))

    image = forms.ImageField(required=True)

    category = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label="Select Category")