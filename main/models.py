import random
from django.db import models


class MatchProfile(models.Model):
  # Step 1: Initial Registration Fields
  full_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  age = models.IntegerField()
  phone = models.CharField(max_length=30)
  gender = models.CharField(
      max_length=20,
      choices=[('Male', 'Male'), ('Female', 'Female')],
      default='Male',
  )
  seeking = models.CharField(
      max_length=20,
      choices=[
          ('Female', 'Female (Seeking Women)'),
          ('Male', 'Male (Seeking Men)'),
      ],
      default='Female',
  )
  country = models.CharField(max_length=100)
  occupation = models.CharField(max_length=100)
  bio = models.TextField()
  profile_image = models.ImageField(
      upload_to='profiles/', blank=True, null=True
  )

  # Email Verification Fields
  is_verified = models.BooleanField(default=False)
  verification_code = models.CharField(max_length=6, blank=True, null=True)

  # Step 2: The 9 Questionnaire Fields
  q1_relationship_goal = models.TextField(blank=True, null=True)
  q2_core_values = models.TextField(blank=True, null=True)
  q3_dealbreakers = models.TextField(blank=True, null=True)
  q4_love_language = models.TextField(blank=True, null=True)
  q5_lifestyle_habits = models.TextField(blank=True, null=True)
  q6_conflict_resolution = models.TextField(blank=True, null=True)
  q7_future_vision = models.TextField(blank=True, null=True)
  q8_partner_personality = models.TextField(blank=True, null=True)
  q9_communication_preference = models.TextField(blank=True, null=True)

  status = models.CharField(max_length=50, default='Pending Interview')
  created_at = models.DateTimeField(auto_now_add=True)

  def generate_code(self):
    self.verification_code = str(random.randint(100000, 999999))
    self.save()

  def _str_(self):
    return f'{self.full_name} ({self.email})'