from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def sign_in(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('hr:main'))
    else:
        return HttpResponseRedirect(reverse('institution:search'))
