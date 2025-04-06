import logging

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, UserCreateForm, UserEditForm
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.exceptions import ValidationError
# --- Основные страницы ---
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def postypauchim(request):
    return render(request, 'main/postypauchim.html')

def roditeli(request):
    return render(request, 'main/roditeli.html')

def contakt(request):
    return render(request, 'main/contakt.html')

def ychiteluam(request):
    return render(request, 'main/ychiteluam.html')

def handler404(request, exception):
    return HttpResponseNotFound(render(request, 'main/404.html'))

# --- Регистрация ---
def registr(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user.username)
            return redirect('vxod')  # перенаправление на страницу входа
    else:
        form = RegisterForm()

    return render(request, 'main/registr.html', {'form': form})

# --- Вход ---
logger = logging.getLogger(__name__)


def validate_credentials(username, password):
    """Валидация логина и пароля"""
    if len(username) < 4:
        raise ValidationError("Логин слишком короткий (мин. 4 символа)")
    if len(password) < 8:
        raise ValidationError("Пароль слишком короткий (мин. 8 символов)")
    if not any(c.isupper() for c in password):
        raise ValidationError("Пароль должен содержать заглавные буквы")


@ensure_csrf_cookie
def vxod(request):
    if request.method == 'POST':
        try:
            username = request.POST['username'].strip()
            password = request.POST['password']

            logger.info(f"Попытка входа пользователя: {username}")  # Логируем

            # Валидация
            # validate_credentials(username, password)

            user = authenticate(request, username=username, password=password)
            if user is None:
                logger.warning(f"Неудачная аутентификация для {username}")  # Лог ошибки
                raise ValidationError("Неверный логин или пароль")

            login(request, user)
            logger.info(f"Успешный вход. Перенаправляю {username} в админ-панель")  # Подтверждение

            if user.is_staff or user.is_superuser:
                logger.info(f"Админ {username} перенаправлен в админку")
                return JsonResponse({'success': True, 'redirect_url': '/admin/'})
            else:
                logger.info(f"Пользователь {username} перенаправлен на главную")
                return JsonResponse({'success': True, 'redirect_url': '/'})

        except ValidationError as e:
            logger.error(f"Ошибка валидации: {str(e)}")  # Логируем ошибки
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.critical(f"Серверная ошибка: {str(e)}")  # Критические ошибки
            return JsonResponse({'error': 'Ошибка сервера'}, status=500)

    return render(request, 'main/vxod.html')
# --- Админка ---
def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_panel(request):
    users = User.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'users': users})

@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно создан!')
            return redirect('admin_panel')
    else:
        form = UserCreateForm()

    return render(request, 'admin_panel/create_user.html', {'form': form})

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные пользователя обновлены!')
            return redirect('admin_panel')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'admin_panel/edit_user.html', {
        'form': form,
        'user': user
    })
