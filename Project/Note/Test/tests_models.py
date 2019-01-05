from django.test import TestCase
from mixer.backend.django import mixer
import Note.models as models
from datetime import datetime, timedelta
import pytz
from Project.settings import TIME_ZONE


class TestNotes(TestCase):
    """
    Tests of my notes class
    """
    def setUp(self):
        mixer.blend('Note.notes')

    def test_instance_creation(self):
        """
        Test if there is an error after instance creation
        """
        note = models.Notes.objects.get(pk=1)
        self.assertIsInstance(note, models.Notes)
        self.assertTrue(note)

    def test_creation_date(self):
        """
        Test if creation date is Ok
        """
        now = datetime.now(pytz.timezone(TIME_ZONE))
        note = models.Notes.objects.get(pk=1)
        created_date = note.created_at
        created_date.replace(tzinfo=None)
        self.assertTrue((now - timedelta(seconds=50)) <= created_date <= now)


class TestCategory(TestCase):
    """
    Tests of my Category class
    """
    def setUp(self):
        mixer.blend('Note.category')
    
    def test_instance_creation(self):
        categorie = models.Category.objects.get(pk=1)
        self.assertIsInstance(categorie, models.Category)

    def test_creation_date(self):
        now = datetime.now(pytz.timezone(TIME_ZONE))
        categorie = models.Category.objects.get(pk=1)
        created_date = categorie.created_at
        created_date.replace(tzinfo=None)
        self.assertTrue((now - timedelta(seconds=50)) <= created_date <= now)