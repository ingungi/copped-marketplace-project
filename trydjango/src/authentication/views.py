from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from django.views.generic.base import TemplateView
import stripe
from selling.models import Item_posting
from purchasing.models import Cart
from . import forms
from .forms import ItemSalesForm
from datetime import datetime
from django.contrib import messages



stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

def home_view(request):
    context = {}
    context['user']= request.user
    return render(request,'index.html', context)
class HomePageView(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['object'] = Cart.objects.get(user=self.request.user, active=True)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    context = {}
    cart = Cart.objects.filter(user=request.user,active=True)[0]
    Cart.objects.filter(user=request.user, active=True).update(order_date=datetime.now())
    Cart.objects.filter(user=request.user).update(purchased=True)
    Cart.objects.filter(user=request.user).update(active=False)


    if request.method == 'POST':

        total = int(cart.get_total_shipping())*100
        charge = stripe.Charge.create(amount=total,
                                      currency='cad',
                                      description = 'A Copped Charge',
                                      source= request.POST['stripeToken'])


        context['object']= cart
    return render(request, 'charge.html', context)

def cart_view(request):
    context={}
    return render(request, 'cart.html', context)

def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email= form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'])
                return HttpResponseRedirect(reverse('Home'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')
        context['form']= form
    return render(request,'account/signup.html',context)

def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
              username=form.cleaned_data['username'],
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('Home'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
        request.session['user'] = request.user
        request.session['username']= request.user.username

    return render(request, 'account/login.html', context)




def do_logout(request):
    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})

    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def dashboard_view(request):

    user=User.objects.get(username=request.user.username)

    context = {}
    if request.method == 'POST':
        form= forms.changeForm(request.POST)
        if form.is_valid():
            try:
                user.first_name= form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                return HttpResponseRedirect(reverse('Home'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')
        context['form'] = form
    return render(request, 'dashboard/userDash.html', context)

@login_required
def posting(request):

    context = {'items': Item_posting.objects.all()}
    if request.method == 'POST':
        #itemSales form not working so manually used post information
        form = ItemSalesForm(request.POST, request.FILES)
        #put to lower so all characters the same for designer
        new_item = Item_posting(title=request.POST.get('title',False).lower(),
                                descrip=request.POST.get('descrip', False),
                                price=request.POST.get('price', False),
                                type=request.POST.get('type', False),
                                size=request.POST.get('size', False),
                                image=request.FILES['image'],
                                image2=request.FILES['image2'],
                                image3=request.FILES['image3'],
                                image4=request.FILES['image4'],
                                designer=request.POST.get('designer', False).lower(),
                                quantity=request.POST.get('quantity', False),
                                color=request.POST.get('color', False),

                                )
        new_item.owner = request.user
        new_item.save()

        context['form'] = form
    return render(request, 'addlisting.html', context)

def change_password(request):
    user = User.objects.get(username=request.user.username)
    context = {}
    if request.method == 'POST':
        form = forms.changePassword(request.POST)
        if form.is_valid():
            try:
                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password'])
                user.save()
                return HttpResponseRedirect(reverse('Home'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')
        context['form'] = form
    return render(request, 'dashboard/dashLogin.html', context)

def past_orders(request):
    context={}
    try:
        carts = Cart.objects.filter(user=request.user, purchased=True)
        context={
            'objects': carts
        }
        return render(request, 'dashboard/myOrders.html', context)
    except Exception as e:
        messages.info(request, 'You do not have past orders')

        return redirect("cart_view")








