from django.urls import path
from.import views
from django.contrib import admin


urlpatterns = [
    # Основные страницы
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),  # Добавил слеш в конце
    path('postypauchim/', views.postypauchim, name='postypauchim'),
    path('roditeli/', views.roditeli, name='roditeli'),

    # Аутентификация
    path('registr/', views.registr, name='registr'),  # Регистрация
    path('vxod/', views.vxod, name='vxod'),  # Вход
    # path('logout/', views.logout_view, name='logout'),  # Добавил выход

    # Другие страницы
    path('ychiteluam/', views.ychiteluam, name='ychiteluam'),
    path('contakt/', views.contakt, name='contakt'),

    # Админка
    path('admin/', admin.site.urls),

    # Добавьте это в конце для обработки 404
   # path('<path:not_found>/', views.handler404, name='404'),

    # Панель админа
    path('admin/', admin.site.urls),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/user/create/', views.create_user, name='create_user'),
    path('admin-panel/user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
]

handler404 = 'main.views.handler404'

