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
        self.manually_created_note1 = models.Notes(title = "Test", body = "Body of my test note")
        self.manually_created_note1.save()
        self.manually_created_note2 = models.Notes(title = "Test", body = "Body of my second test note")
        self.manually_created_note2.save()

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

    def test_slug_format(self):
        """
        Test if slug field is correctly set up
        """
        note = models.Notes.objects.get(pk=1)
        note.save()
        now = datetime.now(pytz.timezone(TIME_ZONE))
        title = note.title
        formated_title = title.replace(" ", "-")
        formated_title = formated_title.lower()
        expected_slug_field = "-".join([formated_title, str(now.day), str(now.month), str(now.year)])
        self.assertEqual(note.slug, expected_slug_field)

    def test_manually_created_note(self):
        """
        Test if a note created manually with only title and body is working
        To verify that we will check is the instance of note is created
        We will also check if there is a value in slug field
        """
        self.assertIsInstance(self.manually_created_note1, models.Notes)
        self.assertIsNotNone(self.manually_created_note1.slug)


    def test_if_there_is_duplicate_slug_field(self):
        """
        My default rule for slugfield can potentially generate two identif slug if
        the same day two notes are create. We will check if there is correctly a correct
        incrementation of a counter who permit to distingue those notes
        """
        self.assertNotEqual(self.manually_created_note1.slug, self.manually_created_note2.slug)



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