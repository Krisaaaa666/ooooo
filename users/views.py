from django.shortcuts import render

# Create your views here.


from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def registr (request):
    form = UserCreationForm()
    return render(request, 'users/registr.html', {'form': form})