from django.db import IntegrityError, models, transaction as db_transaction # Use alias to prevent naming conflicts
from django.contrib.auth.models import AbstractUser,BaseUserManager

from django.db.models import Sum, Q, F
from decimal import Decimal
from django.core.validators import MinValueValidator # Prevents negative Numbers
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
# TruncMonth converts a date into the first day of its month
          # Example: 2026-03-15 → 2026-03-01
from django.db.models.functions import TruncMonth, Coalesce # ADDED: Coalesce to prevent 'None' values in charts
from django.db.models.functions import Coalesce



# ====================CUSTOM USER MANAGER==========================================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        try:
         user.save(using=self._db)
        except IntegrityError:
         raise ValueError("A user with this email already exists.")
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_admin'] = True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
#===================== USER MODEL ==========================================
class User(AbstractUser):
    """Custom User model using email as username"""
    username = None
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Role flags for dashboard access control
    is_admin = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
    
    @property
    def role(self):
        if self.is_superuser:
            return "Super Administrator"
        elif self.is_admin:
            return "Administrator"
        elif self.is_accountant:
            return "Accountant"

        return "Staff User"
    


# ==================== TEACHER MODEL ==================================
class Teacher(models.Model):
    """Complete Teacher model with salary tracking"""
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )  
    DESIGNATIONS = (
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('HOD', 'Head of Department'),
        ('Senior Teacher', 'Senior Teacher'),
        ('Teacher', 'Teacher'),
        ('Assistant Teacher', 'Assistant Teacher')
    )
# Link to User model (for portal access to the teacher if the admin want )
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='teacher_profile'
    )
# Fully delete the data of a user each and every thing  
    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)

# Professional ID
    teacher_id = models.CharField(max_length=20, unique=True, db_index=True)
# Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
# Professional Information
    qualification = models.CharField(max_length=200, blank=True)
    subject_specialization = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=50, choices=DESIGNATIONS, default='Teacher')
    date_of_joining = models.DateField() 
# Contact Information
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
# Salary Information
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),validators=[MinValueValidator(0)])
    total_salary_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    salary_due = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
# Bank Details (for salary transfer)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
# Status
    is_active = models.BooleanField(default=True)
# Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_salary_status(self):
        """Recalculate salary totals based on Salary records"""
        total = Salary.objects.filter(teacher=self).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        self.total_salary_paid = total
# Calculate expected salary based on months since joining
        months = self.calculate_months_since_joining()
        expected = self.monthly_salary * months
        self.salary_due = expected - self.total_salary_paid
# Use update() to avoid triggering signals/recursion
        self.__class__.objects.filter(pk=self.pk).update(
            total_salary_paid=self.total_salary_paid,
            salary_due=self.salary_due
        )
# Use for when every the teacher is joining the school and their salary calculation
    def calculate_months_since_joining(self):
        """Calculate months employed for salary calculation"""
        today = timezone.now().date()
        diff = relativedelta(today, self.date_of_joining)
        return diff.months + (diff.years * 12) + 1



# ==================== CLASS MODEL ==================================
class Class(models.Model):
    """ Model for school classes/grades """
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
        ('Class 5', 'Class 5'),
        ('Class 6', 'Class 6'),
        ('Class 7', 'Class 7'),
        ('Class 8', 'Class 8'),
        ('Class 9', 'Class 9'),
        ('Class 10', 'Class 10'),
        ('Class 11', 'Class 11'),
        ('Class 12', 'Class 12')
    ]
# Class Information
    name = models.CharField(max_length=20, choices=CLASS_CHOICES, db_index=True, unique=True)      
# Fee Structure
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0)])
# Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["name"] # Note: sort alphabetically (Class 1, Class 2).
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        
    def __str__(self):
        return self.name
        


#=================== SECTION MODEL ======================
class Section(models.Model):
    """Model for class sections (A, B, C...)"""
    name = models.CharField(max_length=5, default='A')
# One Class can have many Sections (ForeignKey relationship)
    student_class = models.ForeignKey("Class",
        on_delete=models.CASCADE,
        related_name="sections"
        )
    
