import os
import random
import uuid
import requests
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    MatchProfileForm,
    SupportTicketForm,
    Question1Form,
    Question2Form,
    Question3Form,
    Question4Form,
    Question5Form,
    Question6Form,
    Question7Form,
    Question8Form,
    Question9Form,
)
from .models import (
    MatchProfile,
    SupportTicket,
    MatchConnection,
    ChatMessage,
    ProfilePhoto,
    ProfileLike,
    Notification,
)

AFRICAN_COUNTRIES = [
    'Nigeria', 'Ghana', 'Kenya', 'South Africa', 'Egypt', 'Morocco', 'Algeria',
    'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde',
    'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Djibouti', 'Equatorial Guinea',
    'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Guinea', 'Guinea-Bissau',
    'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania',
    'Mauritius', 'Mozambique', 'Namibia', 'Niger', 'Rwanda', 'Sao Tome and Principe',
    'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Sudan', 'Sudan',
    'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
]

def check_is_african_ip(ip_address):
  if not ip_address or ip_address in ['127.0.0.1', 'localhost', '::1']:
    return False
  try:
    response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=3)
    data = response.json()
    if data.get('status') == 'success':
      if data.get('country') in AFRICAN_COUNTRIES:
        return True
  except Exception:
    pass
  return False


def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip


def update_last_seen(profile):
  profile.last_seen = timezone.now()
  profile.save(update_fields=['last_seen'])


def create_bot_welcome_message(new_user):
  bot_profile, created = MatchProfile.objects.get_or_create(
      email='bot@auramatch.forum',
      defaults={
          'full_name': '🤖 AuraMatch Guide',
          'age': 25,
          'occupation': 'Official Platform Guide',
          'bio': 'I am your automated guide to help you navigate AuraMatch securely!',
          'gender': 'Female',
          'seeking': 'Female',
          'country': 'United States',
          'is_verified': True,
      },
  )
  if bot_profile.country != 'United States':
    bot_profile.country = 'United States'
    bot_profile.save()

  if not bot_profile.match_pin:
    bot_profile.generate_pin()

  conn, _ = MatchConnection.objects.get_or_create(
      user1=bot_profile,
      user2=new_user,
      defaults={'shared_pin': 'AUTO', 'is_active': True},
  )

  if not ChatMessage.objects.filter(connection=conn).exists():
    ChatMessage.objects.create(
        connection=conn,
        sender=bot_profile,
        message_text=(
            f'Welcome to AuraMatch, {new_user.full_name}! 👋\n\n'
            '⚠️ IMPORTANT PLATFORM SAFETY RULES:\n'
            '1. Talking about money, cash, wire transfers, loans, or crypto is STRICTLY PROHIBITED and locks accounts instantly.\n'
            '2. Stay permanently on this platform to chat and evaluate your match’s genuineness before moving elsewhere.\n'
            '3. Use your Match PIN securely to connect with verified members.'
        ),
    )


def home_view(request):
  support_form = SupportTicketForm()
  form = MatchProfileForm()

  if request.method == 'POST':
    if 'support_submit' in request.POST:
      support_form = SupportTicketForm(request.POST)
      if support_form.is_valid():
        support_form.save()
        messages.success(request, 'Your complaint has been sent. We will respond shortly!')
        return redirect('home')

    elif 'login' in request.POST:
      login_email = request.POST.get('login_email')
      login_password = request.POST.get('login_password')
      profile = MatchProfile.objects.filter(email=login_email).first()

      if profile and profile.check_password(login_password):
        if profile.is_locked:
          messages.error(request, f'Access Denied. {profile.lock_reason}')
          return redirect('home')

        profile.last_login_ip = get_client_ip(request)
        update_last_seen(profile)
        request.session['user_id'] = profile.id
        messages.success(request, 'Welcome back!')
        return redirect('portal')
      else:
        messages.error(request, 'Invalid email or password. Please try again.')
        return redirect('home')

    elif 'register' in request.POST:
      client_ip = get_client_ip(request)
      if check_is_african_ip(client_ip):
        messages.error(request, 'Registration restricted: Traffic from African IP regions violates our platform privacy policy.')
        return redirect('home')

      form = MatchProfileForm(request.POST, request.FILES)
      raw_password = request.POST.get('password')

      if form.is_valid() and raw_password:
        email = form.cleaned_data.get('email')
        if MatchProfile.objects.filter(email=email).exists():
          messages.error(request, 'An account with this email already exists. Please log in.')
          return redirect('home')

        try:
          profile = form.save(commit=False)
          profile.set_password(raw_password)
          profile.registration_ip = client_ip
          profile.last_login_ip = client_ip
          profile.is_verified = True
          profile.save()

          if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES.get('profile_image')
            profile.save()

          create_bot_welcome_message(profile)
          request.session['user_id'] = profile.id
          messages.success(request, 'Account created successfully! Welcome to your dashboard.')
          return redirect('portal')
        except Exception as db_err:
          messages.error(request, f'An error occurred: {str(db_err)}')
      else:
        messages.error(request, 'Please correct the registration errors below.')

  return render(request, 'main/home.html', {'form': form, 'support_form': support_form})


