from django import forms

from main.models import Newsletter
from main.common import Carousel


class NewsletterCreationForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'status']


class CarouselCreationForm(forms.ModelForm):

    class Meta:
        model = Carousel
        fields = '__all__'