# One Teacher can be assigned to one Section (ForeignKey relationship)
    class_teacher = models.ForeignKey("Teacher",on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="section_teacher"
        )

    capacity = models.PositiveIntegerField(default=40, validators=[MinValueValidator(1)])
# Status
    is_active = models.BooleanField(default=True)
# Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student_class", "name",]
        verbose_name = "Section"
        verbose_name_plural = "Sections" 
        # Merged constraints into a single list for better readability and performance 
    constraints = [
            models.UniqueConstraint(
                fields=["student_class", "name"], # No duplicate class-section combos
                name="unique_class_section"
            ),
            models.UniqueConstraint(
                fields=['class_teacher'],
                condition=Q(class_teacher__isnull=False),
                name='unique_class_teacher'
            )
        ] 

    def __str__(self):
        return f"{self.student_class.name} - {self.name}"

    @property
    def student_count(self):
        return self.students.count()

    @property
    def available_seats(self):
        return self.capacity - self.student_count


# ==================== STUDENT MODEL ====================
class Student(models.Model):
    """Student model for School Management System"""
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    
# Link to User model (optional - for portal access)
    user = models.OneToOneField(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile'
    )
# Personal Information of a Student
    photo = models.ImageField(upload_to="students/", blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5,choices=BLOOD_GROUP_CHOICES,blank=True,null=True )
# Academic Information of a Student
    admission_number = models.CharField(max_length=20, unique=True, db_index=True)
    roll_number = models.PositiveIntegerField(db_index=True, validators=[MinValueValidator(1)])
    
# One Class can have many Students (ForeignKey relationship)
    class_room = models.ForeignKey(
        'Class',
        on_delete=models.CASCADE,
        related_name='students'
    )
    
# One Section can have many Students (One-to-Many relationship)
    section = models.ForeignKey(
        "Section",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )
    
    admission_date = models.DateField(default=timezone.localdate)
# Contact Information
    phone_number = models.CharField(max_length=15, blank=True, db_index=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True, db_index=True)
    address = models.TextField()
# Fee Summary Fields (auto-calculated)
    total_fee_paid = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'),
                                         help_text="Auto-calculated from fee payments")
    total_fee_due = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'),
                                        help_text="Auto-calculated based on months enrolled")
# Status
    is_active = models.BooleanField(default=True)
# Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
            fields=['class_room','section','roll_number'],# No duplicate roll numbers in same class
            name='unique_roll_per_section'
            )
        ] 
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def clean(self):
        """Ensure that the selected section belongs to the selected class."""
        if self.section and self.section.student_class != self.class_room:
            raise ValidationError({"section": "The selected section does not belong to the chosen class."
        })
            
    def save(self, *args,**kwargs):
        self.full_clean()
        return super().save(*args,**kwargs)
    
    def update_fee_status(self):
        """Update fee status - calculate total paid and due amounts"""
# Calculate total fees paid by student
        total_paid = Fee.objects.filter(student=self).aggregate(
                                         total=Sum('amount')
                                        )['total'] or Decimal('0.00')  
           
# Calculate expected fee based on months since admission
        months_enrolled = self.calculate_months_since_admission()
        monthly_fee = self.class_room.monthly_fee
        total_expected = monthly_fee * months_enrolled
        
# Calculate amount due
        total_due = total_expected - total_paid
        
# Update fields using update() to avoid recursion
        self.__class__.objects.filter(pk=self.pk).update(total_fee_paid=total_paid,
            total_fee_due=max(total_due, Decimal("0.00"))
        )

    def calculate_months_since_admission(self):
        """Calculate months since admission for fee calculation"""
        today = timezone.now().date()
        diff = relativedelta(today, self.admission_date)
        return diff.months + (diff.years * 12) + 1
       
# String Representation
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"


    @property
    def full_name(self):
        """Returns student's full name"""
        return f"{self.first_name} {self.last_name}"



