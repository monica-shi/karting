from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, resolve


class AuthRequiredMiddleware(object):
    get_response = None

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if (not request.user.is_authenticated
                and resolve(request.path).view_name != 'login'
                and resolve(request.path).view_name != 'signup'):
            return HttpResponseRedirect(reverse_lazy('login'))  # or http response

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
