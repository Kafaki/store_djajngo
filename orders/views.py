from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView

from orders.models import Order
from products.models import Basket

from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    extra_context = {"title": "Store - Спасибо за заказ!"}


class CancelTemplateView(TemplateView):
    template_name = 'orders/success.html'



class OrderListVieiw(ListView):
    template_name = 'orders/orders.html'
    extra_context = {'title': "Store - Заказы"}
    context_object_name = 'orders'
    ordering = ['-created']

    def get_queryset(self):
        return Order.objects.filter(initiator=self.request.user)


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    extra_context = {'title': "Store - оформление заказа"}

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        baskets = Basket.objects.filter(user=request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return redirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # Проверяем наличие order_id в metadata
    if not session.metadata or 'order_id' not in session.metadata:
        print(f"⚠️ Order ID not found in session metadata. Session ID: {session.id}")
        return

    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
