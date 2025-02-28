from django.db import models


class Item(models.Model):
    """
    Модель товара.

    Атрибуты:
        name (CharField): Название товара.
        description (TextField): Описание товара.
        price (IntegerField): Цена товара в центах.
        currency (CharField): Валюта товара (по умолчанию 'usd').
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()  # Цена в центах
    currency = models.CharField(max_length=3, default='usd')  # Валюта товара ('usd', 'eur', и т.д.)

    def __str__(self):
        return self.name


class Discount(models.Model):
    """
    Модель скидки.

    Атрибуты:
        name (CharField): Название скидки.
        amount (DecimalField): Сумма скидки.
    """
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма скидки

    def __str__(self):
        return self.name


class Tax(models.Model):
    """
    Модель налога.

    Атрибуты:
        name (CharField): Название налога.
        percentage (DecimalField): Процент налога (например, 20.00 для 20%).
    """
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Например, 20.00 для 20%

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель заказа.

    Атрибуты:
        items (ManyToManyField): Список товаров в заказе.
        total_price (DecimalField): Итоговая стоимость заказа.
        discount (ForeignKey): Примененная скидка (может отсутствовать).
        tax (ForeignKey): Примененный налог (может отсутствовать).
    """
    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def calculate_total_price(self):
        """
        Пересчитывает общую стоимость заказа, включая скидку и налог.
        """
        total = sum(item.price for item in self.items.all())

        if self.discount:
            total -= self.discount.amount  # Учитываем скидку (если есть)
            total = max(total, 0)  # Защита от отрицательных цен

        if self.tax:
            total += total * (self.tax.percentage / 100)  # Добавляем налог

        self.total_price = round(total, 2)  # Округляем до 2 знаков после запятой
        self.save()

    def set_discount(self, discount):
        """
        Присваивает скидку к заказу и пересчитывает стоимость.

        Аргументы:
            discount (Discount): Экземпляр скидки.
        """
        self.discount = discount
        self.calculate_total_price()
        self.save()

    def set_tax(self, tax):
        """
        Присваивает налог к заказу и пересчитывает стоимость.

        Аргументы:
            tax (Tax): Экземпляр налога.
        """
        self.tax = tax
        self.calculate_total_price()
        self.save()
