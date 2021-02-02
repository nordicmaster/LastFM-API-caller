import random
import string
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus
from .models import StatsArtist


class StatsArtistModelTests(TestCase):
    def test_last_seen_with_valid_date(self):
        """
        all of StatsArtist objects have valid last_seen date (past)
        """
        today = date.today()
        for art in StatsArtist.objects.all():
            self.assertIs(art.last_seen <= today, True)


class IndexViewTests(TestCase):
    def test_index_text(self):
        """
        Last API Caller - this text is available on Index page
        """
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Last API Caller")
        self.assertContains(response, "form")


class SimilarViewTests(TestCase):
    def test_similar_text(self):
        """
        Similarity - this text is available on Similar page
        """
        client = Client()
        response = client.get(reverse('similar'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Similarity")
        self.assertContains(response, "form")

    def test_similar_input(self):
        """
        Testing text input on Similar page
        """
        random.seed()
        n = random.randint(3,10)
        strname = ''.join(random.choices(string.ascii_letters, k=n))
        client = Client()
        response = client.post(
            "/similar", data={"name": strname}
        )
        print(strname)
        print(response)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertContains(response.content, strname, html=True)
