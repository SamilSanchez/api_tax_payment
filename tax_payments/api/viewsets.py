import random

from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from tax_payments.api.serializers import (
    FilterByDateTaxPaymentSerializer,
    FilterByPaymentStatusTaxSerializer,
    FilterByServiceTaxSerializer,
    TaxSerializer,
    TaxPaymentSerializer,
)
from tax_payments.models import Tax, TaxPayment


def random_code(size=5):
    """
    Función para generar un codigo aleatorio, recibe como parametro el tamaño deseado.

    """
    letters = ["a", "b", "c", "d", "e", "h", "k", "m", "n", "s", "t", "u"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    values = letters + numbers
    code = ""

    for i in range(size):
        code += str(random.choice(values))

    return code


class TaxViewSet(viewsets.ViewSet):
    """
    Administrar las boletas (impuestos) de servicios
    """

    serializer_class = TaxSerializer
    pagination_classes = (IsAuthenticated,)
    queryset = Tax.objects.all()

    def list(self, request):
        """
        Muestra la lista de boletas (impuestos) de servicio
        """
        params = request.query_params
        service_type = params.get("service_type")
        payment_status = params.get("payment_status")

        if service_type:
            queryset = TaxPayment.objects.filter(
                payable__service_type=service_type
            ).all()
            serializer = FilterByServiceTaxSerializer(queryset, many=True)
            return Response(
                {"status_code": status.HTTP_200_OK, "taxs": serializer.data}
            )

        elif payment_status:
            queryset = TaxPayment.objects.filter(
                payable__payment_status=payment_status
            ).all()
            serializer = FilterByPaymentStatusTaxSerializer(queryset, many=True)
            return Response(
                {"status_code": status.HTTP_200_OK, "taxs": serializer.data}
            )

        serializer = self.serializer_class(self.queryset, many=True)
        return Response({"status_code": status.HTTP_200_OK, "taxs": serializer.data})

    def create(self, request):
        """
        Crear una boleta (impuesto) de servicio
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            validated_data = serializer.validated_data
            validated_data["barcode"] = f"tax_{random_code(size=8)}"
            Tax.objects.create(**validated_data)
            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "new_tax": serializer.validated_data,
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class TaxPaymentViewSet(viewsets.ViewSet):
    """
    Administrar loas pagos de la boletas (impuestos) de servicios
    """

    serializer_class = TaxPaymentSerializer
    pagination_classes = (IsAuthenticated,)
    queryset = TaxPayment.objects.all()

    def list(self, request):
        """
        Muestra la lista de pagos de boleta (impuesto)
        """
        params = request.query_params
        date_initial = params.get("date_initial")
        date_end = params.get("date_end")

        if date_initial and date_end:
            import datetime as dt

            year1 = int(date_initial.split("/")[2])
            month1 = int(date_initial.split("/")[1])
            day1 = int(date_initial.split("/")[0])

            year2 = int(date_end.split("/")[2])
            month2 = int(date_end.split("/")[1])
            day2 = int(date_end.split("/")[0])

            start = dt.date(
                year1,
                month1,
                day1,
            )
            end = dt.date(
                year2,
                month2,
                day2,
            )

            result = (
                TaxPayment.objects.filter(date__range=[start, end])
                .values("date")
                .annotate(total_amount=Sum("amount"))
                .annotate(count=Count("*"))
                .order_by("date")
            )

            serializer = FilterByDateTaxPaymentSerializer(result, many=True)
            return Response(
                {"status_code": status.HTTP_200_OK, "tax_payments": serializer.data}
            )

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(
            {"status_code": status.HTTP_200_OK, "tax_payments": serializer.data}
        )

    def create(self, request):
        """
        Crear una nuevo pago de boleta (impuesto)
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            tax_payment = TaxPayment.objects.create(**validated_data)
            tax_payment.payable.payment_status = "paid"
            tax_payment.payable.save()
            return Response(
                {"status_code": status.HTTP_201_CREATED, "tax_id": tax_payment.id}
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
