from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Butterfly, ButterflyMedia, ExpertReview, CustomUser
from .forms import SignupForm
from django.utils import timezone


from django.views.decorators.csrf import csrf_exempt

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

        # --- Logging received data ---
        print("==== Received Data from Frontend ====")
        print(f"Name: {name}")
        print(f"Species: {species}")
        print(f"Characteristics: {characteristics}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Location Name: {location_name}")

        print("\nUploaded Media Files:")
        if not media_files:
            print("No media files received.")
        else:
            for idx, file in enumerate(media_files, start=1):
                print(f"{idx}. Filename: {file.name}, Content Type: {file.content_type}, Size: {file.size} bytes")

        print("=====================================\n")
        # --- End logging ---

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
                researcher=request.user  # Optional
            )

            # Process each uploaded file
            for file in media_files:
                content_type = file.content_type

                if content_type.startswith("image/"):
                    media_type = "image"
                elif content_type.startswith("video/"):
                    media_type = "video"
                else:
                    messages.warning(request, f"Unsupported file type: {content_type}")
                    continue

                # Save media file (link it to the butterfly)
                ButterflyMedia.objects.create(
                    butterfly=butterfly,
                    media_file=file,
                    media_type=media_type
                )

            messages.success(request, "Butterfly details and media successfully saved!")
            return redirect("capture_butterfly")

        except Exception as e:
            messages.error(request, f"Error saving details: {str(e)}")
            print("Error in saving data:", str(e))  # Logging the exception
            return redirect("capture_butterfly")

    return render(request, "butterfly/capture.html")


@login_required
def butterfly_list(request):
    """Displays butterflies based on user role."""
    if is_expert(request.user):
        # Experts see only pending butterflies
        butterflies = Butterfly.objects.filter(status="pending")
    else:
        # Regular users see all (or only their own, if needed)
        butterflies = Butterfly.objects.all()  # Change to filter by user if needed

    return render(request, "butterfly/butterfly_list.html", {"butterflies": butterflies})


# ----------------------------------------------
# 🔹 EXPERTS & VALIDATORS VIEWS
# ----------------------------------------------

@login_required
@user_passes_test(is_expert)
def expert_dashboard(request):
    """Displays butterflies that need expert review."""
    pending_butterflies = Butterfly.objects.filter(status="pending")
    pending_count = pending_butterflies.count()  # Get the count of pending submissions
    return render(
        request,
        "expert/dashboard.html",
        {"butterflies": pending_butterflies, "pending_count": pending_count},
    )


@login_required
@user_passes_test(is_expert)
def review_butterfly(request, record_id):
    """Allows experts to review a butterfly record."""
    butterfly = get_object_or_404(Butterfly, id=record_id)

    if request.method == "POST":
        feedback = request.POST["feedback"]
        species_identification = request.POST.get("species_identification", "Unknown")
        decision = request.POST["decision"]  # 'validated' or 'rejected'

        # Create expert review
        review = ExpertReview.objects.create(
            butterfly=butterfly,
            expert=request.user,
            feedback=feedback,
            species_identification=species_identification,
            decision=decision,
            review_date=datetime.now(),
        )

        # Update butterfly record status
        if decision == "validated":
            butterfly.status = "validated"
        else:
            butterfly.status = "rejected"
            # TODO: Notify researcher if rejected

        butterfly.save()
        return redirect("expert_dashboard")

    return render(request, "expert/review.html", {"butterfly": butterfly})


# ----------------------------------------------
# 🔹 AUTHENTICATION VIEWS
# ----------------------------------------------

def signup(request):
    """Registers a new researcher only."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_expert = False  # Ensure they are not experts
            user.is_researcher = True  # Mark as researcher
            user.is_staff = False  # Ensure normal users are not staff/admins
            user.is_superuser = False  # Ensure normal users are not superusers
            user.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")  # Redirect to login page
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

            # Handle "next" parameter if available
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)

            # Role-based redirection
            if is_expert(user):
                return redirect("expert_dashboard")  # Experts → Dashboard
            else:
                return redirect("capture_butterfly")  # Researchers → Capture Page
        else:
            return render(
                request,
                "registration/login.html",
                {"form": form, "error": "Invalid username or password."},
            )

    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})
