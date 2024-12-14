from django.contrib import admin
from .models import CustomerUser, VerificationCode, TokenBlacklist

# Register the CustomerUser model
@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')

# Register the VerificationCode model
@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'is_used')
    search_fields = ('phone_number',)
    list_filter = ('is_used',)

# Register the TokenBlacklist model
@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    list_display = ('token', 'blacklisted_at')
