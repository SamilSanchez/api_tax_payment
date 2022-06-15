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


class FilterByDateTaxPaymentSerializer(serializers.Serializer):

    date = serializers.DateField()
    total_amount = serializers.FloatField()
    count = serializers.IntegerField()


class FilterByServiceTaxSerializer(serializers.ModelSerializer):

    expiration_date = serializers.SerializerMethodField()
    barcode = serializers.SerializerMethodField()

    class Meta:

        model = TaxPayment
        fields = ("expiration_date", "amount", "barcode")

    def get_expiration_date(self, obj):
        return obj.payable.expiration_date

    def get_barcode(self, obj):
        return obj.payable.barcode


class FilterByPaymentStatusTaxSerializer(serializers.ModelSerializer):

    service_type = serializers.SerializerMethodField()
    expiration_date = serializers.SerializerMethodField()
    barcode = serializers.SerializerMethodField()

    class Meta:

        model = TaxPayment
        fields = ("service_type", "expiration_date", "amount", "barcode")

    def get_service_type(self, obj):
        return obj.payable.service_type

    def get_expiration_date(self, obj):
        return obj.payable.expiration_date

    def get_barcode(self, obj):
        return obj.payable.barcode
