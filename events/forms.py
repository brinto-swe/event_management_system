from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField
from .models import Event, Category

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        field_classes = {'username': UsernameField}

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False 
        
        if commit:
            user.save()
        return user

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category','image']
        widget = {
            'date':forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={'class': 'time-picker-input'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
