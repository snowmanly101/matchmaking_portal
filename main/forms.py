from django import forms
from .models import MatchProfile


class MatchProfileForm(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = [
        'full_name',
        'email',
        'age',
        'phone',
        'gender',
        'seeking',
        'country',
        'occupation',
        'bio',
        'profile_image',
    ]
    widgets = {
        'full_name': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter full name'}
        ),
        'email': forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'name@example.com'}
        ),
        'age': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Age'}
        ),
        'phone': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 000-0000',
            }
        ),
        'gender': forms.Select(attrs={'class': 'form-select'}),
        'seeking': forms.Select(attrs={'class': 'form-select'}),
        'country': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Country of Residence',
            }
        ),
        'occupation': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Profession / Industry'}
        ),
        'bio': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': (
                    'Tell us about yourself and what you are looking'
                    ' for...'
                ),
            }
        ),
        'profile_image': forms.ClearableFileInput(
            attrs={'class': 'form-control text-white'}
        ),
    }


# Individual Question Forms for the 9-Step Interactive Sequence
class Question1Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q1_relationship_goal']
    widgets = {
        'q1_relationship_goal': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Long-term committed relationship leading to marriage...',
            }
        )
    }


class Question2Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q2_core_values']
    widgets = {
        'q2_core_values': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Honesty, ambition, family orientation, and faith...',
            }
        )
    }


class Question3Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q3_dealbreakers']
    widgets = {
        'q3_dealbreakers': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Dishonesty, lack of ambition, smoking...',
            }
        )
    }


class Question4Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q4_love_language']
    widgets = {
        'q4_love_language': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Quality time and acts of service...',
            }
        )
    }


class Question5Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q5_lifestyle_habits']
    widgets = {
        'q5_lifestyle_habits': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Fitness enthusiast, early riser, loves traveling...',
            }
        )
    }


class Question6Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q6_conflict_resolution']
    widgets = {
        'q6_conflict_resolution': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Calm discussion, taking space when needed, compromise...',
            }
        )
    }


class Question7Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q7_future_vision']
    widgets = {
        'q7_future_vision': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Building businesses, settling down abroad, raising kids...',
            }
        )
    }


class Question8Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q8_partner_personality']
    widgets = {
        'q8_partner_personality': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Sense of humor, emotionally intelligent, kind...',
            }
        )
    }


class Question9Form(forms.ModelForm):

  class Meta:
    model = MatchProfile
    fields = ['q9_communication_preference']
    widgets = {
        'q9_communication_preference': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., Daily phone calls, WhatsApp check-ins...',
            }
        )
    }