# ==================== EXPENSE/INCOME MODEL ====================
class Transaction(models.Model):
    """General school transactions for profit/loss tracking"""
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
     
    CATEGORIES = (
        ('fee', 'Student Fees'),
        ('salary', 'Teacher Salaries'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
        ('rent', 'Rent'),
        ('other_income', 'Other Income'),
        ('other_expense', 'Other Expense'),
    )
# Short title describing the transaction
    title = models.CharField(max_length=200)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="recorded_transactions"
                                    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-date', '-created_at'] # First order by latest transaction date, then by creation time
        indexes = [
        models.Index(fields=['date']),
        models.Index(fields=['transaction_type']),
        models.Index(fields=['category'])
        ]
        
    def __str__(self):
        return f"{self.title} - ({self.get_transaction_type_display()}) {self.amount}"
    
    
# Get monthly income vs expense for charts
    @classmethod
    def get_monthly_summary(cls, year=None):
        
        if not year: # If year is not provided, use the current year
            year = timezone.now().year
                                                # This allows grouping transactions by month
        return cls.objects.filter(date__year=year).annotate(month=TruncMonth('date')# TruncMonth converts a date
        # into the first day of its month Example: 2026-03-15 → 2026-03-01
        # Group results by the month field                                                     
        ).values('month').annotate( 
            # FIXED: Added Coalesce so charts get '0' instead of 'None' if no data exists
            total_income=Coalesce(Sum('amount', filter=Q(transaction_type='income')), Decimal('0.00')),    
            total_expense=Coalesce(Sum('amount', filter=Q(transaction_type='expense')), Decimal('0.00'))   
        ).order_by('month') # Order results chronologically from January to December
    


# Calculate total profit or loss for a given year  
    @classmethod
    def get_yearly_profit(cls, year=None):

        if not year:
           year = timezone.now().year
    # Aggregate total income and expense in one query
        result = cls.objects.filter(date__year=year).aggregate(
        # Sum of all income transactions
        # FIXED: Added Coalesce to prevent math errors on empty records
            total_income=Coalesce(Sum('amount', filter=Q(transaction_type='income')), Decimal('0.00')),
        # Sum of all expense transactions
        total_expense=Coalesce(Sum('amount', filter=Q(transaction_type='expense')), Decimal('0.00'))
        )
    # Handle None values if no transactions exist Return profit or loss
        return result['total_income'] - result['total_expense']
    
    
# Returns total transaction amount grouped by category.Useful for category-based charts.    
    @classmethod
    def get_category_totals(cls):
        
        return cls.objects.values('category').annotate(
            # Sum of all transactions in each category
            total_amount = Sum('amount')
        ).order_by('-total_amount')


# Calculate monthly profit or loss for a given year.       
    @classmethod
    def get_monthly_profit_loss(cls, year=None):
        
        if not year:
            year = timezone.now().year
            
        return cls.objects.filter(date__year=year).annotate(
            # Extract month from date
            month=TruncMonth('date') # TruncMonth converts a date into the first day of its month Example: 2026-03-15 → 2026-03-01
            
        ).values('month').annotate(
            
            # Monthly income
            # FIXED: Coalesced values to ensure profit calculation works
            total_income=Coalesce(Sum('amount', filter=Q(transaction_type='income')), Decimal('0.00')),
            # Monthly expense
            total_expense=Coalesce(Sum('amount', filter=Q(transaction_type='expense')), Decimal('0.00'))
        ).annotate(

        # F Use for the value from the database column when performing the calculation.
        profit=F('total_income') - F('total_expense')
                                # Profit = income - expense
        ).order_by('month')    


# ==================== FEE MODEL ====================
class Fee(models.Model):
    """Student fee payment records"""
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('check', 'Check'),
        ('online', 'Online Payment'),
    )
    
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('partial', 'Partial'),
    )
    
# One student can have multiple monthly fee payments
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='fee_payments'
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='fee_record',
        null=True,
        blank=True
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    month_for = models.DateField(help_text="Fee for which month/year", db_index=True)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True)
    
