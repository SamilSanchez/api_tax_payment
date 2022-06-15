from dataclasses import fields
from django_filters.rest_framework import FilterSet
from prisma.apps.conciliation.models import BankCashAndOther


class SpecialFilterBank(FilterSet):
    class Meta:
        model = BankCashAndOther
        fields = {"name": ["exact", "icontains"]}
