import json
import random

from django.core.serializers import json as json_serializar

from rest_framework import viewsets, filters as df
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status

from tax_payments.api.serializers import TaxSerializer, TaxPaymentSerializer
from tax_payments.models import Tax, TaxPayment

# from prisma.apps.base.api.permissions import ValidatePermissionAll
# from prisma.apps.base.models import StatusCodeInfo
# from prisma.apps.base.api.paginations import SmallResultSetPagination
# from prisma.apps.base.api.serializers import ProvinceSerializer, StatusCodeModelSerializer


"""
Viewsets: 

- Se encarga de la logica comun (crear, actualizar, leer, eliminar)
- Bueno para operaciones estandar de la bases de datos
- Forma mas rapida de hacer interfaz con base de datos

Cuando usamos viewsets ?

- CRUD simple
- API Simple
- Poca personalizacion de logica
- Trabaja con estructuras de datos normales

Usan funciones de operadores de modelos:
def list() -> enlista objetos
    create() -> crea objeto
    retrieve() -> obtiene objeto especifico
    update() -> actualiza objeto
    partial_update() -> actualiza parcialmente un objeto
    destroy() -> Elimina objeto
"""

# Algunas Vista Genericas para realizar dos o mas metodos metodos http con la misma url
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView

# Al heredar de “ModelViewSet” el API que expondremos será CRUD
# class StatusCodeModelViewSet(viewsets.ModelViewSet):
#     """
#     CRUD para los estados de respuesta http.
#     """

#     model = StatusCodeInfo
#     queryset = StatusCodeInfo.objects.all()
#     serializer_class = StatusCodeModelSerializer
#     permission_classes = (IsAuthenticated, ValidatePermissionAll)
#     pagination_class = SmallResultSetPagination
#     filter_backends = (
#         df.OrderingFilter,
#         df.SearchFilter,
#     )
#     search_fields = ("name",)
#     ordering_fields = ("name",)


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

    def list(self, request):
        """
        Muestra la lista de boletas (impuestos) de servicio
        """
        taxs = Tax.objects.all()
        _json = json_serializar.Serializer()
        taxs = json.loads(_json.serialize(taxs))
        return Response({"status_code": status.HTTP_200_OK, "taxs": taxs})

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

    def retrieve(self, request, pk=None):
        """
        Obtener solo una boleta (impuesto) de servicio
        """
        return Response({"http_method": "GET"})

    def update(self, request, pk=None):
        """
        Actualizar los datos de una boleta (impuesto) de servicio
        """
        return Response({"http_method": "PUT"})

    def partital_update(self, request, pk=None):
        """
        Actualizar los datos parcialmente de una de boleta (impuesto)  de servicio
        """
        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk=None):
        """
        Eliminar de boleta (impuesto) de servicio
        """
        return Response({"http_method": "DELETE"})


class TaxPaymentViewSet(viewsets.ViewSet):
    """
    Administrar loas pagos de la boletas (impuestos) de servicios
    """

    serializer_class = TaxPaymentSerializer
    pagination_classes = (IsAuthenticated,)

    def list(self, request):
        """
        Muestra la lista de pagos de boleta (impuesto)
        """
        taxs_pays = TaxPayment.objects.all()
        _json = json_serializar.Serializer()
        list_taxs_pays = json.loads(_json.serialize(taxs_pays))
        return Response(
            {"status_code": status.HTTP_200_OK, "tax_payments": list_taxs_pays}
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

    def retrieve(self, request, pk=None):
        """
        Obtener un pago de boleta (impuesto)
        """
        return Response({"http_method": "GET"})

    def update(self, request, pk=None):
        """
        Actualizar un pago de boleta (impuesto)
        """
        return Response({"http_method": "PUT"})

    def partital_update(self, request, pk=None):
        """
        Actualizar los datos parcialmente de un pago de boleta (impuesto)
        """
        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk=None):
        """
        Eliminar una de boleta (impuesto)
        """
        return Response({"http_method": "DELETE"})
