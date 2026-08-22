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

    # Security IP Tracking (Item 4)
    registration_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)

    # Email Verification Fields
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    # Unique Match PIN for Item 6
    match_pin = models.CharField(max_length=6, unique=True, blank=True, null=True)

    # Account Lock / Scam Detection Flag (Item 7)
    is_locked = models.BooleanField(default=False)
    lock_reason = models.CharField(max_length=255, blank=True, null=True)

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

    def generate_pin(self):
        if not self.match_pin:
            self.match_pin = str(random.randint(10000, 99999))
            self.save()

    def _str_(self):
        return f'{self.full_name} ({self.email})'


# Item 5: Customer Support Tickets
class SupportTicket(models.Model):
    profile = models.ForeignKey(MatchProfile, on_delete=models.CASCADE, null=True, blank=True)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def _str_(self):
        return f"Ticket from {self.sender_email}: {self.subject}"


# Item 6: Match Connection via PIN
class MatchConnection(models.Model):
    user1 = models.ForeignKey(MatchProfile, related_name='connections_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(MatchProfile, related_name='connections_as_user2', on_delete=models.CASCADE)
    connected_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Connection: {self.user1.full_name} & {self.user2.full_name}"


# Item 6 & 7: Chat Messages with Image Sharing & Money Scam Auto-Lock
class ChatMessage(models.Model):
    connection = models.ForeignKey(MatchConnection, on_delete=models.CASCADE)
    sender = models.ForeignKey(MatchProfile, on_delete=models.CASCADE)
    message_text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Item 7: Scam / Money Keyword Auto-Lock Detector
        if self.message_text:
            forbidden_words = ['money', 'send money', 'cash', 'wire', 'crypto', 'gift card', 'loan', 'pay me', 'dollars', 'naira', 'funds']
            text_lower = self.message_text.lower()
            for word in forbidden_words:
                if word in text_lower:
                    # Lock the sender's account instantly
                    sender_profile = self.sender
                    sender_profile.is_locked = True
                    sender_profile.lock_reason = f"Account locked automatically for violating community rules (Trigger word: '{word}')."
                    sender_profile.save()
                    self.message_text = "[MESSAGE BLOCKED & ACCOUNT LOCKED FOR POLICY VIOLATION]"
                    break
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Message from {self.sender.full_name}"