from django.db import transaction
from ..models import Fee
from .transaction_service import TransactionService


class FeeService:
    """
    Handles all student fee related operations.
    """

    @staticmethod
    def create_fee_payment(
        student,
        amount,
        month_for,
        payment_date,
        payment_method,
        received_by
    ):

        with transaction.atomic():

            # Create financial transaction
            transaction_record = TransactionService.create_income(
                title=f"Fee Payment - {student.full_name}",
                category="fee",
                amount=amount,
                date=payment_date,
                user=received_by
            )

            # Create fee record
            fee = Fee.objects.create(
                student=student,
                amount=amount,
                month_for=month_for,
                payment_date=payment_date,
                payment_method=payment_method,
                transaction=transaction_record,
                received_by=received_by
            )

            # Update student's fee summary
            student.update_fee_status()

            return fee
