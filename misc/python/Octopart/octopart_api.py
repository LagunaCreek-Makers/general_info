import os
import sys
import requests
import octopart_schemas as ops

class OctopartService:
    """
    Interact with Octopart API
    https://octopart.com/api/docs/v3/rest-api
    """

    def __init__(self, api_key, include=None, callback=False, pretty_print=False, suppress_status_codes=False):
        self.api_key = api_key
        self.base_url = "http://octopart.com/api/v3/"
        self.callback = callback
        self.pretty_print = pretty_print
        self.suppress_status_codes = suppress_status_codes
        if include is None:
            self.include = ['short_description',
                            'datasheets',
                            'compliance_documents',
                            'descriptions',
                            'imagesets',
                            'specs',
                            'category_uids',
                            'external_links',
                            'reference_designs',
                            'cad_models',
                            ]
        return

    def brandsUid(self, uid):
        """
        This method returns individual brands by primary key. The fetch key for a brand is its 'uid'.
        https://octopart.com/api/docs/v3/rest-api#endpoints-brands-get
        """
        payload = {'apikey': self.api_key}
        r = requests.get(self.base_url + 'brands/' + uid, params=payload)
        return ops.Brand(r.json())

    def brandsSearch(self, q, start=0, limit=10, sortby='score desc', filters=None, facets=None, stats=None):
        """
        This method allows searching across brands by keyword. 
        This is the ideal method to use to go from a brand alias or keyword to a Octopart brand instance
        https://octopart.com/api/docs/v3/rest-api#endpoints-brands-search
        """
        payload = {'apikey': self.api_key,
                   'q': q,
                   'start': start,
                   'limit': limit,
                   'sortby': sortby
                   }

        if filters is not None:
            payload = {**payload, **filters}

        if facets is not None:
            payload = {**payload, **facets}

        if stats is not None:
            payload = {**payload, **facets}

        r = requests.get(self.base_url + "brands/search", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.SearchRespons(r.json())

    def brandsMulti(self, uid_lst):
        """
        This endpoint returns multiple brands simultaneously by primary key. 
        The fetch key for each brand is its 'uid'.
        https://octopart.com/api/docs/v3/rest-api#endpoints-brands-get_multi
        """
        payload = {'apikey': self.api_key,
                   'uid[]': uid_lst
                   }

        r = requests.get(self.base_url + "brands/get_multi", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return r.json()

    def categoriesUid(self, uid):
        """
        This method returns invividual category nodes by primary key. The fetch key for a category is its 'uid'.
        https://octopart.com/api/docs/v3/rest-api#endpoints-categories-get
        """
        payload = {'apikey': self.api_key}
        r = requests.get(self.base_url + 'categories/' + uid, params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.Category(r.json())

    def categoriesSearch(self, q, start=0, limit=10, sortby='score desc', filters=None, facets=None, stats=None):
        """
        This method allows searching across categories by keyword.
        https://octopart.com/api/docs/v3/rest-api#endpoints-categories-search
        """
        payload = {'apikey': self.api_key,
                   'q': q,
                   'start': start,
                   'limit': limit,
                   'sortby': sortby
                   }

        if filters is not None:
            payload = {**payload, **filters}

        if facets is not None:
            payload = {**payload, **facets}

        if stats is not None:
            payload = {**payload, **facets}

        r = requests.get(self.base_url + 'categories/search', params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.SearchResponse(r.json())

    def categoriesMulti(self, uid_lst):
        """
        This endpoint returns multiple categories simultaneously by primary key. 
        The fetch key for each part is its 'uid'. 
        Missing categories will also be missing from the response list.
        https://octopart.com/api/docs/v3/rest-api#endpoints-categories-get_multi
        """
        payload = {'apikey': self.api_key,
                   'uid[]': uid_lst
                   }

        r = requests.get(self.base_url + "categories/get_multi", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return r.json

    def partsUid(self, uid, include=None):
        """
        This method returns individual parts by primary key. The fetch key for a part is its 'uid'.
        https://octopart.com/api/docs/v3/rest-api#endpoints-parts-get
        """
        payload = {'apikey': self.api_key,
                   }

        if include is not None:
            payload['include[]'] = self.include
        else:
            payload['include[]'] = include

        r = requests.get(self.base_url + "parts/" + uid, params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.Part(r.json())

    def partsMatch(self, queries, include=None, exact_only=False):
        """
        Match a list of parts by mpn, sku, brand, seller, mpn_or_sku

        Example Query
        queries = [{'mpn': 'SN74S74N','reference': 'line1'},
                   {'sku': '67K1122','reference': 'line2'},
                   {'mpn_or_sku': 'SN74S74N','reference': 'line3'},
                   {'brand': 'Texas Instruments','mpn': 'SN74S74N','reference': 'line4'}
                  ]

        https://octopart.com/api/docs/v3/rest-api#endpoints-parts-match
        """
        payload = {'apikey': self.api_key,
                   'queries': queries
                   }

        if include is not None:
            payload['include[]'] = self.include
        else:
            payload['include[]'] = include

        r = requests.get(self.base_url + "parts/match", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.PartsMatchResponse(r.json())

    def partsSearch(self, q, include=None, start=0, limit=10, sortby='score desc',
                    filters=None, facets=None, stats=None):
        """
        This method allows searching across parts by keyword or technical specs. 
        This is the ideal method to use to filter parts by manufacturer or 
        to perform a parametric search.

        https://octopart.com/api/docs/v3/rest-api#endpoints-parts-search
        """
        payload = {'apikey': self.api_key,
                   'q': q,
                   'start': start,
                   'limit': limit,
                   'sortby': sortby
                   }

        if include is not None:
            payload['include[]'] = self.include
        else:
            payload['include[]'] = include

        if filters is not None:
            payload = {**payload, **filters}

        if facets is not None:
            payload = {**payload, **facets}

        if stats is not None:
            payload = {**payload, **facets}

        r = requests.get(self.base_url + "parts/search", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.SearchResponse(r.json)

    def partsMulti(self, uid_lst, include=None):
        """
         Returns multiple parts simultaneously by primary key.
         The fetch key for each part is its 'uid'. 
         Missing parts will also be missing from the response list.

         https://octopart.com/api/docs/v3/rest-api#endpoints-parts-get_multi
        """
        payload = {'apikey': self.api_key,
                   'uid[]': uid_lst
                   }

        if include is not None:
            payload['include[]'] = self.include
        else:
            payload['include[]'] = include

        r = requests.get(self.base_url + "parts/get_multi", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return r.json()

    def sellersUid(self, uid):
        """
        This method returns individual sellers by primary key. The fetch key for a seller is its 'uid'

        https://octopart.com/api/docs/v3/rest-api#endpoints-sellers-get
        """
        payload = {'apikey': self.api_key}
        r = requests.get(self.base_url + "sellers/" + uid, params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.Seller(r.json())

    def sellersSearch(self, q, start=0, limit=10, sortby='score desc',
                      filters=None, facets=None, stats=None):
        """
        This method allows searching across sellers by keyword. 
        This is the ideal method to use to go from a seller alias or keyword to a Octopart seller instance

        https://octopart.com/api/docs/v3/rest-api#endpoints-sellers-search
        """
        payload = {'apikey': self.api_key,
                   'q': q,
                   'start': start,
                   'limit': limit,
                   'sortby': sortby
                   }

        if filters is not None:
            payload = {**payload, **filters}

        if facets is not None:
            payload = {**payload, **facets}

        if stats is not None:
            payload = {**payload, **facets}

        r = requests.get(self.base_url + "sellers/search", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return ops.SearchResponse(r.json())

    def sellersMulti(self, uid_lst):
        """
        This endpoint returns multiple sellers simultaneously by primary key. 
        The fetch key for each seller is its 'uid'.

        https://octopart.com/api/docs/v3/rest-api#endpoints-sellers-get_multi
        """
        payload = {'apikey': self.api_key,
                   'uid[]': uid_lst
                   }
        r = requests.get(self.base_url + "sellers/get_multi", params=payload)

        if r.status_code >= 400 and r.status_code < 500:
            return ops.ClientErrorResponse(r.json())
        elif r.status_code >= 500 and r.status_code < 600:
            return ops.ServerErrorResponse(r.json())

        return r.json()


##Schemas
