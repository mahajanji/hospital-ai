from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

# ✅ Normal Django view (template only)

def home(request):
    return render(request, "index.html")

def login_views(request):
    return render(request, "login.html")

def register_views(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login_form.html")

# ✅ REST API for login
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(data)
