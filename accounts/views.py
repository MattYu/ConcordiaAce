from django.shortcuts import render
from accounts.forms import RegistrationForm

# Create your views here.
def register_user(request):
    context = {}
    
    if (request.method == 'POST'):
        print(request.POST)
        print(request.POST.get('registrationType'))
        form = RegistrationForm(
            request.POST, 
            request.FILES,
            registrationType=request.POST.get('registrationType'),
            )
        #request.session['form'] = form.as_p()
 
    else:
        form = RegistrationForm(registrationType=None, companyType=None)
    context['form'] = form

    return render(request, "register.html", context)


def login(request):
    return render(request, "login.html")