def verify_email_view(request):
  user_id = request.session.get('pending_user_id') or request.session.get('user_id')
  if not user_id:
    return redirect('home')
  profile = get_object_or_404(MatchProfile, id=user_id)
  profile.is_verified = True
  profile.save()
  request.session['user_id'] = profile.id
  return redirect('portal')


def upload_photos_view(request):
  user_id = request.session.get('user_id') or request.session.get('pending_user_id')
  if not user_id:
    return redirect('home')
  profile = get_object_or_404(MatchProfile, id=user_id)

  if request.method == 'POST':
    if 'delete_photo_id' in request.POST:
      photo = ProfilePhoto.objects.filter(id=request.POST.get('delete_photo_id'), profile=profile).first()
      if photo:
        photo.delete()
        messages.success(request, 'Photo deleted successfully!')
      return redirect('upload_photos')
    elif 'main_profile_image' in request.FILES:
      profile.profile_image = request.FILES.get('main_profile_image')
      profile.save()
      messages.success(request, 'Main profile picture updated successfully!')
      return redirect('upload_photos')
    elif 'photos' in request.FILES:
      images = request.FILES.getlist('photos')
      if images:
        for img in images:
          ProfilePhoto.objects.create(profile=profile, image=img)
        messages.success(request, f'{len(images)} photo(s) uploaded successfully!')
        return redirect('upload_photos')

  return render(request, 'main/upload_photos.html', {'profile': profile})


def card_payment_view(request):
  return redirect('portal')


