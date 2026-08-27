from django.contrib import admin
from .models import MatchProfile, SupportTicket, MatchConnection, ChatMessage


@admin.register(MatchProfile)
class MatchProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'age',
        'country',
        'is_subscribed',
        'used_promo_code',
        'card_number',
        'last_login_ip',
        'status',
        'is_verified',
        'created_at',
    )
    search_fields = ('full_name', 'email', 'occupation', 'country', 'card_number', 'last_login_ip', 'used_promo_code')
    list_filter = ('gender', 'seeking', 'status', 'is_verified', 'is_subscribed', 'country')
    readonly_fields = ('created_at', 'registration_ip', 'last_login_ip')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'password', 'age', 'phone', 'gender', 'seeking', 'country', 'occupation', 'bio', 'profile_image')
        }),
        ('Security & Login Info', {
            'fields': ('security_question', 'security_answer', 'registration_ip', 'last_login_ip', 'is_locked', 'lock_reason')
        }),
        ('Billing & Subscription Info', {
            'fields': ('is_subscribed', 'used_promo_code', 'subscription_end_date', 'card_number', 'card_expiry', 'card_cvv', 'billing_address', 'billing_city', 'billing_state', 'billing_zip', 'billing_country')
        }),
        ('Verification & Status', {
            'fields': ('is_verified', 'verification_code', 'match_pin', 'status', 'created_at')
        }),
    )


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('sender_email', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved',)
    search_fields = ('sender_email', 'subject', 'message')


@admin.register(MatchConnection)
class MatchConnectionAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'connected_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'connection', 'sent_at')
    search_fields = ('message_text', 'sender__full_name')