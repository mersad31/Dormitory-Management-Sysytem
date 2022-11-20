from django.shortcuts import render


def home(request, *args, **kwargs):
    context = {}
    return render(request=request, template_name='Index.html', content_type='text/html',
                  status=200,
                  context=context,
                  using=None)
