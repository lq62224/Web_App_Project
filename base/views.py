from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Client, Order, Topic
from .forms import ClientForm, OrderForm

from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# clients = [
#     {'id': 1, 'name':'Maria'},
#     {'id': 2, 'name':'Lupe'},
#     {'id': 3, 'name':'Ruby'},

# ]


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Sorry, something went wrong with your request')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    clients= Client.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) 
        )

    #clients = Client.objects.all() 
    #clients= Client.objects.filter(topic__name__icontains=q) 
    client_count = clients.count()

    orders = Order.objects.all()
    topics = Topic.objects.all()
    context = {'clients': clients, 'order' : orders, 'topics':topics, 'client_count':client_count}
    return render(request, 'base/home.html', context)

def client(request, pk): # instead of room it is clients
    client = Client.objects.get(id=pk)

    context = {'client' : client}
    return render(request, 'base/client.html', context)

def order(request, pk): # instead of room it is clients
    order = Order.objects.get(id=pk)
    context = {'order' : order}
    return render(request, 'base/order.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    clients = user.client_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'clients':clients,  'topics':topics}
    return render(request, 'base/profile.html', context)    

@login_required(login_url='login')
def createClient(request):
    form = ClientForm()
    # topics = Topic.objects.all()
    if request.method =='POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.host = request.user
            client.save()
            return redirect('home')
    #     topic_name = request.POST.get('topic')
    #     topic, created = Topic.objects.get_or_create(name=topic_name)

    #     Room.objects.create(
    #         host=request.user,
    #         topic=topic,
    #         name=request.POST.get('name'),
    #         description=request.POST.get('description'),
    #     )
    #     return redirect('home')
    context= {'form': form}
    # context= {'form': form, 'topics':topics}
    return render(request, 'base/client_form.html', context)

@login_required(login_url='login')
def updateClient(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
#     topics = Topic.objects.all()
    if request.user != client.host:
        return HttpResponse('You are not allowed here!!')

    if request.method =='POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('home')

#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name=topic_name)
#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')
    context = {'form': form}
    # context = {'form': form, 'topics':topics, 'room': room}
    return render(request, 'base/client_form.html', context)

@login_required(login_url='login')
def deleteClient(request, pk):
    client = Client.objects.get(id=pk)

    if request.user != client.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        client.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':client})

# @login_required(login_url='login')
# def deleteMessage(request, pk):
#     message = Message.objects.get(id=pk)

#     if request.user != message.user:
#         return HttpResponse('You are not allowed here!!')

#     if request.method == 'POST':
#         message.delete()
#         return redirect('home')
#     return render(request, 'base/delete.html', {'obj':message})

# @login_required(login_url='login')
# def updateUser(request):
#     user = request.user
#     form = UserForm(instance=user)

#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user-profile', pk=user.id)

#     return render(request, 'base/update-user.html', {'form': form})




@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'form': form}
    # context= {'form': form, 'topics':topics}
    return render(request, 'base/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method =='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form': form}
    # context = {'form': form, 'topics':topics, 'room': room}
    return render(request, 'base/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    #     if request.user != room.host:
    #         return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        order.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':order})