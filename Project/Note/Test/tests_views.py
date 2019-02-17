from django.test import TestCase, Client
from django.contrib.auth.models import User
from Note.models import Notes, Category
from django.urls import reverse
from datetime import datetime
import pytz
from Project.settings import TIME_ZONE

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
        view = self.client_with_account.get(reverse('Note:identification'))
        self.assertEqual(200, view.status_code)


    def test_login_with_right_login(self):
        """Test if after the identification with right login the user is on the dashboard
        we will also verify that the request has not create a new user"""
        users_number_before = User.objects.count()
        response = self.client_with_account.post(
            reverse('Note:identification'),
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
            reverse('Note:identification'),
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
            reverse('Note:identification'),
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
            reverse('Note:identification'),
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
        response = self.client_with_account.get(reverse('Note:dashboard'))
        self.assertEqual(200, response.status_code)

    def test_unlog_user(self):
        """
        test if a visitor is redirect
        """
        response = self.client_without_account.get(reverse('Note:dashboard'), follow=True)
        self.assertRedirects(
            response,
            '/?next=/dashboard/',
            status_code=302,
            target_status_code=200)

class TestDetailNote(TestCase):
    """
    Test detail note view
    """
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()
        self.client_with_account = Client()
        self.client_with_account.login(username='test', password='test')
        self.client_without_account = Client()
        self.note = Notes(title = "Test", body = "Body of my test note", created_at = datetime.now(pytz.timezone(TIME_ZONE)))
        self.note.save()

    def test_log_user(self):
        """
        test if a log user can access to the test note
        """
        response = self.client_with_account.get(reverse('Note:detail', args=([self.note.slug])))
        self.assertEqual(200, response.status_code)

    def test_unlog_user(self):
        """
        test if a visitor is redirect
        """
        response = self.client_without_account.get(reverse('Note:detail', args=([self.note.slug])), follow=True)
        self.assertRedirects(
            response,
            '/?next=' + reverse('Note:detail', args=([self.note.slug])),
            status_code=302,
            target_status_code=200)


class TestDetailCategory(TestCase):
    """
    Test detail Category view
    """
    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()
        self.client_with_account = Client()
        self.client_with_account.login(username='test', password='test')
        self.client_without_account = Client()
        self.category = Category(title = "Test", created_at = datetime.now(pytz.timezone(TIME_ZONE)))
        self.category.save()
        self.note = Notes(title = "Test", body = "Body of my test note", created_at = datetime.now(pytz.timezone(TIME_ZONE)))
        self.note.save()
        self.category.notes_id.add(self.note)
        

    def test_log_user(self):
        """
        test if a log user can access to the test category
        """
        response = self.client_with_account.get(reverse('Note:category', args=([self.category.slug])))
        self.assertEqual(200, response.status_code)

    def test_unlog_user(self):
        """
        test if a visitor is redirect
        """
        response = self.client_without_account.get(reverse('Note:category', args=([self.category.slug])), follow=True)
        self.assertRedirects(
            response,
            '/?next=' + reverse('Note:category', args=([self.category.slug])),
            status_code=302,
            target_status_code=200)



class TestDeleteNoteView(TestCase):
    """
    Test detail note view
    Test if delete note work for owner of the note
    Test if delete note return 404 error for someone who delete a note doesn't own
    """
    def setUp(self):
        user_with_note = User.objects.create_user('test', 'test@test.com', 'test')
        user_with_note.save()
        user_without_note = User.objects.create_user('test_without_note','test_without_note@test.com', 'test')
        user_without_note.save()
        self.client_with_account_with_note = Client()
        self.client_with_account_with_note.login(username='test', password='test')
        self.client_without_account = Client()
        self.client_with_account_without_note = Client()
        self.client_with_account_without_note.login(username='test_without_note', password='test')
        self.note = Notes(
            title = "Test",
            body = "Body of my test note",
            created_at = datetime.now(pytz.timezone(TIME_ZONE)),
            user_id = user_with_note)
        self.note.save()
        

    def test_delete_as_not_owner(self):
        """
        test to delete a note you don't own
        """
        amount_of_note_before_delete = Notes.objects.count()
        response = self.client_with_account_without_note.post(reverse('Note:delete_note', args=([self.note.slug])))
        self.assertEqual(404, response.status_code) 
        self.assertEqual(Notes.objects.count(), amount_of_note_before_delete )

    def test_delete_as_visitor(self):
        """
        test if a visitor is redirect
        """
        response = self.client_without_account.post(reverse('Note:delete_note', args=([self.note.slug])), follow=True)
        self.assertRedirects(
            response,
            '/?next=' + reverse('Note:delete_note', args=([self.note.slug])),
            status_code=302,
            target_status_code=200)
    
    def test_delete_as_owner(self):
        """
        test to delete a note you don't own
        """
        amount_of_note_before_delete = Notes.objects.count()
        response = self.client_with_account_with_note.post(reverse('Note:delete_note', args=([self.note.slug])))
        self.assertEqual(302, response.status_code)
        self.assertEqual(Notes.objects.count(), amount_of_note_before_delete - 1 )
