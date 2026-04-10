from django.conf import settings
from django.db import models
from django.utils import timezone


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField(help_text='Duration in days')

    class Meta:
        ordering = ['price', 'duration']

    def __str__(self):
        return f'{self.name} ({self.duration} days)'


class Subscription(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_EXPIRED = 'Expired'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.user.username} - {self.plan.name}'

    def refresh_status(self, commit=True):
        current_status = self.STATUS_ACTIVE if self.end_date >= timezone.localdate() else self.STATUS_EXPIRED
        if self.status != current_status:
            self.status = current_status
            if commit:
                self.save(update_fields=['status'])
        return self.status

    def save(self, *args, **kwargs):
        self.status = self.STATUS_ACTIVE if self.end_date >= timezone.localdate() else self.STATUS_EXPIRED
        super().save(*args, **kwargs)
