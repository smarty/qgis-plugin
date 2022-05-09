# import smartystreets_python_sdk as smarty
from . import *
from .us_street import Client as USStreetClient
from .us_zipcode import Client as USZIPClient
from .us_extract import Client as USExtractClient
from .us_autocomplete import Client as USAutocompleteClient
from .us_autocomplete_pro import Client as USAutocompleteProClient
from .us_reverse_geo import Client as USReverseGeoClient
from .international_street import Client as InternationalStreetClient
from .international_autocomplete import Client as InternationalAutocompleteClient


class ClientBuilder:
    def __init__(self, signer):
        """
        The ClientBuilder class helps you build a client object for one of the supported SmartyStreets APIs.
        You can use ClientBuilder's methods to customize settings like maximum retries or timeout duration.
        These methods are chainable, so you can usually get set up with one line of code.
        """
        self.signer = signer
        self.serializer = NativeSerializer() # TODO: 
        self.http_sender = None
        self.max_retries = 5
        self.max_timeout = 10000
        self.url_prefix = None
        self.proxy = None
        self.debug = None
        self.header = None
        self.licenses = []
        self.INTERNATIONAL_STREET_API_URL = "https://international-street.api.smartystreets.com/verify"
        self.INTERNATIONAL_AUTOCOMPLETE_API_URL = "https://international-autocomplete.api.smartystreets.com/lookup"
        self.US_AUTOCOMPLETE_API_URL = "https://us-autocomplete.api.smartystreets.com/suggest"
        self.US_AUTOCOMPLETE_PRO_API_URL = "https://us-autocomplete-pro.api.smartystreets.com/lookup"
        self.US_EXTRACT_API_URL = "https://us-extract.api.smartystreets.com"
        self.US_STREET_API_URL = "https://us-street.api.smartystreets.com/street-address"
        self.US_ZIP_CODE_API_URL = "https://us-zipcode.api.smartystreets.com/lookup"
        self.US_REVERSE_GEO_API_URL =  "https://us-reverse-geo.api.smartystreets.com/lookup"

    def retry_at_most(self, max_retries):
        """
        Sets the maximum number of times to retry sending the request to the API. (Default is 5)

        Returns self to accommodate method chaining.
        """
        self.max_retries = max_retries
        return self

    def with_max_timeout(self, max_timeout):
        """
        The maximum time (in milliseconds) to wait for a connection, and also to wait for
        the response to be read. (Default is 10000)

        Returns self to accommodate method chaining.
        """
        self.max_timeout = max_timeout
        return self

    def with_sender(self, sender):
        """
        Default is a series of nested senders. (See build_sender()

        Returns self to accommodate method chaining.
        """
        self.http_sender = sender
        return self

    def with_serializer(self, serializer):
        """
        Changes the Serializer from the default.

        Returns self to accommodate method chaining.
        """
        self.serializer = serializer
        return self

    def with_base_url(self, base_url):
        """
        This may be useful when using a local installation of the SmartyStreets APIs.
        base_url is a string that defaults to the URL for the API corresponding to the Client object being built.

        Returns self to accommodate method chaining.
        """
        self.url_prefix = base_url
        return self

    def with_proxy(self, host, username=None, password=None):
        """
        Assigns a proxy through which to send all Lookups.
        :param host: The proxy host including port, but not scheme. (example: localhost:8080)
        :param username: Username to authenticate with the proxy server
        :param password: Password to authenticate with the proxy server
        :return: Returns self to accommodate method chaining.
        """
        self.proxy = Proxy(host, username, password) # TODO
        return self

    def with_custom_header(self, custom_header):
        """
        Create custom headers when necessary.
        :param custom_header: Input your custom headers
        :return: Returns self to accommodate method chaining
        """
        self.header = custom_header
        return self

    def with_debug(self):
        """
        Enables debug mode, which will print information about the HTTP request and response to the console.

        Returns self to accommodate method chaining.
        """
        self.debug = True
        return self

    def with_licenses(self, licenses):
        """
        Allows the caller to specify the subscription license (aka "track") they wish to use.
        :param licenses: Input licenses
        :return: Returns self to accommodate method chaining
        """
        self.licenses = licenses
        return self

    def build_international_street_api_client(self):
        self.ensure_url_prefix_not_null(self.INTERNATIONAL_STREET_API_URL)
        return InternationalStreetClient(self.build_sender(), self.serializer)

    def build_international_autocomplete_api_client(self):
        self.ensure_url_prefix_not_null(self.INTERNATIONAL_AUTOCOMPLETE_API_URL)
        return InternationalAutocompleteClient(self.build_sender(), self.serializer)

    def build_us_autocomplete_api_client(self):
        self.ensure_url_prefix_not_null(self.US_AUTOCOMPLETE_API_URL)
        return USAutocompleteClient(self.build_sender(), self.serializer)

    def build_us_autocomplete_pro_api_client(self):
        self.ensure_url_prefix_not_null(self.US_AUTOCOMPLETE_PRO_API_URL)
        return USAutocompleteProClient(self.build_sender(), self.serializer)

    def build_us_extract_api_client(self):
        self.ensure_url_prefix_not_null(self.US_EXTRACT_API_URL)
        return USExtractClient(self.build_sender(), self.serializer)

    def build_us_street_api_client(self):
        self.ensure_url_prefix_not_null(self.US_STREET_API_URL)
        return USStreetClient(self.build_sender(), self.serializer)

    def build_us_zipcode_api_client(self):
        self.ensure_url_prefix_not_null(self.US_ZIP_CODE_API_URL)
        return USZIPClient(self.build_sender(), self.serializer)

    def build_us_reverse_geo_api_client(self):
        self.ensure_url_prefix_not_null(self.US_REVERSE_GEO_API_URL)
        return USReverseGeoClient(self.build_sender(), self.serializer)

    def build_sender(self):
        if self.http_sender is not None:
            return self.http_sender

        sender = RequestsSender(self.max_timeout, self.proxy) # TODO
        sender.debug = self.debug

        sender = StatusCodeSender(sender) # TODO

        if self.header is not None:
            sender = CustomHeaderSender(self.header, sender) # TODO

        if self.signer is not None:
            sender = SigningSender(self.signer, sender) # TODO

        if self.max_retries > 0:
            sender = RetrySender(self.max_retries, sender) # TODO

        sender = URLPrefixSender(self.url_prefix, sender) # TODO

        sender = LicenseSender(self.licenses, sender) # TODO

        return sender

    def ensure_url_prefix_not_null(self, url):
        if self.url_prefix is None:
            self.url_prefix = url
