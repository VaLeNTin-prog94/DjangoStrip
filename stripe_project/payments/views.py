import stripe
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views import View

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class BuyView(View):
    """
    Представление для создания сессии оплаты через Stripe Checkout.

    Метод GET создает новую сессию оплаты для товара с указанным ID и возвращает ID сессии.
    """

    def get(self, request, id):
        """
        Обрабатывает GET-запрос для создания сессии Stripe Checkout.

        Аргументы:
            request (HttpRequest): Запрос от клиента.
            id (int): ID товара, который пользователь хочет купить.

        Возвращает:
            JsonResponse: JSON-ответ с идентификатором сессии Stripe или ошибкой.
        """
        item = get_object_or_404(Item, id=id)

        try:
            # Создаем сессию Stripe Checkout
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',  # Валюта в долларах
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': item.price,  # Цена в центах
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'{request.build_absolute_uri("/success/")}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{request.build_absolute_uri("/cancel/")}',
            )

            return JsonResponse({'id': session.id})

        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)


def item_detail(request, id):
    """
    Представление для отображения информации о конкретном товаре.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        id (int): ID товара, который необходимо отобразить.

    Возвращает:
        HttpResponse: Страница с информацией о товаре.
    """
    item = get_object_or_404(Item, id=id)
    item.price = item.price / 100  # Конвертируем цену из центов в доллары

    return render(request, 'item.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


def success(request):
    """
    Представление для страницы успешной оплаты.

    Аргументы:
        request (HttpRequest): Запрос от клиента.

    Возвращает:
        HttpResponse: Страница с сообщением об успешной оплате.
    """
    return render(request, 'success.html')


def cancel(request):
    """
    Представление для страницы отмены оплаты.

    Аргументы:
        request (HttpRequest): Запрос от клиента.

    Возвращает:
        HttpResponse: Страница с сообщением об отмене оплаты.
    """
    return render(request, 'cancel.html')


def home(request):
    """
    Главная страница магазина с отображением списка товаров.

    Реализует пагинацию, отображая по 10 товаров на страницу.

    Аргументы:
        request (HttpRequest): Запрос от клиента.

    Возвращает:
        HttpResponse: Страница с перечнем товаров.
    """
    items = Item.objects.all()
    paginator = Paginator(items, 10)  # Разбиваем список товаров на страницы по 10 товаров
    page_number = request.GET.get('page')  # Получаем номер текущей страницы
    page_obj = paginator.get_page(page_number)

    # Конвертируем цены из центов в доллары
    for item in page_obj:
        item.price = item.price / 100

    return render(request, 'home.html', {'page_obj': page_obj})
