import httplib

from django_webtest import WebTest


class ECDTestCase(WebTest):
    """
    Extends the WebTest class and introduces new methods which make
    testing easier. All the tests which test views must use this
    class instead of the django TestCase directly because WebTest 
    is already an extension of django TestCase and webtest classes.
    """
    def getUrl(self, url_name, args=None):
	    """
	    Returns the URL for the url name.
	    """
	    from django.core.urlresolvers import reverse
	    return reverse(url_name, args)

    def get(self, url, params=None, headers=None, 
	    extra_environ=None, status=None, expect_errors=False):
	    """
	    Performs a GET to the specified url.
	    The method wraps around app.get so that it can be used
	    as self.get.
	    """		
	    response = self.app.get(url, params=params, headers=headers,
				    extra_environ=extra_environ,status=status,
				    expect_errors=expect_errors)
	    return response

    def printResponse(self, response):
	    """
	    Prints the response to the terminal.
	    We need this method because the response is a unicode string and
	    results in exception when printed directly i.e print response.
	    """
	    from django.utils.encoding import smart_str
	    print smart_str(response)

    def assertResponseCode(self, response, status_code):
        """Asserts that the response status is status_code.
        """
        if response.status_code != status_code:
          verbose_codes = [
	      httplib.FOUND,
          ]
          message_codes = [
	      httplib.FORBIDDEN, httplib.BAD_REQUEST, httplib.NOT_FOUND,
          ]
          url_codes = [httplib.NOT_FOUND]

          if response.status_code in verbose_codes:
	    print response

          if response.context and response.status_code in message_codes:
	    try:
	      print response.context['message']
	    except KeyError:
	      pass

          if response.status_code in url_codes:
	    print response.request['PATH_INFO']

        self.assertEqual(status_code, response.status_code)

    def assertResponseOK(self, response):
        """Asserts that the response status is OK.
        """
        self.assertResponseCode(response, httplib.OK)

    def assertResponseRedirect(self, response):
        """Asserts that the response status is FOUND.
        """
        self.assertResponseCode(response, httplib.FOUND)

    def assertResponseForbidden(self, response):
        """Asserts that the response status is FORBIDDEN.
        """
        self.assertResponseCode(response, httplib.FORBIDDEN)

    def assertResponseBadRequest(self, response):
        """Asserts that the response status is BAD_REQUEST.
        """
        self.assertResponseCode(response, httplib.BAD_REQUEST)

    def assertResponseNotFound(self, response):
        """Asserts that the response status is NOT_FOUND.
        """
        self.assertResponseCode(response, httplib.NOT_FOUND)
