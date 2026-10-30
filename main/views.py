import os
import random
import uuid
from datetime import timedelta
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
)


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

                if not profile.is_verified:
                    request.session['pending_user_id'] = profile.id
                    return redirect('verify_email')
                
                return redirect('portal')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
                return redirect('home')

        elif 'register' in request.POST:
            form = MatchProfileForm(request.POST, request.FILES)
            raw_password = request.POST.get('password')

            if form.is_valid() and raw_password:
                email = form.cleaned_data.get('email')

                existing_profile = MatchProfile.objects.filter(email=email).first()
                if existing_profile:
                    messages.error(request, 'An account with this email already exists. Please log in below.')
                    return render(request, 'main/home.html', {'form': form, 'support_form': support_form})

                try:
                    profile = form.save(commit=False)
                    profile.set_password(raw_password)
                    profile.registration_ip = get_client_ip(request)
                    profile.last_login_ip = get_client_ip(request)

                    profile.favorite_music = request.POST.get('favorite_music', '')
                    profile.interests = request.POST.get('interests', '')

                    verification_code = str(random.randint(100000, 999999))
                    profile.verification_code = verification_code
                    profile.is_verified = True
                    profile.save()

                    if request.FILES.get('profile_image'):
                        profile.profile_image = request.FILES.get('profile_image')
                        profile.save()

                    request.session['user_id'] = profile.id
                    messages.success(request, 'Account created successfully! Welcome to your dashboard.')
                    return redirect('portal')

                except Exception as db_err:
                    messages.error(request, f'An error occurred: {str(db_err)}')
            else:
                error_msg = 'Please correct the errors below.'
                if form.errors:
                    for field, errors in form.errors.items():
                        error_msg = f'{field}: {errors[0]}'
                        break
                messages.error(request, error_msg)

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
        images = request.FILES.getlist('photos')
        for img in images:
            ProfilePhoto.objects.create(profile=profile, image=img)
        if not profile.profile_image and profile.photos.exists():
            profile.profile_image = profile.photos.first().image
            profile.save()
        messages.success(request, 'Photos uploaded successfully!')
        return redirect('portal')

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

    # Update Bio, Favorite Music, and Hobbies
    if request.method == 'POST' and 'update_bio' in request.POST:
        new_bio = request.POST.get('bio')
        fav_music = request.POST.get('fav_music')
        interests = request.POST.get('interests')

        if new_bio is not None:
            profile.bio = new_bio
        if fav_music is not None:
            profile.favorite_music = fav_music
        if interests is not None:
            profile.interests = interests

        profile.save()
        messages.success(request, 'Your profile info has been updated successfully!')
        return redirect('portal')

    # Send PIN Request
    if request.method == 'POST' and 'send_pin_request' in request.POST:
        target_id = request.POST.get('target_user_id')
        target_user = get_object_or_404(MatchProfile, id=target_id)

        conn = MatchConnection.objects.filter(
            (models.Q(user1=profile) & models.Q(user2=target_user))
            | (models.Q(user1=target_user) & models.Q(user2=profile))
        ).first()

        if not conn:
            MatchConnection.objects.create(
                user1=profile, user2=target_user, shared_pin=profile.match_pin, is_active=False
            )
            messages.success(request, f'PIN Request sent to {target_user.full_name}!')
        else:
            messages.info(request, 'A request or connection already exists.')
        return redirect('portal')

    # Approve PIN Request
    if request.method == 'POST' and 'approve_connection_id' in request.POST:
        conn_id = request.POST.get('approve_connection_id')
        conn = get_object_or_404(MatchConnection, id=conn_id)
        if conn.user2 == profile or conn.user1 == profile:
            conn.is_active = True
            conn.save()
            messages.success(request, 'PIN Approved! Chat and full profile unlocked.')
            return redirect('chat_room', connection_id=conn.id)

    # Decline PIN Request
    if request.method == 'POST' and 'decline_connection_id' in request.POST:
        conn_id = request.POST.get('decline_connection_id')
        conn = get_object_or_404(MatchConnection, id=conn_id)
        if conn.user2 == profile or conn.user1 == profile:
            conn.delete()
            messages.info(request, 'PIN Request declined.')
            return redirect('portal')

    # Connect directly via Partner PIN
    if request.method == 'POST' and 'partner_pin' in request.POST:
        partner_pin = request.POST.get('partner_pin')
        partner = MatchProfile.objects.filter(match_pin=partner_pin).first()

        if partner and partner != profile:
            connection = MatchConnection.objects.filter(
                (models.Q(user1=profile) & models.Q(user2=partner))
                | (models.Q(user1=partner) & models.Q(user2=profile))
            ).first()

            if not connection:
                connection = MatchConnection.objects.create(
                    user1=profile, user2=partner, shared_pin=partner_pin, is_active=True
                )
            else:
                connection.is_active = True
                connection.shared_pin = partner_pin
                connection.save()

            messages.success(request, f'Connected with {partner.full_name}!')
            return redirect('chat_room', connection_id=connection.id)
        else:
            messages.error(request, 'Invalid Match PIN.')

    all_users = MatchProfile.objects.exclude(id=profile.id).filter(is_locked=False)

    query = request.GET.get('q', '')
    gender_filter = request.GET.get('gender', '')

    if query:
        all_users = all_users.filter(
            models.Q(full_name__icontains=query)
            | models.Q(occupation__icontains=query)
            | models.Q(country__icontains=query)
            | models.Q(bio__icontains=query)
            | models.Q(favorite_music__icontains=query)
            | models.Q(interests__icontains=query)
        )

    if gender_filter:
        all_users = all_users.filter(gender=gender_filter)

    five_mins_ago = timezone.now() - timedelta(minutes=5)
    
    active_users = []
    for u in all_users:
        u.is_online = u.last_seen and u.last_seen >= five_mins_ago
        active_users.append(u)

    online_count = MatchProfile.objects.filter(last_seen__gte=five_mins_ago).count()

    active_connections = MatchConnection.objects.filter(
        (models.Q(user1=profile) | models.Q(user2=profile)) & models.Q(is_active=True)
    )

    # CRITICAL: Target incoming requests where user2 is the current profile
    pending_requests = MatchConnection.objects.filter(
        user2=profile, is_active=False
    )

    return render(
        request,
        'main/portal.html',
        {
            'profile': profile,
            'active_users': active_users,
            'connections': active_connections,
            'pending_requests': pending_requests,
            'online_count': online_count,
            'query': query,
            'gender_filter': gender_filter,
        },
    )


