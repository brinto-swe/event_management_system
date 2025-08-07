from django import forms
from .models import Event, Participant, Category
from django.core.exceptions import ValidationError
from django.utils import timezone


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'Class':' border-solid border-2 border-zinc-500 p-2 rounded',
                'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'Class':'border-solid border-2 border-zinc-500 p-2 rounded','rows': 3}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300'
            }),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past.")
        return date


class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    

    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={
                'Class':'border-solid border-2 border-zinc-500 p-2 rounded', 'placeholder':'Enter participant name'
            }),
            'email': forms.EmailInput(attrs={
                'Class':'border-solid border-2 border-zinc-500 p-2 rounded', 'placeholder': 'example@email.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Participant.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
