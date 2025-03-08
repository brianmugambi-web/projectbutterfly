from django.shortcuts import render, redirect
from django.contrib import messages  # Import Django messages
from .models import Butterfly
import datetime

from django.core.files.storage import default_storage

def capture_butterfly(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            species = request.POST.get("species", "").strip()
            characteristics = request.POST.get("characteristics", "").strip()
            uploaded_file = request.FILES.get("media", None) 

            latitude = request.POST.get("latitude", "").strip()
            longitude = request.POST.get("longitude", "").strip()
            location_name = request.POST.get("location_name", "").strip()

            print("Uploaded Files:", request.FILES)
            print("Location Data:", latitude, longitude, location_name)

            if not name:
                messages.error(request, "Name is required.")
                return redirect("home")

            if uploaded_file is None:
                messages.error(request, "You must upload an image or video.")
                return redirect("home")

            # Determine file type (image or video)
            content_type = uploaded_file.content_type
            is_image = content_type.startswith("image")
            is_video = content_type.startswith("video")

            butterfly = Butterfly(
                name=name,
                species=species if species else None,
                characteristics=characteristics,
                date_taken=datetime.datetime.now(),
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                location_name=location_name if location_name else None
            )

            if is_image:
                butterfly.image = uploaded_file
            elif is_video:
                butterfly.video = uploaded_file
            
            butterfly.save()

            messages.success(request, "Butterfly details successfully saved!")
            return redirect("home")

        except Exception as e:
            messages.error(request, f"Error saving details: {str(e)}")
            return redirect("home")

    return render(request, "butterfly/capture.html")

def butterfly_list(request):
    pass 