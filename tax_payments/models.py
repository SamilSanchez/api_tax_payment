from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError


METHOD_PAY = [
    ("debit_card", "Tarjeta de Débito"),
    ("credit_card", "Tarjeta de Crédito"),
    ("cash", "Efectivo"),
]

SERVICE_TYPE = [
    ("light", "LUZ"),
    ("water", "AGUA"),
    ("gas", "GAS"),
    ("internet", "INTERNET"),
]

PAYMENT_STATUS = [("pending", "Pendiente"), ("paid", "Pagada")]


def different_to_zero(number):
    """
    Función que valida si el numero es cero y retornar un error.
    """
    if number == 0:
        raise ValidationError("El valor debe ser diferente de cero")


def validate_number_greater_than_zero(number):
    """
    Función que valida si el número es menor que cero, para retornar un error.
    """

    if int(number) < 0:
        raise ValidationError("El valor debe ser mayor a cero")


def validate_date_less_than_actual(date):
    """
    Función que valida si la fecha es mayor a la actual.
    """

    if date > datetime.now().date():
        raise ValidationError("La fecha del mayor a la fecha actual")


class Tax(models.Model):
    """
    Representa las boletas creadas, con su status correspondiente (pending, paid, etc.)

    Tipo de servicio (Luz/Gas/etc...)
    Descripción del servicio. Ej: 'Edenor S.A.'
    Fecha de vencimiento. Ej (2021-01-15)
    Importe del servicio.
    Status del pago (pending, paid, etc.).
    Código de barra (debe ser único - PK)

    """

    barcode = models.CharField(
        primary_key=True,
        verbose_name="Código de barra",
        max_length=50,
        help_text="Identificador unico de la boleta.",
    )

    service_type = models.CharField(
        verbose_name="Tipo de servicio",
        max_length=100,
        choices=SERVICE_TYPE,
        help_text="Seleccione el sercicio adquirido",
    )

    payment_status = models.CharField(
        verbose_name="Estatus",
        max_length=100,
        choices=PAYMENT_STATUS,
        help_text="Estatus del pago",
        default="pending",
    )

    expiration_date = models.DateField(verbose_name="Fecha de vencimiento")

    description = models.TextField(
        verbose_name="Descripción", help_text="Descripcion breve del servicio"
    )

    def __str__(self) -> str:
        PAYMENT_STATUS = {
            "pending": "Pendiente",
            "paid": "Pagada",
        }
        SERVICE_TYPE = {
            "light": "LUZ",
            "water": "AGUA",
            "gas": "GAS",
            "internet": "INTERNET",
        }
        return f"Referencia: {self.barcode} | Servicio: {SERVICE_TYPE[self.service_type]} | Estatus del pago: {PAYMENT_STATUS[self.payment_status]}"


class TaxPayment(models.Model):
    """
    Representa la información de pagos, los datos de la tarjeta, el valor, etc.

    Método de pago (debit_card, credit_card o cash)
    Número de la tarjeta (solo en caso de no ser efectivo)
    Importe del pago
    Código de barra
    Fecha de pago
    """

    payable = models.OneToOneField(
        Tax,
        related_name="transactions",
        related_query_name="transaction",
        verbose_name="Boltea de pago",
        help_text="Boleta de pago de servicios a pagar",
        on_delete=models.PROTECT,
        unique=True,
    )

    pay_method = models.CharField(
        verbose_name="Método de pago",
        max_length=100,
        choices=METHOD_PAY,
        help_text="Seleccione el metodo de pago utilizado",
    )

    # TODO Agregar validacion del número de tarjeta
    card_number = models.IntegerField(
        verbose_name="Número de tarjeta",
        help_text="Solo en caso de no ser efectivo",
        validators=[],
        blank=True,
        null=True,
    )

    amount = models.FloatField(
        verbose_name="Importe del pago",
        validators=[different_to_zero, validate_number_greater_than_zero],
    )

    date = models.DateField(
        verbose_name="Fecha de pago", validators=[validate_date_less_than_actual]
    )

    def __str__(self) -> str:
        return f"Boleta: {self.payable} | Método de pago: {self.pay_method} | Monto: {self.amount}"
