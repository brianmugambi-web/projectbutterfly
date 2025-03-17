from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Butterfly, ButterflyMedia, ExpertReview, CustomUser
from .forms import SignupForm


@csrf_exempt
def my_view(request):
    return JsonResponse({"message": "CSRF disabled for this view"})


# ----------------------------------------------
# 🔹 Utility function to check user role
# ----------------------------------------------
def is_expert(user):
    """Check if the user is an expert."""
    return hasattr(user, "is_expert") and user.is_expert


# ----------------------------------------------
# 🔹 RESEARCHERS & ENTHUSIASTS VIEWS
# ----------------------------------------------


@login_required
def capture_butterfly(request):
    """Allows researchers to capture butterfly details with location tracking."""

    if is_expert(request.user):  # Prevent experts from capturing
        return redirect("expert_dashboard")

    if request.method == "POST":
        # Fetch text fields
        name = request.POST.get("name", "").strip()
        species = request.POST.get("species", "").strip()
        characteristics = request.POST.get("characteristics", "").strip()

        # Location Data
        latitude = request.POST.get("latitude", "").strip()
        longitude = request.POST.get("longitude", "").strip()
        location_name = request.POST.get("location_name", "").strip()

        # Media files
        media_files = request.FILES.getlist("media")

        # Logging received data
        print(f"Name: {name}, Species: {species}, Characteristics: {characteristics}")
        print(f"Latitude: {latitude}, Longitude: {longitude}, Location: {location_name}")
        print(f"Uploaded {len(media_files)} media files.")

        # Validation
        if not name:
            messages.error(request, "Name is required.")
            return redirect("capture_butterfly")

        if not media_files:
            messages.error(request, "You must upload at least one image or video.")
            return redirect("capture_butterfly")

        try:
            # Create the Butterfly object
            butterfly = Butterfly.objects.create(
                name=name,
                species=species if species else None,
                characteristics=characteristics,
                date_taken=timezone.now(),
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                location_name=location_name if location_name else None,
                status="pending",
                researcher=request.user
            )

            # Process each uploaded file
            for file in media_files:
                content_type = file.content_type
                media_type = "image" if content_type.startswith("image/") else "video" if content_type.startswith("video/") else None

                if media_type:
                    ButterflyMedia.objects.create(
                        butterfly=butterfly,
                        media_file=file,
                        media_type=media_type
                    )
                else:
                    messages.warning(request, f"Unsupported file type: {content_type}")

            messages.success(request, "Butterfly details and media successfully saved!")
            return redirect("capture_butterfly")

        except Exception as e:
            messages.error(request, f"Error saving details: {str(e)}")
            print("Error in saving data:", str(e))
            return redirect("capture_butterfly")

    return render(request, "butterfly/capture.html")


@login_required
def butterfly_list(request):
    """Displays butterflies based on user role."""
    butterflies = Butterfly.objects.filter(status="pending") if is_expert(request.user) else Butterfly.objects.all()
    return render(request, "butterfly/butterfly_list.html", {"butterflies": butterflies})


# ----------------------------------------------
# 🔹 EXPERTS & VALIDATORS VIEWS (UPDATED)
# ----------------------------------------------

@login_required
@user_passes_test(is_expert)
def expert_dashboard(request):
    """Displays butterflies that need expert review."""
    pending_butterflies = Butterfly.objects.filter(status="pending")
    pending_count = pending_butterflies.count()
    return render(
        request,
        "expert/dashboard.html",
        {"butterflies": pending_butterflies, "pending_count": pending_count},
    )


@login_required
@user_passes_test(is_expert)
def review_butterfly(request, record_id):
    """Allows experts to review a butterfly record with multiple images."""
    butterfly = get_object_or_404(Butterfly, id=record_id)
    media_files = butterfly.media.all()  # Fetch all media files for this butterfly

    if request.method == "POST":
        feedback = request.POST["feedback"]
        species_identification = request.POST.get("species_identification", "Unknown")

        # Handle per-image validation
        accepted_media_ids = request.POST.getlist("accept_media")  # List of accepted media IDs

        # Update media statuses instead of deleting
        for media in media_files:
            if str(media.id) in accepted_media_ids:
                media.status = "accepted"
            else:
                media.status = "rejected"
            media.save()

        # Create expert review
        ExpertReview.objects.create(
            butterfly=butterfly,
            expert=request.user,
            feedback=feedback,
            species_identification=species_identification,
            decision="validated" if accepted_media_ids else "rejected",
            review_date=timezone.now(),
        )

        # Final validation decision based on remaining media
        if media_files.filter(status="accepted").exists():
            butterfly.status = "validated"
        else:
            butterfly.status = "rejected"

        butterfly.save()
        return redirect("expert_dashboard")

    return render(request, "expert/review.html", {"butterfly": butterfly, "media_files": media_files})


# ----------------------------------------------
# 🔹 AUTHENTICATION VIEWS
# ----------------------------------------------

def signup(request):
    """Registers a new researcher only."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_expert = False
            user.is_researcher = True
            user.is_staff = False
            user.is_superuser = False
            user.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


def custom_login(request):
    """Handles login and redirects users based on their role."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("expert_dashboard" if is_expert(user) else "capture_butterfly")

        return render(request, "registration/login.html", {"form": form, "error": "Invalid username or password."})

    return render(request, "registration/login.html", {"form": AuthenticationForm()})
