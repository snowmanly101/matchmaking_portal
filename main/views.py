import random
from django.contrib import messages
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
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
from .models import MatchProfile, SupportTicket, MatchConnection, ChatMessage


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home_view(request):
    support_form = SupportTicketForm()
    form = MatchProfileForm()

    if request.method == 'POST':
        if 'support_submit' in request.POST:
            support_form = SupportTicketForm(request.POST)
            if support_form.is_valid():
                support_form.save()
                messages.success(request, "Your complaint has been sent to customer care. We will respond shortly!")
                return redirect('home')

        elif 'login' in request.POST:
            login_email = request.POST.get('login_email')
            login_password = request.POST.get('login_password')
            
            profile = MatchProfile.objects.filter(email=login_email).first()
            
            if profile and profile.check_password(login_password):
                if profile.is_locked:
                    messages.error(request, f"Access Denied. {profile.lock_reason}")
                    return redirect('home')

                profile.last_login_ip = get_client_ip(request)
                profile.save()
                
                request.session['user_id'] = profile.id
                messages.success(request, "Welcome back!")
                
                if not profile.is_verified:
                    request.session['pending_user_id'] = profile.id
                    return redirect('verify_email')
                elif not profile.is_subscribed:
                    return redirect('card_payment')
                elif profile.status == 'Under Review - Pending Interview':
                    return redirect('portal')
                else:
                    return redirect('questionnaire_step', step=1)
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
                    profile.generate_pin()
                    profile.save()
                    
                    profile.generate_code()
                    
                    # Safe email execution
                    try:
                        send_mail(
                            subject='Your AuraMatch Verification Code',
                            message=f'Hello {profile.full_name},\n\nYour verification code is: {profile.verification_code}',
                            from_email=None,
                            recipient_list=[profile.email],
                            fail_silently=True,
                        )
                    except Exception as email_err:
                        print(f"Email sending bypassed safely: {email_err}")

                    request.session['pending_user_id'] = profile.id
                    return redirect('verify_email')
                except Exception as db_err:
                    messages.error(request, f"An error occurred during registration: {str(db_err)}")
            else:
                error_msg = "Please correct the errors below."
                if form.errors:
                    for field, errors in form.errors.items():
                        error_msg = f"{field}: {errors[0]}"
                        break
                messages.error(request, error_msg)
        
    return render(request, 'main/home.html', {'form': form, 'support_form': support_form})


def verify_email_view(request):
    user_id = request.session.get('pending_user_id') or request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        if entered_code == str(profile.verification_code):
            profile.is_verified = True
            profile.verification_code = ''
            profile.save()
            request.session['user_id'] = profile.id
            if 'pending_user_id' in request.session:
                del request.session['pending_user_id']
            
            return redirect('card_payment')
        else:
            messages.error(request, 'Invalid verification code. Please check your email inbox.')

    return render(request, 'main/verify_email.html', {'profile': profile})


