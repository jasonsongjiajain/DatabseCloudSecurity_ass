from re import U
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from application.models import user_detail
from application.models import paymentmethod_detail
from application.models import Plan
from django.contrib.auth.models import User, Group
from .forms import RegistrationForm
from .forms import LoginForm
from .forms import PaymentMethodForm
from .forms import PhonePlanForm
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('full_name')
            phoneno = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')

            # Split the full_name into first_name and last_name
            split_name = full_name.split(' ', 1)
            first_name = split_name[0]
            last_name = split_name[1] if len(split_name) > 1 else ''

            # Create a new user instance
            new_user = User.objects.create_user(username=username, email=email, password=password)
            
            # Set first_name and last_name for the user instance
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            new_user_detail = user_detail.objects.create(user=new_user,phoneno=phoneno)
            new_user_detail.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('homepage')

            else:
                # Invalid login credentials, display an error message
                form.add_error(None, 'Invalid username or password')

    else:
        form = LoginForm()  # If it's a GET request, create an instance of the LoginForm

    return render(request, 'login.html', {'form': form})

@login_required
def homepage(request):
    return render(request, 'homepage.html')

@login_required
def phoneplan(request):
    return render(request, 'phoneplan.html')

@login_required
def payingpage(request):
    user = request.user
    if request.method == 'POST':
        form = PhonePlanForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data.get('plan')
            amount = form.cleaned_data.get('amount')
            new_plan = Plan.objects.create(user=user, plan=plan, amount=amount)
            new_plan.save()
            return redirect('paymentmethod')
    else:
        form = PhonePlanForm()
    return render(request, 'payingpage.html', {'form': form})

@login_required
def paymentmethod(request):
    user=request.user
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            cardtype = form.cleaned_data.get('cardtype')
            CVV = form.cleaned_data.get('CVV')
            cardnumber = form.cleaned_data.get('cardnumber')
            expiryyear = form.cleaned_data.get('expiryyear')
            expirymonth = form.cleaned_data.get('expirymonth')
            cardholdername = form.cleaned_data.get('cardholdername')
            new_Payment_detail = paymentmethod_detail.objects.create(user=user,cardtype=cardtype, cardnumber=cardnumber, expirymonth=expirymonth, expiryyear=expiryyear, CVV=CVV, cardholdername=cardholdername)
            new_Payment_detail.save()
            return redirect('confirmationpage')
    else:
        form = PaymentMethodForm()
    return render(request, 'paymentmethod.html', {'form': form})

@login_required
def confirmationpage(request):
    return render(request, 'confirmationpage.html')

@login_required
def account_info(request):
    user = request.user
    user_with_masked_email = User.objects.using('read_masked_data').get(id=user.id)
    masked_email = user_with_masked_email.email

    try:
        user_detail_obj = user_detail.objects.get(user=user)
    except user_detail.DoesNotExist:
        user_detail_obj = None

    try:
        paymentmethod_detail_obj = paymentmethod_detail.objects.using('read_masked_data').get(user=user)
    except paymentmethod_detail.DoesNotExist:
        paymentmethod_detail_obj = None

    try:
        plan_obj = Plan.objects.get(user=user)
    except Plan.DoesNotExist:
        plan_obj = None

    return render(request, 'account_info.html', {
        'user_detail': user_detail_obj,
        'paymentmethod_detail': paymentmethod_detail_obj,
        'Plan': plan_obj,
        'masked_email': masked_email,
        'user': user
    })




@login_required
def remove_plan(request):
    if request.method == 'POST':
        user = request.user
        plan = get_object_or_404(Plan, user=user)
        plan.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def remove_payment_method(request):
    if request.method == 'POST':
        user = request.user
        payment_method = get_object_or_404(paymentmethod_detail, user=user)
        payment_method.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
