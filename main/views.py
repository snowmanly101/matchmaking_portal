from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from .forms import (
    MatchProfileForm,
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
from .models import MatchProfile

def home_view(request):
    if request.method == 'POST':
        # Handle Returning User Quick Login
        if 'login' in request.POST:
            login_email = request.POST.get('login_email')
            profile = MatchProfile.objects.filter(email=login_email).first()
            
            if profile:
                # Log them into the session
                request.session['user_id'] = profile.id
                messages.success(request, "Welcome back!")
                
                # Check their progress and route them appropriately
                if not profile.is_verified:
                    request.session['pending_user_id'] = profile.id
                    return redirect('verify_email')
                elif profile.status == 'Under Review - Pending Interview' or getattr(profile, 'questionnaire_completed', False):
                    return redirect('portal')
                else:
                    return redirect('questionnaire_step', step=1)
            else:
                messages.error(request, 'No account found with this email address. Please register.')
                return redirect('home')

        # Handle New User Registration Form
        elif 'register' in request.POST:
            form = MatchProfileForm(request.POST, request.FILES)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                
                # Check if email already exists
                existing_profile = MatchProfile.objects.filter(email=email).first()
                if existing_profile:
                    request.session['user_id'] = existing_profile.id
                    request.session['pending_user_id'] = existing_profile.id
                    messages.info(request, 'An account with this email already exists. Logging you in...')
                    
                    if not existing_profile.is_verified:
                        return redirect('verify_email')
                    elif existing_profile.status == 'Under Review - Pending Interview':
                        return redirect('portal')
                    else:
                        return redirect('questionnaire_step', step=1)
                
                profile = form.save()
                
                # Generate verification code if method exists
                if hasattr(profile, 'generate_code'):
                    profile.generate_code()
                
                # Attempt to send email verification code
                try:
                    send_mail(
                        subject='Your AuraMatch Verification Code',
                        message=(
                            f'Hello {profile.full_name},\n\nYour verification code is:\n'
                            f'{profile.verification_code}\nEnter this code on the '
                            'verification page to proceed to your matchmaker questionnaire.'
                        ),
                        from_email='auramatchdate@gmail.com',
                        recipient_list=[profile.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

                # Store user ID in session for verification tracking
                request.session['pending_user_id'] = profile.id
                return redirect('verify_email')
    else:
        form = MatchProfileForm()
        
    return render(request, 'main/home.html', {'form': form})

def verify_email_view(request):
    user_id = request.session.get('pending_user_id') or request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        if entered_code == str(profile.verification_code):
            profile.is_verified = True
            profile.save()
            request.session['user_id'] = profile.id
            if 'pending_user_id' in request.session:
                del request.session['pending_user_id']
            return redirect('questionnaire_step', step=1)
        else:
            messages.error(
                request,
                'Invalid verification code. Please check and try again.'
            )

    return render(request, 'main/verify_email.html', {'profile': profile})

def questionnaire_step_view(request, step):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)

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

    context = {
        'form': form,
        'step': step,
        'total_steps': 9,
        'profile': profile,
    }
    return render(request, template_name, context)

def portal_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')

    profile = get_object_or_404(MatchProfile, id=user_id)
    return render(request, 'main/portal.html', {'profile': profile})

def logout_view(request):
    request.session.flush()
    return redirect('home')