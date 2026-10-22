from django.shortcuts import render

from .dashboard import load_vehicle_data, summarize_vehicles


def dashboard_view(request):
    context = summarize_vehicles(load_vehicle_data())
    return render(request, "vehicles/index.html", context)
