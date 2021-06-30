from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from selling.models import Item_posting
from purchasing.models import Cart, CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from authentication.forms import ItemSalesForm
from .forms import CheckoutForm


def menswear(request):

	mens = Item_posting.objects.filter(type="2")
	paginator = Paginator(mens, 4)
	page = request.GET.get('page')
	try:
		mens_products = paginator.page(page)
	except PageNotAnInteger:
		mens_products = paginator.page(1)
	except EmptyPage:
		mens_products = paginator.page(paginator.num_pages)

	return render(request, 'clothing/menswear.html', {'mens_products': mens_products})

def product(request, Item):
	Choice = Item_posting.objects.get(id=Item)
	return render(request, 'clothing/product.html', {'Choice': Choice})

def designer(request, Brand):
	clothes = Item_posting.objects.filter(designer=Brand)
	paginator = Paginator(clothes, 4)
	page = request.GET.get('page')
	try:
		cproducts = paginator.page(page)
	except PageNotAnInteger:
		cproducts = paginator.page(1)
	except EmptyPage:
		cproducts = paginator.page(paginator.num_pages)
	return render(request, 'designer.html', {'cproducts': cproducts})

def womenswear(request):
	womens = Item_posting.objects.filter(type="1")
	paginator = Paginator(womens, 4)
	page = request.GET.get('page')
	try:
		womens_products = paginator.page(page)
	except PageNotAnInteger:
		womens_products = paginator.page(1)
	except EmptyPage:
		womens_products = paginator.page(paginator.num_pages)
	return render(request, 'clothing/womenswear.html', {'womens_products': womens_products})

def accessories(request):
	acc = Item_posting.objects.filter(type="3")
	paginator = Paginator(acc, 4)
	page = request.GET.get('page')
	try:
		acc_products = paginator.page(page)
	except PageNotAnInteger:
		acc_products = paginator.page(1)
	except EmptyPage:
		acc_products = paginator.page(paginator.num_pages)
	return render(request, 'clothing/accessories.html', {'acc_products': acc_products})

def footwear(request):
	ft = Item_posting.objects.filter(type="4")
	paginator = Paginator(ft, 4)
	page = request.GET.get('page')
	try:
		ft_products = paginator.page(page)
	except PageNotAnInteger:
		ft_products = paginator.page(1)
	except EmptyPage:
		ft_products = paginator.page(paginator.num_pages)

	return render(request, 'clothing/footwear.html', {'ft_products': ft_products})
	
def designer_home(request):
	alphabet = ['A','B','C','D','E','F','G','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	brands_list = []
	for letter in alphabet: 
		letter_ = {'Items': Item_posting.objects.filter(designer__startswith=letter), 'letter': letter}
		brands_list.append(letter_)

	return render(request, 'womenOrMen.html', {'designers' : brands_list})

class OrderSummaryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			cart = Cart.objects.get(user=self.request.user, active=True)
			context = {
				'object': cart
			}
			return render(self.request,'cart.html', context)
		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("cart_view")

@login_required
def remove_from_cart(request, id):
	item = Item_posting.objects.get(id=id)
	pid = item.id
	cart_qs = Cart.objects.filter(user=request.user,purchased=False,active=True)
	if cart_qs.exists():
		cart = cart_qs[0]
		if cart.items.filter(item__id=item.id).exists():
			citem = CartItem.objects.filter(item=item,user=request.user,ordered=False)[0]
			qtynew = item.quantity + citem.quantity
			cquant=citem.quantity-1
			CartItem.objects.filter(item=item, user=request.user, ordered=False).update(quantity=cquant)
			Item_posting.objects.filter(id=id).update(quantity=qtynew)
			cart.items.remove(citem)
			citem.delete()
			messages.info(request, "This item was removed from your cart.")
			return redirect("order-summary")
		else:
			messages.info(request, "This item was not in your cart")
			return redirect("order-summary")
	else:
		messages.info(request, "You have no active item")
		return redirect("order-summary")

@login_required
def add_to_cart(request, id):
	item = Item_posting.objects.get(id=id)
	pid = item.id
	qtynew = item.quantity - 1
	citem, created = CartItem.objects.get_or_create(item=item,user=request.user,ordered=False)
	if item.quantity > 0:
		cart_qs = Cart.objects.filter(user=request.user,active=True)
		if cart_qs.exists():
			cart = cart_qs[0]
			if cart.items.filter(item=item).exists():
				Item_posting.objects.filter(id=id).update(quantity=qtynew)
				citem.quantity += 1
				citem.save()
				messages.info(request, "This item quantity was updated.")
				return redirect("product", Item=pid)
			else:
				cart.items.add(citem)
				Item_posting.objects.filter(id=id).update(quantity=qtynew)
				messages.info(request, "This product was added to your cart.")
				return redirect("product", Item=pid)
		else:
			cart = Cart.objects.create(user=request.user)
			cart.items.add(citem)
			Item_posting.objects.filter(id=id).update(quantity=qtynew)
			messages.info(request, "This product was added to your cart.")
			return redirect("product", Item=pid)
	else:
		messages.info(request, "This product is now out of stock.")
		return redirect("product",Item=pid)


@login_required
def checkout(request):
	context = {}
	if request.method == "POST":
		form = CheckoutForm(request.POST)
		if form.is_valid():
			Cart.objects.filter(user=request.user).update(address=form.cleaned_data['address'])
			Cart.objects.filter(user=request.user).update(name=form.cleaned_data['name'])
			Cart.objects.filter(user=request.user).update(city=form.cleaned_data['city'])
			Cart.objects.filter(user=request.user).update(province=form.cleaned_data['province'])
			Cart.objects.filter(user=request.user).update(postal_code=form.cleaned_data['postal_code'])

			return redirect("payment")
		context = {'form': form}
	return render(request, 'checkout.html', context)

def change_listing(request, item_id):
	context = {'items': Item_posting.objects.all(),
			   'id': item_id
			   }
	context['item'] = Item_posting.objects.filter(id=item_id)[0]
	if request.method == 'POST':
		try:
			Item_posting.objects.filter(id=item_id)[0].delete()

			form = ItemSalesForm(request.POST, request.FILES)
			new_item = Item_posting(title=request.POST.get('title', False).lower(),
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
			context['item'] = Item_posting.objects.filter(id=new_item.id)[0]
			context['form'] = form

		except Item_posting.DoesNotExist:
			messages.info(request, "This item does not exist.")
		#itemSales form not working so manually used post information

	return render(request, 'change_listing.html', context)

def delete_listing(request, item_id):
	context={}
	try:
		Item_posting.objects.filter(id=item_id)[0].delete()
	except Exception as e:

		messages.info(request, e.message)
	return redirect("dashboard")





