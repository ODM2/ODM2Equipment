from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import CreateUserForm


class CreateUserView(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = CreateUserForm
    object = None

    def form_invalid(self, form):
        self.object = form.instance
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)

        if request.user.is_authenticated:
            logout(request)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            form.save()

            user = authenticate(username=username, password=password)
            user.is_superuser = user.is_staff = True

            user.save()

            login(request, user)
            return redirect('home')

        return self.form_invalid(form)
