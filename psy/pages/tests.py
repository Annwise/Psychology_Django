from django.test import TestCase, Client
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_home_page(self):
        """Тест: главная страница доступна"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        """Тест: страница регистрации доступна"""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Тест: страница входа доступна"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_requires_login(self):
        """Тест: личный кабинет требует входа"""
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_booking_form_invalid_data(self):
        """Тест: форма записи возвращает ошибку при отсутствии документов"""
        response = self.client.post('/booking/', {
            'name': 'Test Name',
            'phone': '+79991234567',
            'email': 'test@example.com',
            'message': 'Test message'
        })
        # Проверяем, что возвращается JSON с ошибкой
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json())
        self.assertIn('Документы', response.json()['error'])
