from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from .models import StatsArtist


class StatsArtistModelTests(TestCase):
    def test_last_seen_with_future_date(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        today = date.today()
        for art in StatsArtist.objects.all():
            self.assertIs(art.last_seen <= today, True)


class IndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Last API Caller")