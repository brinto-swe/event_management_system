# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UsernameField
# from .models import Event, Category


# class SignUpForm(forms.ModelForm):
#     password1 = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(attrs={
#             'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
#             'placeholder': 'Enter your password'
#         })
#     )
#     password2 = forms.CharField(
#         label='Confirm Password',
#         widget=forms.PasswordInput(attrs={
#             'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
#             'placeholder': 'Re-enter your password'
#         })
#     )

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')
#         field_classes = {'username': UsernameField}

#         widgets = {
#             'username': forms.TextInput(attrs={
#                 'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Enter a username'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Enter your email (example@mail.com)'
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Enter your first name'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Enter your last name'
#             }),
#         }

#     def clean(self):
#         cleaned = super().clean()
#         p1, p2 = cleaned.get('password1'), cleaned.get('password2')
#         if p1 and p2 and p1 != p2:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         user.is_active = False  # Until email verification or admin approval
#         if commit:
#             user.save()
#         return user


# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['name', 'description', 'date', 'time', 'location', 'category', 'image']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Enter an Event name'
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Give some description about event'
#             }),
#             'date': forms.DateInput(attrs={
#                 'type': 'date',
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#             }),
#             'time': forms.TimeInput(attrs={
#                 'type': 'time',
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#             }),
#             'location': forms.TextInput(attrs={
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Give Event Location'
#             }),
#             'category': forms.Select(attrs={
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#             }),
#         }


# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'description']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Enter a Category name'
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
#                 'placeholder': 'Give some description about Category'
#             }),
#         }


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Event, Category, RSVP


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            'placeholder': 'Re-enter your password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Enter a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Enter your email (example@mail.com)'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Enter your last name'
            }),
            # 'phone_number': forms.TextInput(attrs={
            #     'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            #     'placeholder': 'Enter your phone number'
            # }),
            # 'profile_picture': forms.FileInput(attrs={
            #     'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300'
            # }),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full border px-3 py-2 mb-4 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Enter an Event name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Give some description about event'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Give Event Location'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Enter a Category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-300',
                'placeholder': 'Give some description about Category'
            }),
        }


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = []
