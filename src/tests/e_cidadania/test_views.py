from tests.utils import ECDTestCase

class TestIndexView(ECDTestCase):
	
	def testIndexPage(self):
		url = self.getUrl('site-index')		
		response = self.get(url)
		self.assertResponseOK(response)
		#check the templates used
		self.assertTemplateUsed(response, 'base.html')
		self.assertTemplateUsed(response, 'site_index.html')
		
		

	
