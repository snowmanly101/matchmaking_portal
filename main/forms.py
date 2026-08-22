from django import forms
from .models import MatchProfile, SupportTicket

COUNTRIES_LIST = [
    ('', 'Select Country'),
    ('United States', 'United States'),
    ('Canada', 'Canada'),
    ('United Kingdom', 'United Kingdom'),
    ('Australia', 'Australia'),
    ('Germany', 'Germany'),
    ('France', 'France'),
    ('Spain', 'Spain'),
    ('Italy', 'Italy'),
    ('Brazil', 'Brazil'),
    ('Japan', 'Japan'),
    ('Singapore', 'Singapore'),
    ('New Zealand', 'New Zealand'),
    ('Switzerland', 'Switzerland'),
    ('Netherlands', 'Netherlands'),
    ('Sweden', 'Sweden'),
    ('Norway', 'Norway'),
    ('United Arab Emirates', 'United Arab Emirates'),
]


class MatchProfileForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=COUNTRIES_LIST,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary', 'style': 'background-color: #212529 !important; color: #ffffff !important;'})
    )

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
            'full_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'name@example.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Age'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': '+1 (555) 000-0000'}),
            'gender': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary', 'style': 'background-color: #212529 !important; color: #ffffff !important;'}),
            'seeking': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary', 'style': 'background-color: #212529 !important; color: #ffffff !important;'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Profession / Industry'}),
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['sender_email', 'subject', 'message']
        widgets = {
            'sender_email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Complaint / Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3, 'placeholder': 'Describe your issue...'}),
        }


class Question1Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q1_relationship_goal']
        widgets = {'q1_relationship_goal': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question2Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q2_core_values']
        widgets = {'q2_core_values': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question3Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q3_dealbreakers']
        widgets = {'q3_dealbreakers': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question4Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q4_love_language']
        widgets = {'q4_love_language': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question5Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q5_lifestyle_habits']
        widgets = {'q5_lifestyle_habits': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question6Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q6_conflict_resolution']
        widgets = {'q6_conflict_resolution': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question7Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q7_future_vision']
        widgets = {'q7_future_vision': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question8Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q8_partner_personality']
        widgets = {'q8_partner_personality': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}

class Question9Form(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = ['q9_communication_preference']
        widgets = {'q9_communication_preference': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3})}