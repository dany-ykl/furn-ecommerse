from django.views import View
from cart.models import Order, Customer


class OrderMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user,
                    email=request.user.email,
                    name=request.user.first_name)

                order = Order.objects.create(owner=customer)

            order = Order.objects.filter(owner=customer, in_order=False).first()
    
        else:
            customer = Customer.objects.filter(session_id=request.session.session_key).first()
            if not customer:
                customer = Customer.objects.create(
                session_id=request.session.session_key,
                anonymos_user=True
                )
            order = Order.objects.filter(owner=customer).first()
            if not order:
                order = Order.objects.create(owner=customer, for_anonymos_user=True)
        self.order = order
        self.customer = customer

        return super().dispatch(request, *args, **kwargs)


def get_cart_and_customer(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user,
                    email=request.user.email,
                    name=request.user.first_name
                    )

                order = Order.objects.create(owner=customer)

            order = Order.objects.filter(owner=customer, in_order=False).first()
        else:
            customer = Customer.objects.filter(session_id=request.session.session_key).first()
            if not customer:
                customer = Customer.objects.create(
                session_id=request.session.session_key,
                anonymos_user=True
                )
            order = Order.objects.filter(owner=customer).first()
            if not order:
                order = Order.objects.create(owner=customer, for_anonymos_user=True)
        kwargs['customer'] = customer
        kwargs['order'] = order

        return func(request, *args, **kwargs)
    
    return wrapper
