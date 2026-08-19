from django.contrib import admin
from .models import MatchProfile


@admin.register(MatchProfile)
class MatchProfileAdmin(admin.ModelAdmin):
  list_display = (
      'full_name',
      'email',
      'age',
      'country',
      'status',
      'is_verified',
      'created_at',
  )
  search_fields = ('full_name', 'email', 'occupation', 'country')
  list_filter = ('gender', 'seeking', 'status', 'is_verified')