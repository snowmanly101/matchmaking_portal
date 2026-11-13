from django import forms
from .models import MatchProfile, SupportTicket

# Comprehensive global country list
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
    ('Nigeria', 'Nigeria'),
    ('Ghana', 'Ghana'),
    ('South Africa', 'South Africa'),
    ('Kenya', 'Kenya'),
    ('Argentina', 'Argentina'),
    ('Austria', 'Austria'),
    ('Belgium', 'Belgium'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Denmark', 'Denmark'),
    ('Finland', 'Finland'),
    ('Greece', 'Greece'),
    ('Hong Kong', 'Hong Kong'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Ireland', 'Ireland'),
    ('Israel', 'Israel'),
    ('Malaysia', 'Malaysia'),
    ('Mexico', 'Mexico'),
    ('Philippines', 'Philippines'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Qatar', 'Qatar'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('South Korea', 'South Korea'),
    ('Taiwan', 'Taiwan'),
    ('Thailand', 'Thailand'),
    ('Turkey', 'Turkey'),
    ('Vietnam', 'Vietnam'),
]

GENDER_CHOICES = [
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Non-Binary', 'Non-Binary'),
]

SEEKING_CHOICES = [
    ('', 'Seeking Who?'),
    ('Female', 'Female'),
    ('Male', 'Male'),
    ('Everyone', 'Everyone'),
]


class MatchProfileForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=COUNTRIES_LIST,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary', 'style': 'background-color: #212529 !important; color: #ffffff !important;'})
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary', 'style': 'background-color: #212529 !important; color: #ffffff !important;'})
    )

    seeking = forms.ChoiceField(
        choices=SEEKING_CHOICES,
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
            'city',
            'state',
            'zip_code',
            'country',
            'occupation',
            'height',
            'body_type',
            'ethnicity',
            'marital_status',
            'languages_spoken',
            'religion',
            'smoking',
            'drinking',
            'diet',
            'children',
            'education_level',
            'zodiac_sign',
            'bio',
            'profile_image',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'name@example.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Age'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': '+1 (555) 000-0000'}),
            'city': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'State / Region'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Zip / Postal Code'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Profession / Industry'}),
            'height': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': "e.g. 5'10\""}),
            'body_type': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Body Type'}),
            'ethnicity': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ethnicity'}),
            'marital_status': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Marital Status'}),
            'languages_spoken': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Languages Spoken'}),
            'religion': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Religion'}),
            'smoking': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Smoking Habit'}),
            'drinking': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Drinking Habit'}),
            'diet': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Diet'}),
            'children': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Children'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Education Level'}),
            'zodiac_sign': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Zodiac Sign'}),
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = [
            'q1_relationship_goal',
            'q2_core_values',
            'q3_dealbreakers',
            'q4_love_language',
            'q5_lifestyle_habits',
            'q6_conflict_resolution',
            'q7_future_vision',
            'q8_partner_personality',
            'q9_communication_preference',
        ]
        widgets = {
            'q1_relationship_goal': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'What are your relationship goals?'}),
            'q2_core_values': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'What core values matter most?'}),
            'q3_dealbreakers': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'What are absolute dealbreakers?'}),
            'q4_love_language': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'What is your love language?'}),
            'q5_lifestyle_habits': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'Describe your daily habits.'}),
            'q6_conflict_resolution': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'How do you resolve conflicts?'}),
            'q7_future_vision': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'What is your vision for the future?'}),
            'q8_partner_personality': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'What personality traits do you admire?'}),
            'q9_communication_preference': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2, 'placeholder': 'Preferred communication style?'}),
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