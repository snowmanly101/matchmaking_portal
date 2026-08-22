from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('questionnaire/<int:step>/', views.questionnaire_step_view, name='questionnaire_step'),
    path('portal/', views.portal_view, name='portal'),
    path('chat/<int:connection_id>/', views.chat_room_view, name='chat_room'),
    path('terms/', views.terms_view, name='terms'),
    path('logout/', views.logout_view, name='logout'),
]