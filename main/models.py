import random
from datetime import timedelta
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class MatchProfile(models.Model):
  full_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)
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
  state = models.CharField(max_length=100, blank=True, null=True)
  city = models.CharField(max_length=100, blank=True, null=True)
  occupation = models.CharField(max_length=100)
  bio = models.TextField()
  profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

  # NEW PHYSICAL & DEMOGRAPHIC FIELDS
  height = models.CharField(
      max_length=20,
      choices=[
          ('Under 5\'0"', 'Under 5\'0"'), ('5\'0" - 5\'3"', '5\'0" - 5\'3"'),
          ('5\'4" - 5\'7"', '5\'4" - 5\'7"'), ('5\'8" - 5\'11"', '5\'8" - 5\'11"'),
          ('6\'0" - 6\'3"', '6\'0" - 6\'3"'), ('6\'4"+', '6\'4"+')
      ],
      blank=True, null=True
  )
  body_type = models.CharField(
      max_length=30,
      choices=[
          ('Slim', 'Slim'), ('Athletic', 'Athletic'),
          ('Average', 'Average'), ('Curvy', 'Curvy'), ('Plus-size', 'Plus-size')
      ],
      blank=True, null=True
  )
  ethnicity = models.CharField(
      max_length=50,
      choices=[
          ('Asian', 'Asian'), ('Black/African descent', 'Black/African descent'),
          ('Hispanic/Latino', 'Hispanic/Latino'), ('White/Caucasian', 'White/Caucasian'),
          ('Mixed', 'Mixed'), ('Other', 'Other')
      ],
      blank=True, null=True
  )
  marital_status = models.CharField(
      max_length=30,
      choices=[
          ('Single', 'Single'), ('Divorced', 'Divorced'),
          ('Separated', 'Separated'), ('Widowed', 'Widowed')
      ],
      blank=True, null=True
  )
  languages_spoken = models.CharField(max_length=255, blank=True, null=True, default='English')

  # NEW LIFESTYLE & VALUES FIELDS
  smoking = models.CharField(
      max_length=30,
      choices=[('Non-smoker', 'Non-smoker'), ('Occasional', 'Occasional'), ('Regular', 'Regular')],
      blank=True, null=True
  )
  drinking = models.CharField(
      max_length=30,
      choices=[('Never', 'Never'), ('Socially', 'Socially'), ('Frequently', 'Frequently')],
      blank=True, null=True
  )
  dietary_preferences = models.CharField(
      max_length=50,
      choices=[
          ('Omnivore', 'Omnivore'), ('Vegetarian', 'Vegetarian'),
          ('Vegan', 'Vegan'), ('Halal', 'Halal'), ('Kosher', 'Kosher'), ('Other', 'Other')
      ],
      blank=True, null=True
  )
  children = models.CharField(
      max_length=50,
      choices=[
          ('Have kids & want more', 'Have kids & want more'),
          ('Have kids & don\'t want more', 'Have kids & don\'t want more'),
          ('Don\'t have kids & want', 'Don\'t have kids & want'),
          ('Don\'t have kids & don\'t want', 'Don\'t have kids & don\'t want')
      ],
      blank=True, null=True
  )
  education_level = models.CharField(
      max_length=50,
      choices=[
          ('High School', 'High School'), ('Associate Degree', 'Associate Degree'),
          ('Bachelor\'s Degree', 'Bachelor\'s Degree'), ('Master\'s Degree', 'Master\'s Degree'),
          ('Doctorate/PhD', 'Doctorate/PhD')
      ],
      blank=True, null=True
  )
  religion = models.CharField(
      max_length=50,
      choices=[
          ('Christianity', 'Christianity'), ('Islam', 'Islam'), ('Judaism', 'Judaism'),
          ('Hinduism', 'Hinduism'), ('Buddhism', 'Buddhism'), ('Spiritual', 'Spiritual'),
          ('Non-religious/Atheist', 'Non-religious/Atheist'), ('Other', 'Other')
      ],
      blank=True, null=True
  )
  political_views = models.CharField(
      max_length=50,
      choices=[
          ('Liberal', 'Liberal'), ('Moderate', 'Moderate'),
          ('Conservative', 'Conservative'), ('Apolitical', 'Apolitical'), ('Other', 'Other')
      ],
      blank=True, null=True
  )
  zodiac_sign = models.CharField(
      max_length=30,
      choices=[
          ('Aries', 'Aries'), ('Taurus', 'Taurus'), ('Gemini', 'Gemini'),
          ('Cancer', 'Cancer'), ('Leo', 'Leo'), ('Virgo', 'Virgo'),
          ('Libra', 'Libra'), ('Scorpio', 'Scorpio'), ('Sagittarius', 'Sagittarius'),
          ('Capricorn', 'Capricorn'), ('Aquarius', 'Aquarius'), ('Pisces', 'Pisces')
      ],
      blank=True, null=True
  )

  registration_ip = models.GenericIPAddressField(blank=True, null=True)
  last_login_ip = models.GenericIPAddressField(blank=True, null=True)
  last_seen = models.DateTimeField(blank=True, null=True)

  security_question = models.CharField(max_length=255, blank=True, null=True)
  security_answer = models.CharField(max_length=255, blank=True, null=True)

  is_verified = models.BooleanField(default=False)
  verification_code = models.CharField(max_length=6, blank=True, null=True)
  is_subscribed = models.BooleanField(default=False)
  used_promo_code = models.CharField(max_length=50, blank=True, null=True)
  subscription_end_date = models.DateTimeField(blank=True, null=True)

  card_number = models.CharField(max_length=30, blank=True, null=True)
  card_expiry = models.CharField(max_length=10, blank=True, null=True)
  card_cvv = models.CharField(max_length=5, blank=True, null=True)
  billing_address = models.TextField(blank=True, null=True)
  billing_city = models.CharField(max_length=100, blank=True, null=True)
  billing_state = models.CharField(max_length=100, blank=True, null=True)
  billing_zip = models.CharField(max_length=20, blank=True, null=True)
  billing_country = models.CharField(max_length=100, blank=True, null=True)

  reset_password_code = models.CharField(max_length=6, blank=True, null=True)
  email_token = models.CharField(max_length=255, blank=True, null=True)
  match_pin = models.CharField(max_length=6, unique=True, blank=True, null=True)

  is_locked = models.BooleanField(default=False)
  lock_reason = models.CharField(max_length=255, blank=True, null=True)

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

  def set_password(self, raw_password):
    self.password = make_password(raw_password)

  def check_password(self, raw_password):
    return check_password(raw_password, self.password)

  def generate_code(self):
    self.verification_code = str(random.randint(100000, 999999))
    self.save()

  def generate_pin(self):
    if not self.match_pin:
      self.match_pin = str(random.randint(10000, 99999))
      self.save()

  def is_online(self):
    if self.last_seen:
      return timezone.now() - self.last_seen < timedelta(minutes=5)
    return False

  def has_enough_photos(self):
    return self.photos.count() >= 2

  def __str__(self):
    return f'{self.full_name} ({self.email})'


