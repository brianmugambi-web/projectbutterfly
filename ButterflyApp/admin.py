from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from .models import CustomUser, Butterfly, ExpertReview
from .models import Butterfly, ButterflyMedia, ExpertReview

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "is_expert", "is_researcher"]

    def clean(self):
        """Ensure only one role is set."""
        cleaned_data = super().clean()
        is_expert = cleaned_data.get("is_expert", False)
        is_researcher = cleaned_data.get("is_researcher", False)

        # Ensure a user has only one role
        if is_expert and is_researcher:
            raise forms.ValidationError("A user cannot be both an expert and a researcher. Please select only one role.")
        
        return cleaned_data


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm  # Use the custom form in the admin panel

    list_display = ("username", "email", "get_role", "is_staff")
    search_fields = ("username", "email")
    list_filter = ("is_expert", "is_researcher", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email",)}),
        ("User Role", {"fields": ("is_expert", "is_researcher")}),  # Use toggle instead of a custom field
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_expert", "is_researcher"),
        }),
    )

    class Media:
        """Include custom JavaScript for toggling roles."""
        js = (static("admin/toggle_roles.js"),)

    def get_role(self, obj):
        """Show the role in the list display."""
        return "Expert" if obj.is_expert else "Researcher"
    
    get_role.short_description = "Role"

@admin.register(Butterfly)
class ButterflyAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "status", "researcher", "date_taken")
    list_filter = ("status", "species")
    search_fields = ("name", "species", "location_name")
    ordering = ("-date_taken",)

@admin.register(ButterflyMedia)
class ButterflyMediaAdmin(admin.ModelAdmin):
    list_display = ("butterfly", "media_type", "status", "uploaded_at")
    list_filter = ("media_type", "status")
    search_fields = ("butterfly__name",)
    ordering = ("-uploaded_at",)

@admin.register(ExpertReview)
class ExpertReviewAdmin(admin.ModelAdmin):
    list_display = ("butterfly", "expert", "species_identification", "decision", "review_date")
    list_filter = ("decision",)
    search_fields = ("butterfly__name", "expert__username")
    ordering = ("-review_date",)