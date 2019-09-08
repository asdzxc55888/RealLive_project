from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
class passwordResetView(View):
    template_name = 'password_reset_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
