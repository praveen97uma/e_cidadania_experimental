import unittest
import e_cidadania

from django_webtest import WebTest
from django.core.urlresolvers import reverse

class TestIndexView(WebTest):
	
	def testIndexPage(self):
		url = reverse('site-index')		
		response = self.app.get(url)
		self.assertEqual(response.context, '')
