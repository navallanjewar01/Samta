from django.test import TestCase
from .models import CustomUser, Tenant

class CustomUserModelTest(TestCase):
    def setUp(self):
        # Create a test tenant
        self.tenant = Tenant.objects.create(name='Test Tenant', domain_url='test.com', schema_name='test_schema')

    def test_custom_user_creation(self):
        # Test creating a custom user
        user = CustomUser.objects.create_user(email='test@example.com', phone_number='1234567890', password='test123', tenant=self.tenant)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertTrue(user.check_password('test123'))
        self.assertFalse(user.is_staff)

    # Add more tests as needed...

class TenantModelTest(TestCase):
    def test_tenant_creation(self):
        # Test creating a tenant
        tenant = Tenant.objects.create(name='Test Tenant', domain_url='test.com', schema_name='test_schema')
        self.assertEqual(tenant.name, 'Test Tenant')
        self.assertEqual(tenant.domain_url, 'test.com')
        self.assertEqual(tenant.schema_name, 'test_schema')

  
