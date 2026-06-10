from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import DietProfile
from .diet_logic import generate_ai_diet

def home(request):
    return render(request, "home.html")
def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("profile")
    return render(request, "login.html")

@login_required
def diet_form(request):
    if request.method == "POST":
        age = request.POST["age"]
        gender = request.POST["gender"]
        height = float(request.POST["height"])
        weight = float(request.POST["weight"])
        goal = request.POST["goal"]
        DietProfile.objects.update_or_create(
            user=request.user,
            defaults={
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "goal": goal,
            }
        )
        return redirect("dashboard")
    return render(request, "profile_form.html")

@login_required
def dashboard(request):
    profile = DietProfile.objects.filter(user=request.user).first()
    bmi = None
    category = None
    calories = None
    diet_plan = ""
    if profile:
        height_m = profile.height / 100
        bmi = round(profile.weight / (height_m * height_m), 2)
        water_intake = round(profile.weight * 35 / 1000, 1)  # litres
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal Weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        calories = profile.weight * 30
        if profile.goal == "Weight Loss":
            calories -= 500
        elif profile.goal == "Weight Gain":
            calories += 500
        # Gemini AI Diet Plan
        diet_plan = generate_ai_diet(
            profile.age,
            profile.gender,
            profile.height,
            profile.weight,
            profile.goal
        )
    context = {
        "profile": profile,
        "bmi": bmi,
        "category": category,
        "calories": calories,
        "diet_plan": diet_plan,
    }
    return render(request, "dashboard.html", context)

@login_required
def download_pdf(request):
    profile = DietProfile.objects.filter(user=request.user).first()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="diet_plan.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 800, "AI Diet Plan")
    if profile:
        p.setFont("Helvetica", 12)
        p.drawString(50, 770, f"Name: {request.user.username}")
        p.drawString(50, 750, f"Age: {profile.age}")
        p.drawString(50, 730, f"Gender: {profile.gender}")
        p.drawString(50, 710, f"Height: {profile.height} cm")
        p.drawString(50, 690, f"Weight: {profile.weight} kg")
        p.drawString(50, 670, f"Goal: {profile.goal}")
        diet_plan = generate_ai_diet(
            profile.age,
            profile.gender,
            profile.height,
            profile.weight,
            profile.goal
        )
        y = 630
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "AI Diet Plan")
        y -= 25
        p.setFont("Helvetica", 11)
        for line in diet_plan.split("\n"):
            if line.strip():
                p.drawString(50, y, line[:100])
                y -= 18
                if y < 50:
                    p.showPage()
                    y = 800
    p.save()
    return response