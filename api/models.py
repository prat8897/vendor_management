from django.db import models
from django.utils import timezone
from django.db.models import Avg, Count, Q

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def update_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_pos = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()
        self.on_time_delivery_rate = (on_time_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        self.save()

    def update_quality_rating_avg(self):
        self.quality_rating_avg = self.purchaseorder_set.filter(
            status='completed', quality_rating__isnull=False
        ).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        self.save()

    def update_average_response_time(self):
        response_times = self.purchaseorder_set.filter(
            acknowledgment_date__isnull=False
        ).annotate(
            response_time=F('acknowledgment_date') - F('issue_date')
        ).values_list('response_time', flat=True)
        self.average_response_time = sum(response_times, timezone.timedelta()) / len(response_times) if response_times else timezone.timedelta()
        self.save()

    def update_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.count()
        fulfilled_pos = self.purchaseorder_set.filter(status='completed').count()
        self.fulfillment_rate = (fulfilled_pos / total_pos) * 100 if total_pos > 0 else 0
        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if not is_new and self.status == 'completed':
            self.vendor.update_on_time_delivery_rate()
            self.vendor.update_quality_rating_avg()
            self.vendor.update_fulfillment_rate()
        if self.acknowledgment_date:
            self.vendor.update_average_response_time()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"