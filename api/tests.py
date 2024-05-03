import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder
from datetime import datetime, timedelta
from django.utils import timezone

class VendorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            "name": "Vendor Name1",
            "contact_details": "Contact Details",
            "address": "Vendor Address",
            "vendor_code": "VEN002"
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        url = reverse('vendor-list')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_retrieve_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        updated_data = {'name': 'Updated Vendor'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_performance(self):
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)

class PurchaseOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.po_data = {
            'po_number': 'PO001',
            'vendor': self.vendor,
            'items': {'item1': 10, 'item2': 20},
            'quantity': 30,
            'status': 'pending',
            'delivery_date': datetime.now() + timedelta(days=7)  # Add delivery_date field
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        po_data = {
            'po_number': 'PO002',
            'vendor': self.vendor.id,  # Use the vendor's ID instead of the object
            'items': {'item3': 5, 'item4': 10},
            'quantity': 15,
            'status': 'pending',
            'delivery_date': timezone.now() + timezone.timedelta(days=10)
        }
        response = self.client.post(url, po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_retrieve_purchase_order(self):
        url = reverse('purchaseorder-detail', args=[self.po.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.po_data['po_number'])

    def test_update_purchase_order(self):
        url = reverse('purchaseorder-detail', args=[self.po.id])
        updated_data = {'status': 'completed'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertEqual(self.po.status, updated_data['status'])

    def test_delete_purchase_order(self):
        url = reverse('purchaseorder-detail', args=[self.po.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        url = reverse('purchaseorder-acknowledge', args=[self.po.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertIsNotNone(self.po.acknowledgment_date)