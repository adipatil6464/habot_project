from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Employee
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class EmployeeAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Create a user for authentication and employee data       
        """
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.employee_data = {
            "name": "Test1",
            "email": "test1@example.com",
            "department": "Engineering",
            "role": "Developer"
        }

        # Generate a token for the test user
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)

    def setUp(self):
        """
        Include the token in the headers for each request
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_employee(self):
        """
        create employee
        """
        url = reverse('employee-list-create')
        response = self.client.post(url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.employee_data['name'])

    def test_list_employees(self):
        """
        list of an employee test
        """
        Employee.objects.create(**self.employee_data)

        url = reverse('employee-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_employee(self):
        """
        single employee retrieve test
        """
        employee = Employee.objects.create(**self.employee_data)
        url = reverse('employee-detail', args=[employee.id])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee_data['name'])

    def test_update_employee(self):
        """
        employee update test
        """
        employee = Employee.objects.create(**self.employee_data)
        url = reverse('employee-detail', args=[employee.id])
        updated_data = {
            "name": "John Smith",
            "email": "johnsmith@example.com",
            "department": "Sales",
            "role": "Manager"
        }

        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_employee(self):
        """
        employee delete test
        """
        employee = Employee.objects.create(**self.employee_data)
        url = reverse('employee-detail', args=[employee.id])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=employee.id).exists())

    def test_create_employee_with_existing_email(self):
        """
        create another employee with the same email
        """
        Employee.objects.create(**self.employee_data)
        
        url = reverse('employee-list-create')
        response = self.client.post(url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
