from django.db import transaction
from ..models import Transaction


class TransactionService:
    """
    Handles creation of financial transactions.
    """

    @staticmethod
    def create_income(title, category, amount, date, user=None, description=""):

        return Transaction.objects.create(
            title=title,
            transaction_type="income",
            category=category,
            amount=amount,
            date=date,
            recorded_by=user,
            description=description
        )


    @staticmethod
    def create_expense(title, category, amount, date, user=None, description=""):

        return Transaction.objects.create(
            title=title,
            transaction_type="expense",
            category=category,
            amount=amount,
            date=date,
            recorded_by=user,
            description=description
        )
