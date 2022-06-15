from rest_framework import serializers
from tax_payments.models import Tax, TaxPayment


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
            raise serializers.ValidationError(
                "El metodo de pago seleccionado fue en efectivo, debe borrar el campo de número de tarjeta"
            )

        if data["pay_method"] != "cash" and not data["card_number"]:
            raise serializers.ValidationError("Debe colocar el número de tarjeta")

        return data
