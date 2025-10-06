from django.urls import reverse_lazy
from django.views.generic import CreateView

from orders.forms import OrderForm


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    extra_context = {'title': "Store - оформление заказа"}

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return  super().form_valid(form)


