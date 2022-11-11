from django.shortcuts import redirect
from market.models import Checkout
from django.contrib import messages


def checkout_middleware(get_response):
    def middleware(request):
        if not Checkout.objects.filter(user=request.user, complete=False).exists():
            messages.error(request, "Can't access the requested page because you have no order!")
            return redirect("market")
        return get_response(request)
    return middleware


