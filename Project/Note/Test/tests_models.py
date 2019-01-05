from django.test import TestCase
from mixer.backend.django import mixer
import Note.models as models


class TestNotes(TestCase):
    """
    Tests of my notes class
    """

    def test_instance_creation(self):
        note = mixer.blend('Note.notes')
        self.assertIsInstance(note, models.Notes)
