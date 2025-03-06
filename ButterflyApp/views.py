
# Create your views here.
from django.shortcuts import render, redirect
from .models import Butterfly
from datetime import datetime

def capture_butterfly(request):
    if request.method == "POST":
        name = request.POST["name"]
        species = request.POST.get("species", "")
        characteristics = request.POST["characteristics"]
        image = request.FILES["image"]

        butterfly = Butterfly(
            name=name,
            species=species,
            characteristics=characteristics,
            image=image,
            date_taken=datetime.now()  # Store the date manually
        )
        butterfly.save()
        return redirect("/")  # Redirect to list of saved entries

    return render(request, "butterfly/capture.html")


def butterfly_list(request):
    pass