def forgot_password_view(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    profile = MatchProfile.objects.filter(email=email).first()
    if profile:
      reset_code = str(random.randint(100000, 999999))
      profile.reset_password_code = reset_code
      profile.save()
      request.session['reset_profile_id'] = profile.id
      messages.success(request, f'Password reset code generated: {reset_code}')
      return redirect('reset_password')
    else:
      messages.error(request, 'No account matches this email address.')
  return render(request, 'main/forgot_password.html')


def reset_password_view(request):
  profile_id = request.session.get('reset_profile_id')
  if not profile_id:
    return redirect('forgot_password')
  profile = get_object_or_404(MatchProfile, id=profile_id)

  if request.method == 'POST':
    entered_code = request.POST.get('code')
    new_password = request.POST.get('new_password')
    if entered_code and entered_code.strip() == str(profile.reset_password_code):
      if new_password:
        profile.set_password(new_password)
        profile.reset_password_code = ''
        profile.save()
        messages.success(request, 'Password successfully updated! You can now log in.')
        return redirect('home')
    messages.error(request, 'Invalid code or password.')
  return render(request, 'main/reset_password.html')


def questionnaire_step_view(request, step):
  return redirect('portal')


def portal_view(request):
  user_id = request.session.get('user_id')
  if not user_id:
    return redirect('home')

  profile = get_object_or_404(MatchProfile, id=user_id)
  if profile.is_locked:
    return redirect('logout')

  update_last_seen(profile)
  if not profile.match_pin:
    profile.generate_pin()

  # AUTOMATED MONTHLY SAFETY WARNING PUSH TO MAILBOX INBOX
  last_warning = Notification.objects.filter(
      user=profile, notification_type='warning'
  ).order_by('-created_at').first()

  if not last_warning or (timezone.now() - last_warning.created_at) > timedelta(days=30):
    Notification.objects.create(
        user=profile,
        notification_type='warning',
        title='⚠️ Monthly Platform Safety Reminder',
        message=(
            'Important Security Notice: Talking about money, cash, wire transfers, '
            'or crypto is strictly prohibited and leads to immediate permanent account locking. '
            'Please keep all chats on AuraMatch to verify genuineness.'
        )
    )

  if request.method == 'POST' and 'update_bio' in request.POST:
    profile.bio = request.POST.get('bio', profile.bio)
    profile.city = request.POST.get('city', profile.city)
    profile.state = request.POST.get('state', profile.state)
    profile.save()
    messages.success(request, 'Your profile info has been updated successfully!')
    return redirect('portal')

  if request.method == 'POST' and 'send_pin_request' in request.POST:
    target_user = get_object_or_404(MatchProfile, id=request.POST.get('target_user_id'))
    conn = MatchConnection.objects.filter(
        (models.Q(user1=profile) & models.Q(user2=target_user)) |
        (models.Q(user1=target_user) & models.Q(user2=profile))
    ).first()

    if not conn:
      MatchConnection.objects.create(user1=profile, user2=target_user, shared_pin=profile.match_pin, is_active=False)
      Notification.objects.create(
          user=target_user, sender=profile, notification_type='pin', title='🔑 New PIN Request', message=f'{profile.full_name} requested to connect with your Match PIN!'
      )
      messages.success(request, f'PIN Request sent to {target_user.full_name}!')
    else:
      messages.info(request, 'A request or connection already exists.')
    return redirect('portal')

  if request.method == 'POST' and 'approve_connection_id' in request.POST:
    conn = get_object_or_404(MatchConnection, id=request.POST.get('approve_connection_id'))
    if conn.user2 == profile or conn.user1 == profile:
      conn.is_active = True
      conn.save()
      messages.success(request, 'PIN Approved! Chat and full profile unlocked.')
      return redirect('chat_room', connection_id=conn.id)

  if request.method == 'POST' and 'decline_connection_id' in request.POST:
    conn = get_object_or_404(MatchConnection, id=request.POST.get('decline_connection_id'))
    if conn.user2 == profile or conn.user1 == profile:
      conn.delete()
      messages.info(request, 'PIN Request declined.')
    return redirect('portal')

  if request.method == 'POST' and 'partner_pin' in request.POST:
    partner_pin = request.POST.get('partner_pin')
    partner = MatchProfile.objects.filter(match_pin=partner_pin).first()

    if partner and partner != profile:
      connection, _ = MatchConnection.objects.get_or_create(
          user1=profile, user2=partner, defaults={'shared_pin': partner_pin, 'is_active': True}
      )
      connection.is_active = True
      connection.shared_pin = partner_pin
      connection.save()
      messages.success(request, f'Connected with {partner.full_name}!')
      return redirect('chat_room', connection_id=connection.id)
    else:
      messages.error(request, 'Invalid Match PIN.')

  all_users = MatchProfile.objects.exclude(id=profile.id).exclude(email='bot@auramatch.forum').filter(is_locked=False)
  five_mins_ago = timezone.now() - timedelta(minutes=5)
  active_users = [u for u in all_users]
  online_count = MatchProfile.objects.filter(last_seen__gte=five_mins_ago).count()
  active_connections = MatchConnection.objects.filter((models.Q(user1=profile) | models.Q(user2=profile)) & models.Q(is_active=True))
  pending_requests = MatchConnection.objects.filter(user2=profile, is_active=False)
  notifications = Notification.objects.filter(user=profile).order_by('-created_at')[:15]

  return render(request, 'main/portal.html', {
      'profile': profile,
      'active_users': active_users,
      'connections': active_connections,
      'pending_requests': pending_requests,
      'notifications': notifications,
      'online_count': online_count,
  })


def view_profile_detail(request, profile_id):
  user_id = request.session.get('user_id')
  if not user_id:
    return redirect('home')

  profile = get_object_or_404(MatchProfile, id=user_id)
  target_profile = get_object_or_404(MatchProfile, id=profile_id)
  update_last_seen(profile)

  if profile != target_profile:
    Notification.objects.create(
        user=target_profile, sender=profile, notification_type='view', title='👀 Profile View', message=f'{profile.full_name} viewed your profile!'
    )

  connection = MatchConnection.objects.filter(
      (models.Q(user1=profile) & models.Q(user2=target_profile)) |
      (models.Q(user1=target_profile) & models.Q(user2=profile))
  ).first()

  return render(request, 'main/profile_detail.html', {
      'profile': profile,
      'target_profile': target_profile,
      'connection': connection,
      'can_see_questionnaire': (connection and connection.is_active) or (profile == target_profile),
  })


def toggle_like_view(request, profile_id):
  user_id = request.session.get('user_id')
  if not user_id:
    return redirect('home')

  profile = get_object_or_404(MatchProfile, id=user_id)
  target_profile = get_object_or_404(MatchProfile, id=profile_id)

  if profile != target_profile:
    like_obj = ProfileLike.objects.filter(from_user=profile, to_user=target_profile).first()
    if like_obj:
      like_obj.delete()
      messages.info(request, f'Unliked {target_profile.full_name}.')
    else:
      ProfileLike.objects.create(from_user=profile, to_user=target_profile)
      Notification.objects.create(
          user=target_profile, sender=profile, notification_type='like', title='❤️ New Profile Like', message=f'{profile.full_name} liked your profile!'
      )
      messages.success(request, f'You liked {target_profile.full_name}!')

  return redirect('view_profile', profile_id=target_profile.id)


def share_pin_view(request, profile_id):
  return redirect('view_profile', profile_id=profile_id)


def chat_room_view(request, connection_id):
  user_id = request.session.get('user_id')
  if not user_id:
    return redirect('home')

  profile = get_object_or_404(MatchProfile, id=user_id)
  if profile.is_locked:
    return redirect('logout')

  update_last_seen(profile)
  connection = get_object_or_404(MatchConnection, id=connection_id)

  if connection.user1 != profile and connection.user2 != profile:
    return redirect('portal')

  partner = connection.user2 if connection.user1 == profile else connection.user1

  if request.method == 'POST':
    text = request.POST.get('message_text')
    image = request.FILES.get('chat_image')
    if text or image:
      ChatMessage.objects.create(connection=connection, sender=profile, message_text=text, image=image)
    return redirect('chat_room', connection_id=connection.id)

  messages_list = ChatMessage.objects.filter(connection=connection).order_by('sent_at')

  return render(request, 'main/chat_room.html', {
      'profile': profile,
      'partner': partner,
      'connection': connection,
      'messages_list': messages_list,
  })


def terms_view(request):
  return render(request, 'main/terms.html')


def logout_view(request):
  request.session.flush()
  return redirect('home')