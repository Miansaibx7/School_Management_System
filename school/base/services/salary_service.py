from django.db import transaction
from ..models import Salary
from .transaction_service import TransactionService


class SalaryService:

    @staticmethod
    def pay_salary(teacher,amount, month_for, payment_date, payment_method, paid_by):

        with transaction.atomic():
            # Create financial transaction also load the TransactionService
            transaction_record = TransactionService.create_expense(title=f"Salary Payment - {teacher.full_name}",
                category="salary", amount=amount, date=payment_date, user=paid_by)

            salary = Salary.objects.create(teacher=teacher, amount=amount, month_for=month_for, payment_date=payment_date,
                payment_method=payment_method, transaction=transaction_record, paid_by=paid_by)

            teacher.update_salary_status()

            return salary
