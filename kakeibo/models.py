from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError


# Create your models here.


class Category(models.Model):
    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Category"

    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


def check_length(value):
    if value < 0 or value > 10000000:
        raise ValidationError("Range from 0 to 10000000")


class Kakeibo(models.Model):
    class Meta:
        db_table = "kakeibo"
        verbose_name = "Kakeibo"
        verbose_name_plural = "Kakeibo"

    date = models.DateField(
        verbose_name="Date", default=datetime.now, help_text="Please use format 'yyyy-mm-dd' ")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Category")
    money = models.IntegerField(
        verbose_name="Fee", help_text="Australia dollars", validators=[check_length])
    memo = models.CharField(verbose_name="Memo", max_length=500)

    def __str__(self):
        return self.memo


class Goals(models.Model):
    class Meta:
        db_table = "goal"
        verbose_name = "Goal"
        verbose_name_plural = "Goal"

    weekly_goal = models.IntegerField(
        verbose_name="weeklyGoal", help_text="Setting goal per week",
        validators=[check_length])
    mothly_goal = models.IntegerField(
        verbose_name="monthlyGoal", help_text="Setting goal per month", validators=[check_length])

    TERM_CHOICES = (
        ("Week", 'Week'),
        ("Month", 'Month'),
    )
    memo = models.CharField(verbose_name="Memo", max_length=5,
                            choices=TERM_CHOICES, help_text="Please choose 'Week' or 'Month'")

    def __str__(self):
        return self.memo
