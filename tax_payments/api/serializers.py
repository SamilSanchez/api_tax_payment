import random
from rest_framework import serializers
from tax_payments.models import Tax, TaxPayment


def random_code(size=5):
    """
    Función para generar un codigo aleatorio, recibe como parametro el tamaño deseado.

    """
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "j",
        "k",
        "m",
        "n",
        "r",
        "s",
        "t",
        "u",
        "v",
        "W",
    ]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    values = letters + numbers
    code = ""

    for i in range(size):
        code += str(random.choice(values))

    return code


class TaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tax
        fields = "__all__"
        read_only_fields = ("id", "barcode", "payment_status")


class TaxPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxPayment
        fields = "__all__"
        read_only_fields = ("id",)

    def validate(self, data):
        """
        Validaciones adicionales que requiere la logica del negocio
        """
        if data["pay_method"] == "cash" and data["card_number"]:
            raise serializers.ValidationError("El metodo de pago seleccionado fue en efectivo, debe borrar el campo de número de tarjeta")

        if data["pay_method"] != "cash" and not data["card_number"]:
            raise serializers.ValidationError("Debe colocar el número de tarjeta")

        return data


    def create(self, validated_data):
        """
        Logica negocio adicional cuando se crea una boleta (impuesto) de servicio
        """
        validated_data["barcode"] = f"tax_{random_code(size=8)}"
        return super().create(validated_data)


# class TaxSerializer(serializers.ModelSerializer):

#     customized_field = serializers.SerializerMethodField()

#     class Meta:
#         model = Tax
#         fields = "__all__"
#         read_only_fields = ("id",)
        # More values in https://www.django-rest-framework.org/api-guide/fields/
        # write_only: El campo solo se va poder escribir (POST)
        # read_only: El campo solo se va poder leer (GET)
        # required: El campo se marca como requerido
#         extra_kwargs = {
#             "description": {"write_only": True},
#         }

#     def get_customized_field(self, obj):
#         return "Campo perzonalizado"



# class ProvinceSerializer(serializers.Serializer):
#     """
#     Serializador para provincias
#     """

#     name = serializers.CharField(max_length=50)


