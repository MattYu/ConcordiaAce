from django.shortcuts import render
from accounts.forms import RegistrationForm, LoginForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.models import account_activation_token, User
from django.core.mail import EmailMessage


# Create your views here.
def register_user(request):
    context = {}
    
    if (request.method == 'POST'):
        print(request.POST)
        print("^^^^^^^^^^^^")
        print(request.POST.get('employerCompany'))
        form = RegistrationForm(
            request.POST, 
            request.FILES,
            registrationType=request.POST.get('registrationType'),
            employerCompany=request.POST.get('employerCompany')
            )

        print(form.errors)
        if form.is_valid():
            print("IT WORKS!!!!!!!!!!!!!!")
            
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)

            current_site = get_current_site(request)
            mail_subject = 'Activate your Concordia ACE account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            
            return HttpResponseRedirect('/')

    else:
        form = RegistrationForm(registrationType=None, employerCompany=None)
    context['form'] = form

    return render(request, "register.html", context)


def login_user(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')

    if request.user.is_authenticated:
        return render(request, "404.html")

    form = LoginForm()
    context = {'form': form}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_confirmed = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')