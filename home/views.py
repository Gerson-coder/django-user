from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CreateUser, Members_eliminated, Create_subs
from .forms import UserForm, ManageUserForm
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup_user(request):
    if request.method == 'GET':
        print('obteniendo datos')
        return render(request, 'signup.html', {'form': UserForm()})
    else:
        form = UserForm(request.POST)
        print('Datos POST recibidos:', request.POST) 
        if form.is_valid():
            try:
                
                print('Datos limpios del formulario:', form.cleaned_data)
                
                user = form.save(commit=False)  
                user.set_password(form.cleaned_data['password'])  
                user.save()

                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is None:
                    print('Error en la autenticación')  
                    return render(request, 'signup.html', {'form': form, 'error': 'Ha ocurrido un error, inténtelo de nuevo'})
                else:
                    login(request, user)
                    return redirect('home')
            except Exception as e:
                print(f'Error al guardar el formulario: {e}')
                return render(request, 'signup.html', {'form': form, 'error': 'Error en uno de los campos'})
        else:
            
            print('Errores del formulario:', form.errors)
            return render(request, 'signup.html', {'form': form, 'error': 'Error al registrarse'})

def login_user(request):
    if request.method == 'GET':
        print(request.GET)
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm, 'error': 'El usuario o la contraseña es incorrecta'})
        else:
            login(request, user)
            return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def members_fam(request):
    members = CreateUser.objects.filter(is_active = True)
    return render(request, 'members_fam.html', {'members_fam': members})

def members_eliminated(request):
    members = Members_eliminated.objects.all()
    return render(request, 'members_eliminated.html', {'members_eliminated': members})

def delete_member(request):
    if request.method == 'POST':
        print(request.POST)
        form = ManageUserForm(request.POST)
        if form.is_valid():
            
            if form.delete_user():  # Este método se encargará de eliminar al usuario
                return redirect('members_eliminated')  # Redirige a la página que muestra los eliminados
            else:
                messages.error(request, 'Hubo un error al intentar eliminar el usuario.')
        else:
            messages.error(request, 'Formulario inválido. Por favor revisa los campos.')
    else:
        
        form = ManageUserForm()
        

        return render(request, 'delete_member.html', {'form': form})

def restart_member(request):
    if request.method == 'GET':
        form = ManageUserForm()
        return render(request, 'restart_members.html', {'form': form})
    else:
        form = ManageUserForm(request.POST)
        if form.is_valid():
            if form.restore_user():
                return redirect('members_fam')
            else:
                return render(request, 'restart_members.html', {'form': form, 'error': 'El nickname no existe o ya fue restaurado'})
        else:
            return render(request, 'restart_members.html', {'form': form, 'error': 'Datos inválidos'})

def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        total_miembros_activos = CreateUser.objects.filter(is_active=True).count()
        total_miembros_eliminados = Members_eliminated.objects.count()

        context = {
            'total_miembros_activos': total_miembros_activos,
            'total_miembros_eliminados': total_miembros_eliminados,
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, "No tienes los permisos necesarios para acceder a esta zona.")
        return redirect('home')

def autocomplete_nickname(request):
    if 'term' in request.GET:
        qs = CreateUser.objects.filter(nickname__icontains=request.GET.get('term'))
        nicknames = list(qs.values_list('nickname', flat=True))
        return JsonResponse(nicknames, safe=False)
    return JsonResponse([], safe=False)

def events(request):
    return render(request, 'events.html')

def ranking(request):
    return render(request, 'ranking.html')
    


