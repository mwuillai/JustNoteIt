from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestIdentification(TestCase):
    """
    Test of the identifiacation views.
    It's in the same time an identification view and
    a sign in view. So we well tests potential interaction between
    those two forms.
    """
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()
        self.client_with_account = Client()
        self.client_without_account = Client()


    def test_identification_view_work(self):
        "Test if getting the view is working"
        view = self.client_with_account.get(reverse('identification'))
        self.assertEqual(200, view.status_code)


    def test_login_with_right_login(self):
        """Test if after the identification with right login the user is on the dashboard
        we will also verify that the request has not create a new user"""
        users_number_before = User.objects.count()
        response = self.client_with_account.post(
            reverse('identification'),
            {'username':'test', 'password':'test', 'Authentication':'Authentication'}
            )
        users_number_after = User.objects.count()
        self.assertEqual(302, response.status_code)
        self.assertIn('_auth_user_id', self.client_with_account.session)
        self.assertEqual(users_number_after, users_number_before)


    def test_login_with_wrong_login(self):
        """Test if after the identification with right login the user is on the dashboard
        we will also verify that the request has not create a new user"""
        users_number_before = User.objects.count()
        response = self.client_with_account.post(
            reverse('identification'),
            {'username':'test2', 'password':'test', 'Authentication':'Authentication'}
            )
        users_number_after = User.objects.count()
        self.assertEqual(302, response.status_code)
        self.assertNotIn('_auth_user_id', self.client_with_account.session)
        self.assertEqual(users_number_after, users_number_before)

    def test_creation_account(self):
        """ Test if the accout creation work"""
        users_number_before = User.objects.count()
        response = self.client_without_account.post(
            reverse('identification'),
            {'username':'test789',
             'password1':'test245*',
             'password2':'test245*',
             'Sign up':'Sign up'},
             follow = True
            )
        self.assertRedirects(response, '/?next=/dashboard/', status_code=302,
        target_status_code=200,msg_prefix='', fetch_redirect_response=True)
        self.assertNotIn('_auth_user_id', self.client_with_account.session)
        users_number_after = User.objects.count()
        self.assertEqual(users_number_after, users_number_before+1)


    def test_creation_account_with_wrong_password(self):
        """ Test if the accout creation fail with wrong password"""
        users_number_before = User.objects.count()
        response = self.client_without_account.post(
            reverse('identification'),
            {'username':'test789', 'password1':'test24', 'password2':'test22', 'Sign up':'Sign up'},
            follow = True
            )
        users_number_after = User.objects.count()
        self.assertRedirects(response, '/', status_code=302,
        target_status_code=200,msg_prefix='', fetch_redirect_response=True)
        self.assertNotIn('_auth_user_id', self.client_with_account.session)
        self.assertEqual(users_number_after, (users_number_before))

class TestDashboard(TestCase):
    """
    Test Dashboard
    A logged user can access to this page.
    A visitor must be redirect to the identification view
    """
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()
        self.client_with_account = Client()
        self.client_with_account.login(username='test', password='test')
        self.client_without_account = Client()

    def test_log_user(self):
        """
        test if a log user can access to the dashboard
        """
        response = self.client_with_account.get(reverse('dashboard'))
        self.assertEqual(200, response.status_code)

    def test_unlog_user(self):
        """
        test if a visitor is redirect
        """
        response = self.client_without_account.get(reverse('dashboard'), follow=True)
        self.assertRedirects(
            response,
            '/?next=/dashboard/',
            status_code=302,
            target_status_code=200)
