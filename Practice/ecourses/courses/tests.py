from django.test import TestCase, SimpleTestCase

# Create your tests here.
class SimpleTest(SimpleTestCase):
   def test_courses_page_status(self):
       response = self.client.get('/')
       self.assertEquals(response.status_code, 200)

# # Create your tests here.

