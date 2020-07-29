#!/usr/bin/env python3
"""Provide tests for BaseParse"""
import unittest

from . import URL
from hipposcraper import scrapers


class TestBaseParse(unittest.TestCase):
    """Test BaseParse"""

    def setUp(self):
        self.parse = scrapers.BaseParse(URL)
        self.parse.get_json()

    def tearDown(self):
        del self.parse

    def test_base_object(self):
        self.assertIsNotNone(self.parse)
        self.assertIsInstance(self.parse, object)
        self.assertIn("scrapers.BaseParse", str(self.parse))

    def test_json_data(self):
        self.assertIsInstance(self.parse.user_data, dict)

    def test_get_soup(self):
        self.parse.get_soup()
        self.assertIsNotNone(self.parse.soup)
        self.assertIsInstance(self.parse.soup, object)
        self.assertIn("bs4.BeautifulSoup", str(self.parse.soup.__class__))
