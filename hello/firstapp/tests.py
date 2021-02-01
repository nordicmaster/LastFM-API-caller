from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import StatsArtist


class StatsArtistModelTests(TestCase):
    def test_last_seen_with_future_date(self):
        """
        all of StatsArtist objects have valid last_seen date (past)
        """
        today = date.today()
        for art in StatsArtist.objects.all():
            self.assertIs(art.last_seen <= today, True)


class IndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Last API Caller - this text is available on Index page
        """
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Last API Caller")