# Staff member who received the payment
    received_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_fees"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date']
        constraints = [
            models.UniqueConstraint(
                    fields=['student','month_for'],
                    name='unique_student_fee_month'
                )
            ]
        verbose_name = 'Fee Payment'
        verbose_name_plural = 'Fee Payments'


    def __str__(self):
        return f"{self.student.full_name} - {self.amount} ({self.month_for.strftime('%B %Y')})"

    def save(self, *args, **kwargs):
        with db_transaction.atomic(): # Ensure fee save and student fee status update happen in a single database transaction
                                      # ( Use the aliased db_transaction )
        # Check transaction_id to safely see if the relationship exists yet
        # CHANGED: Logic now updates the existing transaction if the Fee is edited
            transaction_data = {
                'title': f"Fee Payment - {self.student.full_name}",
                'transaction_type': 'income',
                'category': 'fee',
                'amount': self.amount,
                'date': self.payment_date,
                'recorded_by': self.received_by
            }

            if self.transaction:
                # FIXED: This ensures that if you change the Fee amount, the Transaction record also updates
                Transaction.objects.filter(id=self.transaction.id).update(**transaction_data)
            else:
                new_trans = Transaction.objects.create(**transaction_data)
                self.transaction = new_trans

            super().save(*args, **kwargs)
            
            # Use hasattr to ensure the student actually has this method
            if hasattr(self.student, 'update_fee_status'):
                self.student.update_fee_status()


# ==================== SALARY MODEL ====================
class Salary(models.Model):
    """Teacher salary payment records"""
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('check', 'Check'),
    )
    
    STATUS_CHOICES = (
        ('paid','Paid'),
        ('pending','Pending'),
        ('cancelled','Cancelled')
    )
# One Teacher can have multiple monthly Salary payments
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.CASCADE,
        related_name='salary_payments'
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='salary_record', 
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    month_for = models.DateField(help_text="Salary for which month/year", db_index=True)
    payment_date = models.DateField(default=timezone.now, db_index=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='bank')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='pending')
    bank_reference  = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
# User (admin/accountant) who recorded the payment
# If the user is deleted, the field will become NULL
    paid_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="salary_payments_recorded"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date','-month_for']
        constraints = [
            models.UniqueConstraint(
                fields=['teacher','month_for'], # Prevent duplicate salary records for the same teacher and month
                name='unique_teacher_salary_month'
            )
        ] 
        verbose_name = 'Salary Payment'
        verbose_name_plural = 'Salary Payments'

    def __str__(self):
        return f"{self.teacher.full_name} - {self.amount} ({self.month_for.strftime('%B %Y')})"
    
# Custom validation logic before saving the model.
    def clean(self):
        super().clean()
        
# Ensure salary amount is greater than zero
        if self.amount <= 0:
            raise ValidationError("Salary must be greater than zero.")
        
# Require transaction ID if payment method is bank transfer
        # Changed self.transaction_id to self.bank_reference
        if self.payment_method == 'bank' and not self.bank_reference:
            raise ValidationError("Bank Reference required for bank payments.")

    def save(self, *args, **kwargs):
        # Forces validation to run even when saving via script (not just forms)
        self.full_clean()

        with db_transaction.atomic(): # Ensure salary save and teacher salary status update happen in a single database transaction
         # Check transaction_id to safely see if the relationship exists yet
         # CHANGED: Logic now updates the existing transaction if the Salary is edited
            transaction_data = {
                'title': f"Salary Payment - {self.teacher.full_name}",
                'transaction_type': 'expense',
                'category': 'salary',
                'amount': self.amount,
                'date': self.payment_date,
                'recorded_by': self.paid_by
            }
            

            if self.transaction:
                # FIXED: Updates the expense record if salary amount/date changes
                Transaction.objects.filter(id=self.transaction.id).update(**transaction_data)
            else:
                new_trans = Transaction.objects.create(**transaction_data)
                self.transaction = new_trans

            super().save(*args, **kwargs)
            if hasattr(self.teacher, 'update_salary_status'):
                self.teacher.update_salary_status() # Update salary status on the related teacher model