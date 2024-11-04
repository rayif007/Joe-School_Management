from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Custom User model with roles
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', _('Admin')),
        ('staff', _('Office Staff')),
        ('librarian', _('Librarian')),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Student model
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    class_name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()  # Age will not accept negative values

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()  # Display full name in the dropdown

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")


# Book model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")


# Library History model
class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="library_history")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_history")
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name()} borrowed '{self.book.title}'"

    class Meta:
        verbose_name = _("Library History")
        verbose_name_plural = _("Library Histories")


# Fees History model
class FeesHistory(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', _('Paid')),
        ('pending', _('Pending')),
        ('failed', _('Failed')),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees_history")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Fees for {self.student.full_name()} - {self.amount} ({self.get_payment_status_display()})"

    class Meta:
        verbose_name = _("Fees History")
        verbose_name_plural = _("Fees Histories")





