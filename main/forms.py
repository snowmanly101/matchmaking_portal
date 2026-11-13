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

SMOKING_CHOICES = [('', 'Select Smoking Habit'), ('Non-smoker', 'Non-smoker'), ('Light smoker', 'Light smoker'), ('Regular smoker', 'Regular smoker'), ('Trying to quit', 'Trying to quit')]
DRINKING_CHOICES = [('', 'Select Drinking Habit'), ('Non-drinker', 'Non-drinker'), ('Social drinker', 'Social drinker'), ('Regular drinker', 'Regular drinker')]
MARITAL_CHOICES = [('', 'Select Marital Status'), ('Single', 'Single'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Separated', 'Separated')]
EDUCATION_CHOICES = [('', 'Select Education Level'), ('High School', 'High School'), ('Bachelor Degree', 'Bachelor Degree'), ('Master Degree', 'Master Degree'), ('Doctorate / Ph.D', 'Doctorate / Ph.D'), ('Other', 'Other')]


class MatchProfileForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRIES_LIST, widget=forms.Select(attrs={'class': 'form-select'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    seeking = forms.ChoiceField(choices=SEEKING_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    
    smoking = forms.ChoiceField(choices=SMOKING_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    drinking = forms.ChoiceField(choices=DRINKING_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    marital_status = forms.ChoiceField(choices=MARITAL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    education_level = forms.ChoiceField(choices=EDUCATION_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = MatchProfile
        fields = [
            'full_name', 'email', 'age', 'phone', 'gender', 'seeking',
            'city', 'state', 'zip_code', 'country', 'occupation',
            'height', 'body_type', 'ethnicity', 'marital_status',
            'languages_spoken', 'religion', 'smoking', 'drinking',
            'diet', 'children', 'education_level', 'zodiac_sign',
            'bio', 'profile_image',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State / Region'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip / Postal Code'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Profession / Industry'}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g. 5'10\""}),
            'body_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body Type (e.g. Athletic, Average)'}),
            'ethnicity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ethnicity'}),
            'languages_spoken': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Languages Spoken'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Religion'}),
            'diet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Diet (e.g. Vegetarian, Omnivore)'}),
            'children': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Children (e.g. None, Have kids)'}),
            'zodiac_sign': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zodiac Sign'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = MatchProfile
        fields = [
            'q1_relationship_goal', 'q2_core_values', 'q3_dealbreakers',
            'q4_love_language', 'q5_lifestyle_habits', 'q6_conflict_resolution',
            'q7_future_vision', 'q8_partner_personality', 'q9_communication_preference',
        ]
        widgets = {
            'q1_relationship_goal': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q2_core_values': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q3_dealbreakers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q4_love_language': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q5_lifestyle_habits': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q6_conflict_resolution': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q7_future_vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q8_partner_personality': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'q9_communication_preference': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['sender_email', 'subject', 'message']
        widgets = {
            'sender_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Message...'}),
        }