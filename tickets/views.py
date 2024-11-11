from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

# Create your views here.

def base(request):
    return render(request,'tickets/base.html')

@login_required
def dashboard(request):
    return render (request,'tickets/dashboard.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('login')
        else:
            messages.error(request, "There was an error with your signup. Please check the details.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/tickets/dashboard')
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

# Logout
def user_logout(request):
 logout(request)
 return HttpResponseRedirect('/')

#models Views


def is_engineer(user):
    return user.groups.filter(name='Engineer').exists()

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    
    if ticket.creator != request.user and ticket.assigned_engineer != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this ticket.")
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if ticket.assigned_engineer == request.user or request.user.is_superuser:
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.user = request.user
                comment.save()
                return redirect('ticket_detail', id=ticket.id)
            else:
                return HttpResponseForbidden("You are not authorized to add comments to this ticket.")
    else:
        comment_form = CommentForm()

    comments = ticket.comments.all()
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def ticket_update_status(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if ticket.assigned_engineer != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to update the status of this ticket.")

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else: 
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_form.html', {'form': form})
