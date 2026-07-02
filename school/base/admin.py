from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    User,
    Teacher,
    Class,
    Section,
    Student,
    Transaction,
    Fee,
    Salary
)

# ==================== User Admin ====================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_accountant')
    search_fields = ('email', 'name', 'phone')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'bio', 'phone', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_accountant', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

# ==================== Teacher Admin ====================
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'teacher_id', 'designation', 'phone_number', 'is_active')
    search_fields = ('first_name', 'last_name', 'teacher_id', 'email', 'phone_number')
    list_filter = ('designation', 'gender', 'is_active')
    ordering = ('-created_at',)
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'photo')}),
        ('Professional Information', {'fields': ('teacher_id', 'qualification', 'subject_specialization', 'designation', 'date_of_joining')}),
        ('Contact', {'fields': ('phone_number', 'email', 'address', 'emergency_contact')}),
        ('Salary & Bank', {'fields': ('monthly_salary', 'total_salary_paid', 'salary_due', 'bank_name', 'account_number', 'ifsc_code')}),
        ('Status & Timestamps', {'fields': ('is_active', 'user', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'total_salary_paid', 'salary_due')

# ==================== Class Admin ====================
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_fee', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('name',)

# ==================== Section Admin ====================
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('student_class', 'name', 'class_teacher', 'capacity', 'student_count', 'is_active')
    search_fields = ('name',)
    list_filter = ('student_class', 'is_active')
    ordering = ('student_class', 'name')
    readonly_fields = ('student_count', 'available_seats')

# ==================== Student Admin ====================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'admission_number', 'class_room', 'section', 'roll_number', 'is_active')
    search_fields = ('first_name', 'last_name', 'admission_number', 'phone_number', 'email')
    list_filter = ('class_room', 'section', 'gender', 'is_active')
    ordering = ('-created_at',)
    fieldsets = (
        ('Personal', {'fields': ('first_name', 'last_name', 'father_name', 'mother_name', 'gender', 'date_of_birth', 'blood_group', 'photo')}),
        ('Academic', {'fields': ('admission_number', 'roll_number', 'class_room', 'section', 'admission_date')}),
        ('Contact', {'fields': ('phone_number', 'guardian_name', 'guardian_phone', 'email', 'address')}),
        ('Fee Summary', {'fields': ('total_fee_paid', 'total_fee_due')}),
        ('Status', {'fields': ('is_active', 'user', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'total_fee_paid', 'total_fee_due')

# ==================== Transaction Admin ====================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'transaction_type', 'category', 'amount', 'date', 'recorded_by')
    search_fields = ('title', 'description', 'receipt_number')
    list_filter = ('transaction_type', 'category', 'date')
    ordering = ('-date',)

# ==================== Fee Admin ====================
@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'month_for', 'status', 'payment_date', 'payment_method')
    search_fields = ('student__first_name', 'student__last_name', 'notes')
    list_filter = ('status', 'payment_method', 'payment_date')
    ordering = ('-payment_date',)

# ==================== Salary Admin ====================
@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'amount', 'month_for', 'status', 'payment_date', 'payment_method')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'bank_reference')
    list_filter = ('status', 'payment_method', 'payment_date')
    ordering = ('-payment_date',)

# if you still want to use admin.site.register, do it only once:
# admin.site.register(User, UserAdmin)  # NOT needed if you used the decorator