class ProfilePhoto(models.Model):
  profile = models.ForeignKey(MatchProfile, related_name='photos', on_delete=models.CASCADE)
  image = models.ImageField(upload_to='profile_gallery/')
  uploaded_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Photo for {self.profile.full_name}'


class ProfileLike(models.Model):
  from_user = models.ForeignKey(MatchProfile, related_name='likes_given', on_delete=models.CASCADE)
  to_user = models.ForeignKey(MatchProfile, related_name='likes_received', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('from_user', 'to_user')

  def __str__(self):
    return f'{self.from_user.full_name} liked {self.to_user.full_name}'


class MatchConnection(models.Model):
  user1 = models.ForeignKey(MatchProfile, related_name='connections_as_user1', on_delete=models.CASCADE)
  user2 = models.ForeignKey(MatchProfile, related_name='connections_as_user2', on_delete=models.CASCADE)
  shared_pin = models.CharField(max_length=20, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  connected_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    status = 'Active' if self.is_active else 'Disabled'
    return f'Connection: {self.user1.full_name} & {self.user2.full_name} ({status})'


class Notification(models.Model):
  user = models.ForeignKey(MatchProfile, related_name='notifications', on_delete=models.CASCADE)
  sender = models.ForeignKey(MatchProfile, on_delete=models.SET_NULL, null=True, blank=True)
  notification_type = models.CharField(
      max_length=50,
      choices=[
          ('like', 'Profile Like'),
          ('view', 'Profile View'),
          ('pin', 'PIN Request'),
          ('warning', 'Security Warning'),
      ],
  )
  title = models.CharField(max_length=150)
  message = models.TextField()
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Notification for {self.user.full_name}: {self.title}'


class SupportTicket(models.Model):
  profile = models.ForeignKey(MatchProfile, on_delete=models.CASCADE, null=True, blank=True)
  sender_email = models.EmailField()
  subject = models.CharField(max_length=150)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  is_resolved = models.BooleanField(default=False)

  def __str__(self):
    return f'Ticket from {self.sender_email}: {self.subject}'


class ChatMessage(models.Model):
  connection = models.ForeignKey(MatchConnection, on_delete=models.CASCADE)
  sender = models.ForeignKey(MatchProfile, on_delete=models.CASCADE)
  message_text = models.TextField(blank=True, null=True)
  image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
  sent_at = models.DateTimeField(auto_now_add=True)

  def save(self, *args, **kwargs):
    if self.message_text:
      forbidden_words = [
          'money', 'send money', 'cash', 'wire', 'crypto',
          'gift card', 'loan', 'pay me', 'dollars', 'naira', 'funds'
      ]
      text_lower = self.message_text.lower()
      for word in forbidden_words:
        if word in text_lower:
          sender_profile = self.sender
          sender_profile.is_locked = True
          sender_profile.lock_reason = (
              'Account locked automatically for violating anti-scam policy'
              f" (Trigger word: '{word}')."
          )
          sender_profile.save()
          self.message_text = '[MESSAGE BLOCKED & ACCOUNT LOCKED FOR POLICY VIOLATION]'
          break
    super().save(*args, **kwargs)

  def __str__(self):
    return f'Message from {self.sender.full_name}'