def card_payment_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    CURRENT_MONTHLY_PROMO = "CFEOH2026"

    if request.method == 'POST':
        promo_code = request.POST.get('promo_code', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        
        # Check if the user entered the promo code
        if promo_code:
            if promo_code == CURRENT_MONTHLY_PROMO:
                profile.is_subscribed = True
                profile.used_promo_code = promo_code
                profile.save()
                messages.success(request, "Promo code applied successfully! Welcome aboard.")
                return redirect('questionnaire_step', step=1)
            else:
                messages.error(request, "Invalid promo code. Please try again.")
        
        # Otherwise, check if they are paying with a card
        elif card_number:
            profile.is_subscribed = True
            profile.save()
            messages.success(request, "Payment successful! Let's set up your profile.")
            return redirect('questionnaire_step', step=1)
        else:
            messages.error(request, "Please enter either a valid promo code or your card details.")

    return render(request, 'main/card_payment.html', {'profile': profile})


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        profile = MatchProfile.objects.filter(email=email).first()
        if profile:
            reset_code = str(random.randint(100000, 999999))
            profile.reset_password_code = reset_code
            profile.save()
            
            request.session['reset_profile_id'] = profile.id
            
            try:
                send_mail(
                    subject='Password Reset Code - AuraMatch',
                    message=f'Hello {profile.full_name},\n\nYour password reset code is: {reset_code}',
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Password reset email bypassed safely: {e}")
                
            messages.success(request, "A password reset code has been sent to your email.")
            return redirect('reset_password')
        else:
            messages.error(request, "No account matches this email address.")
            
    return render(request, 'main/forgot_password.html')


def reset_password_view(request):
    profile_id = request.session.get('reset_profile_id')
    if not profile_id:
        return redirect('forgot_password')
        
    profile = get_object_or_404(MatchProfile, id=profile_id)

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        new_password = request.POST.get('new_password')
        
        if entered_code and entered_code == str(profile.reset_password_code):
            if new_password:
                profile.set_password(new_password)
                profile.reset_password_code = ''
                profile.save()
                
                if 'reset_profile_id' in request.session:
                    del request.session['reset_profile_id']
                    
                messages.success(request, "Password successfully updated! You can now log in.")
                return redirect('home')
            else:
                messages.error(request, "Please enter a valid new password.")
        else:
            messages.error(request, "Invalid or expired reset code.")
            
    return render(request, 'main/reset_password.html')


def questionnaire_step_view(request, step):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    if profile.is_locked:
        return redirect('logout')
    if not profile.is_subscribed:
        return redirect('card_payment')

    form_mapping = {
        1: (Question1Form, 'main/questionnaire_step.html'),
        2: (Question2Form, 'main/questionnaire_step.html'),
        3: (Question3Form, 'main/questionnaire_step.html'),
        4: (Question4Form, 'main/questionnaire_step.html'),
        5: (Question5Form, 'main/questionnaire_step.html'),
        6: (Question6Form, 'main/questionnaire_step.html'),
        7: (Question7Form, 'main/questionnaire_step.html'),
        8: (Question8Form, 'main/questionnaire_step.html'),
        9: (Question9Form, 'main/questionnaire_step.html'),
    }

    if step not in form_mapping:
        return redirect('portal')

    form_class, template_name = form_mapping[step]

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if step < 9:
                return redirect('questionnaire_step', step=step + 1)
            else:
                profile.status = 'Under Review - Pending Interview'
                profile.save()
                return redirect('portal')
    else:
        form = form_class(instance=profile)

    context = {'form': form, 'step': step, 'total_steps': 9, 'profile': profile}
    return render(request, template_name, context)


def portal_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    if profile.is_locked:
        return redirect('logout')
    if not profile.is_subscribed:
        return redirect('card_payment')

    if request.method == 'POST':
        partner_pin = request.POST.get('partner_pin')
        partner = MatchProfile.objects.filter(match_pin=partner_pin).first()
        
        if partner and partner != profile:
            connection = MatchConnection.objects.filter(
                (models.Q(user1=profile) & models.Q(user2=partner)) |
                (models.Q(user1=partner) & models.Q(user2=profile))
            ).first()
            
            if not connection:
                connection = MatchConnection.objects.create(user1=profile, user2=partner)
            
            return redirect('chat_room', connection_id=connection.id)
        else:
            messages.error(request, "Invalid Match PIN. Please check and try again.")

    connections = MatchConnection.objects.filter(models.Q(user1=profile) | models.Q(user2=profile))

    return render(request, 'main/portal.html', {'profile': profile, 'connections': connections})


def chat_room_view(request, connection_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    if profile.is_locked:
        return redirect('logout')

    connection = get_object_or_404(MatchConnection, id=connection_id)
    
    if connection.user1 != profile and connection.user2 != profile:
        return redirect('portal')

    partner = connection.user2 if connection.user1 == profile else connection.user1

    if request.method == 'POST':
        text = request.POST.get('message_text')
        image = request.FILES.get('chat_image')
        
        if text or image:
            ChatMessage.objects.create(
                connection=connection,
                sender=profile,
                message_text=text,
                image=image
            )
            profile.refresh_from_db()
            if profile.is_locked:
                messages.error(request, f"Your account has been locked: {profile.lock_reason}")
                return redirect('logout')

        return redirect('chat_room', connection_id=connection.id)

    messages_list = ChatMessage.objects.filter(connection=connection).order_by('sent_at')

    return render(request, 'main/chat_room.html', {
        'profile': profile,
        'partner': partner,
        'connection': connection,
        'messages_list': messages_list
    })


def terms_view(request):
    return render(request, 'main/terms.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')