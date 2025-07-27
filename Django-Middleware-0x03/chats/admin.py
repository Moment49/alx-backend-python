from django.contrib import admin
from .models import Message, Conversation
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


CustomUser = get_user_model()


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', 'password']
    
    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ("email", "first_name", "last_name", 'role')
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'role')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'role', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()


# Register your models here.
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(CustomUser, CustomUserAdmin)
