from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# for email verification
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.views import View
from .utils import TokenGenerator, generate_token

# write import for force_text
from django.utils.encoding import force_str

# login imports
from django.contrib.auth import authenticate, login, logout

def signup(request):
   if request.method == 'POST':
        # Get the post parameters
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']

        # passwords should match
        if pass1 != pass2:
            print("Passwords do not match")
            messages.warning(request, "Passwords do not match")
            return redirect('/auth/signup')

        # check if username already exists
        if User.objects.filter(email=email).exists():
            print("Email already exists")
            messages.warning(request, "Email already exists")
            return redirect('/auth/signup')
        
        # Create the user
        myuser = User.objects.create_user(username=email,email= email,password= pass1)
        myuser.is_active = False
        myuser.save()
        print("user created")

        print("HOST EMAIL: " + settings.EMAIL_HOST_USER)
        print("HOST PASSWORD: "+ settings.EMAIL_HOST_PASSWORD)

        # send email for verification
        email_subject = 'Activate your account'
        message = render_to_string('verificationMail.html', {
            'user': myuser,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email_message.send()
        messages.success(request, "Account created successfully. Please check your email to verify your account")

        return redirect('/auth/login')

   return render(request,'signup.html')

def handlelogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginemail = request.POST['email']
        loginpassword = request.POST['password']

        user = authenticate(username=loginemail, password=loginpassword)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('/')
            else:
                messages.warning(request, "Account is not verified. Please check your email")
                return redirect('/auth/login')
            
        else:
            messages.warning(request, "Invalid credentials. Please try again")
            return redirect('/auth/login')

        

    return render(request,'login.html')
    
def handlelogout(request):

    logout(request)
    messages.success(request, "Logged out successfully")

    return redirect('/auth/login')

class VerifyAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account verified successfully")
            return redirect('/auth/login')
        
        return render(request, 'verificationFailed.html', status=401)

