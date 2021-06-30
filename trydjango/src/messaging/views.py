from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request,'index1.html',{})

def room(request, room_name):
 #here room_name is the seller's name

    return render(request, 'room.html',{
        'room_name': room_name
    })