def view_profile_detail(request, profile_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    target_profile = get_object_or_404(MatchProfile, id=profile_id)
    update_last_seen(profile)

    connection = MatchConnection.objects.filter(
        (models.Q(user1=profile) & models.Q(user2=target_profile))
        | (models.Q(user1=target_profile) & models.Q(user2=profile))
    ).first()

    can_see_questionnaire = (connection and connection.is_active) or (profile == target_profile)

    has_liked = ProfileLike.objects.filter(
        from_user=profile, to_user=target_profile
    ).exists()

    return render(
        request,
        'main/profile_detail.html',
        {
            'profile': profile,
            'target_profile': target_profile,
            'has_liked': has_liked,
            'connection': connection,
            'can_see_questionnaire': can_see_questionnaire,
        },
    )


def toggle_like_view(request, profile_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    target_profile = get_object_or_404(MatchProfile, id=profile_id)

    if profile != target_profile:
        like_obj = ProfileLike.objects.filter(
            from_user=profile, to_user=target_profile
        ).first()
        if like_obj:
            like_obj.delete()
            messages.info(request, f'Unliked {target_profile.full_name}.')
        else:
            ProfileLike.objects.create(from_user=profile, to_user=target_profile)
            messages.success(request, f'You liked {target_profile.full_name}!')
            
            if target_profile.email:
                try:
                    send_mail(
                        'Someone liked your profile on AuraMatch!',
                        f'{profile.full_name} liked your profile. Log in to check them out!',
                        'noreply@auramatch.forum',
                        [target_profile.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

    return redirect('view_profile', profile_id=target_profile.id)


def share_pin_view(request, profile_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    target_profile = get_object_or_404(MatchProfile, id=profile_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        entered_pin = request.POST.get('pin_code')

        connection = MatchConnection.objects.filter(
            (models.Q(user1=profile) & models.Q(user2=target_profile))
            | (models.Q(user1=target_profile) & models.Q(user2=profile))
        ).first()

        if action == 'disable':
            if connection:
                connection.is_active = False
                connection.save()
                messages.info(request, 'Connection disabled.')
        elif action == 'share':
            if entered_pin and entered_pin.strip() == str(target_profile.match_pin):
                if not connection:
                    connection = MatchConnection.objects.create(
                        user1=profile,
                        user2=target_profile,
                        shared_pin=entered_pin,
                        is_active=True,
                    )
                else:
                    connection.is_active = True
                    connection.shared_pin = entered_pin
                    connection.save()
                messages.success(request, 'PIN Approved! Full profile and chat unlocked.')
                return redirect('chat_room', connection_id=connection.id)
            else:
                messages.error(request, 'Invalid Match PIN entered.')

    return redirect('view_profile', profile_id=target_profile.id)


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

    if not connection.is_active:
        messages.error(request, 'This chat connection is not active.')
        return redirect('portal')

    partner = connection.user2 if connection.user1 == profile else connection.user1

    if request.method == 'POST':
        text = request.POST.get('message_text')
        image = request.FILES.get('chat_image')

        if text or image:
            ChatMessage.objects.create(
                connection=connection, sender=profile, message_text=text, image=image
            )
        return redirect('chat_room', connection_id=connection.id)

    messages_list = ChatMessage.objects.filter(connection=connection).order_by('sent_at')

    return render(
        request,
        'main/chat_room.html',
        {
            'profile': profile,
            'partner': partner,
            'connection': connection,
            'messages_list': messages_list,
            'requires_upgrade': False,
        },
    )


def terms_view(request):
    return render(request, 'main/terms.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')