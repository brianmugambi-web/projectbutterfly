from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # Import dynamically

CustomUser = get_user_model()  # Get the active user model

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Use the new CustomUser model
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_researcher = True  # Set researcher role
        user.is_expert = False  # Ensure they are NOT an expert
        if commit:
            user.save()
        return user
