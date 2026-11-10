from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('complete-profile/', views.complete_profile_view, name='complete_profile'),
    path('questionnaire/', views.questionnaire_step_view, name='questionnaire_step'),
    path('portal/', views.portal_view, name='portal'),
    path('profile/<int:profile_id>/', views.view_profile_detail, name='view_profile'),
    path('profile/<int:profile_id>/like/', views.toggle_like_view, name='toggle_like'),
    path('profile/<int:profile_id>/share-pin/', views.share_pin_view, name='share_pin'),
    path('chat/<int:connection_id>/', views.chat_room_view, name='chat_room'),
    path('upload-photos/', views.upload_photos_view, name='upload_photos'),
    path('card-payment/', views.card_payment_view, name='card_payment'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('terms/', views.terms_view, name='terms'),
    path('logout/', views.logout_view, name='logout'),
    path('api/check-updates/', views.api_check_updates_view, name='api_check_updates'),
]