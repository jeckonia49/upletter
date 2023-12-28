from django.shortcuts import render
from django.contrib.flatpages.models import FlatPage



def handler404(request, *args, **kwargs):
    response = render(request, 'flatpages/404.html', {
        "flatpage":FlatPage.objects.get(title="404")
    })
    return response


def handler500(request, *args, **argv):
    response = render('flatpages/404.html', {"flatpage":FlatPage.objects.get(title="404")})
    return response