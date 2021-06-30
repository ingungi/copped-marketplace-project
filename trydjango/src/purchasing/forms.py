from django import forms

class CheckoutForm(forms.Form):
		name = forms.CharField()
		address = forms.CharField()
		city = forms.CharField()
		province = forms.CharField()
		postal_code = forms.CharField()