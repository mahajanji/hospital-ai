from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse
from .models import Contact


# ✅ Normal Django view (template only)

def home(request):
    return render(request, "index.html")



def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            return JsonResponse({'success': False, 'message': 'Please fill all required fields.'})

        try:
            Contact.objects.create(name=name, email=email, phone=phone, message=message)
            return JsonResponse({'success': True, 'message': 'Thank you for contacting us!'})
        except Exception:
            return JsonResponse({'success': False, 'message': 'Error saving your message. Please try again.'})
    return render(request, "contact.html")

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


############################## Chat Bot #####################################
# chatbot/views.py
# chatbot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import get_chatbot_response  # ✅ make sure name matches

@csrf_exempt
def chatbot_reply(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "invalid json"}, status=400)

    message = data.get("message", "").strip()
    if not message:
        return JsonResponse({"reply": "Please type a message."})

    reply = get_chatbot_response(message)  # ✅ function name fixed
    return JsonResponse({"reply": reply})

# In your HTML form, use JavaScript to submit the form via AJAX
