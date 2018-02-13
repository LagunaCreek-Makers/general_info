import requests
import os


class Asset:
    """
    Asset Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-asset
    """

    def __init__(self, data):
        self.url = data['url']
        self.mimetype = data['mimetype']
        self.metadata = data['metadata']
        self.filename = os.path.basename(self.url)
        self.data = None
        return

    def __str__(self):
        string = "Asset:\n"
        string += "\tURL: {0}\n".format(self.url)
        string += "\tMimetype: {0}\n".format(self.mimetype)
        string += "\tMetadata: {0}\n".format(self.metadata)
        return string

    def download(self):
        if self.url is None:
            return

        r = requests.get(self.url)
        if r.status_code == 200:
            self.data = r.content

        return

    def save_file(self):
        if self.data is None:
            return

        fh = open(self.filename, 'wb')
        fh.write(self.data)
        fh.close()
        return


class Attribution:
    """
    Attribution Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-attribution
    """

    def __init__(self, data):
        if 'sources' not in data or data['sources'] is None:
            self.sources = None
        else:
            self.sources = [Source(x) for x in data['sources']]
        self.first_acquired = data['first_acquired']
        return

    def __str__(self):
        string = "Attribution:\n"

        if self.sources is not None:
            for x in self.sources:
                string += str(x)

        string += "\tFirst Acquired: {0}\n".format(self.first_acquired)
        return string


class Brand:
    """
    Brand Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-brand
    """

    def __init__(self, data):
        self.uid = data['uid']
        self.name = data['name']
        self.homepage_url = data['homepage_url']
        return

    def __str__(self):
        string = ""
        string += "Brand:\n";
        string += "\tUID: {0}\n".format(self.uid)
        string += "\tName: {0}\n".format(self.name)
        string += "\tURL: {0}\n".format(self.homepage_url)
        return string


class BrokerListing:
    """
    BrokerListing Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-brokerlisting
    """

    def __init__(self, data):
        self.seller = data['seller']
        self.listing_url = data['listing_url']
        self.octopart_rfq_url = data['octopart_rfq_url']
        return


class CADModel(Asset):
    """
    CADModel Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-cadmodel
    """

    def __init__(self, data):
        Asset.__init__(self, data)
        self.attribution = None if 'attribution' not in data else Attribution(data['attribution'])
        return

    def __str__(self):
        string = "CAD Model:\n"
        string += "\tURL: {0}\n".format(self.url)
        string += "\tMimetype: {0}\n".format(self.mimetype)
        string += "\tMetadata: {0}\n".format(self.metadata)
        string += "\tAttribution: {0}\n".format(self.attribution)
        return string


class Category:
    """
    Category schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-category
    """

    def __init__(self, data):
        self.uid = data['uid']
        self.name = data['name']
        self.parent_uid = data['parent_uid']
        self.children_uids = data['children_uids']
        self.ancestor_uids = data['ancestor_uids']
        self.ancestor_names = data['ancestor_names']
        self.num_parts = data['num_parts']
        self.imagesets = None if 'imagesets' not in data else [ImageSet(x) for x in data['imagesets']]
        return


class ComplianceDocument(Asset):
    """
    Compliance Document Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-compliancedocument
    """
    def __init__(self, data):
        Asset.__init__(self.data)
        self.subtypes = data['subtypes']
        self.attribution = None if 'attribution' not in data else Attribution(data['attribution'])
        return

    def __str__(self):
        string = "Compliance Document:\n"
        string += "\tURL: {0}\n".format(self.url)
        string += "\tMimetype: {0}\n".format(self.mimetype)
        string += "\tMetadata: {0}\n".format(self.metadata)
        string += "\tSubtypes: {0}\n".format(self.subtypes)
        string += "\tAttribution: {0}\n".format(self.attribution)
        return string


class Datasheet(Asset):
    """
    Datasheet Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-datasheet
    """
    def __init__(self, data):
        Asset.__init__(self, data)
        self.attribution = None if 'attribution' not in data else Attribution(data['attribution'])
        return

    def __str__(self):
        string = "Datasheet:\n"
        string += "\tURL: {0}\n".format(self.url)
        string += "\tMimetype: {0}\n".format(self.mimetype)
        string += "\tMetadata: {0}\n".format(self.metadata)
        string += str(self.attribution)
        return string


class Description:
    """
    Description Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-description
    """
    def __init__(self, data):
        self.value = data['value']
        self.attribution = None if 'attribution' not in data else Attribution(data['attribution'])
        return

    def __str__(self):
        string = "Description:\n"
        string += "\tValue: {0}\n".format(self.value)
        string += "\tAttribution: {0}\n".format(self.attribution)
        return string


class ExternalLinks:
    """
    External Links Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-externallinks
    """
    def __init__(self, data):
        self.product_url = data['product_url']
        self.freesample_url = data['freesample_url']
        self.evalkit_url = data['evalkit_url']
        return

    def __str__(self):
        string = "External Links:\n"
        string += "\tProduct URL: {0}\n".format(self.product_url)
        string += "\tFree Sample URL: {0}\n".format(self.freesample_url)
        string += "\tEval Kit URL: {0}\n".format(self.evalkit_url)
        return string


class ImageSet:
    """
    Image Set  Schema
    https://octopart.com/api/docs/v3/rest-api#object-schemas-imageset
    """
    def __init__(self, data):
        if 'swatch_image' not in data or data['swatch_image'] is None:
            self.swatch_image = None
        else:
            self.swatch_image = Asset(data['swatch_image'])

        if 'small_image' not in data or data['small_image'] is None:
            self.small_image = None
        else:
            self.small_image = Asset(data['small_image'])

        if 'medium_image' not in data or data['medium_image'] is None:
            self.medium_image = None
        else:
            self.medium_image = Asset(data['medium_image'])

        if 'large_image' not in data or data['large_image'] is None:
            self.large_image = None
        else:
            self.large_image = Asset(data['large_image'])

        if 'attribution' not in data or data['attribution'] is None:
            self.attribution = None
        else:
            self.attribution = Attribution(data['attribution'])

        self.credit_string = None if 'credit_string' not in data else data['credit_string']
        self.credit_url = None if 'credit_url' not in data else data['credit_url']
        return

    def __str__(self):
        string = "ImageSet:\n"
        string += "\tSwatch Image: {0}\n".format(self.swatch_image)
        string += "\tSmall Image: {0}\n".format(self.small_image)
        string += "\tMedium Image: {0}\n".format(self.medium_image)
        string += "\tLarge Image: {0}\n".format(self.large_image)
        string += "\tAttribution: {0}\n".format(self.attribution)
        string += "\tCredit String: {0}\n".format(self.credit_string)
        string += "\tCredit URL: {0}\n".format(self.credit_url)
        return string


class Manufacturer:
    def __init__(self, data):
        self.uid = data['uid']
        self.name = data['name']
        self.homepage_url = data['homepage_url']
        return

    def __str__(self):
        string = "Manufactuer:\n"
        string += "\tUID: {0}\n".format(self.uid)
        string += "\tName: {0}\n".format(self.name)
        string += "\tURL: {0}\n".format(self.homepage_url)
        return string


class Part:
    def __init__(self, data):
        self.uid = None if 'uid' not in data else data['uid']
        self.mpn = None if 'mpn' not in data else data['mpn']
        self.manufacturer = None if 'manufacturer' not in data else Manufacturer(data['manufacturer'])
        self.brand = None if 'brand' not in data else Brand(data['brand'])
        self.octopart_url = None if 'octopart_url' not in data else data['octopart_url']
        self.external_links = None if 'external_links' not in data else ExternalLinks(data['external_links'])
        self.offers = None if 'offers' not in data else [PartOffer(x) for x in data['offers']]
        self.broker_listings = None if 'broker_listing' not in data else BrokerListing(data['broker_listings'])
        self.short_description = None if 'short_description' not in data else data['short_description']
        self.snippet = None if 'snippet' not in data else data['snippet']
        self.redirected_uids = None if 'redirected_uids' not in data else data['redirected_uids']
        self.descriptions = None if 'description' not in data else [Description(x) for x in data['description']]

        if 'imagesets' not in data or data['imagesets'] is None:
            self.imagesets = None
        else:
            self.imagesets = [ImageSet(x) for x in data['imagesets']]

        self.datasheets = None if 'datasheets' not in data else [Datasheet(x) for x in data['datasheets']]
        self.compliance_documents = None if 'compliance_documents' not in data else [ComplianceDocument(x) for x in
                                                                                     data['compliance_documents']]
        self.reference_designs = None if 'reference_designs' not in data else [ReferenceDesign(x) for x in
                                                                               data['reference_designs']]
        self.cad_models = None if 'cad_models' not in data else [CADModel(x) for x in data['cad_models']]
        self.specs = None if 'specs' not in data else data['specs']
        self.category_uids = None if 'category_uids' not in data else data['category_uids']
        return

    def __str__(self):
        string = ""
        string += "UID: {0}\n".format(self.uid)
        string += "MPN: {0}\n".format(self.mpn)
        string += str(self.manufacturer)
        string += str(self.brand)
        string += "OctoPart URL: {0}\n".format(self.octopart_url)
        return string


class PartOffer:
    def __init__(self, data):
        self.sku = data['sku']
        self.seller = None if 'seller' not in data else Seller(data['seller'])
        self.eligible_region = data['eligible_region']
        self.product_url = data['product_url']
        self.octopart_rfq_url = data['octopart_rfq_url']
        self.prices = data['prices']
        self.in_stock_quantity = data['in_stock_quantity']
        self.on_order_quantity = data['on_order_quantity']
        self.factory_lead_days = data['factory_lead_days']
        self.factory_order_multiple = data['factory_order_multiple']
        self.order_multiple = data['order_multiple']
        self.moq = data['moq']
        self.multipack_quantity = data['multipack_quantity']
        self.packaging = data['packaging']
        self.is_authorized = data['is_authorized']
        self.last_updated = data['last_updated']
        return

    def __str__(self):
        string = "Part Offer:\n"
        string += str(self.seller) + "\n"
        string += "\tEligible Region: {0}\n".format(self.eligible_region)
        string += "\tProduct URL: {0}\n".format(self.product_url)
        string += "\tOctoPart RFQ URL: {0}\n".format(self.octopart_rfq_url)
        string += "\tPrices: {0}\n".format(self.prices)
        string += "\tIn Stock Quantity: {0}\n".format(self.in_stock_quantity)
        string += "\tOn Order Quantity: {0}\n".format(self.on_order_quantity)
        string += "\tFactor_Lead Days: {0}\n".format(self.factory_lead_days)
        string += "\tFactory Order Multiple: {0}\n".format(self.order_multiple)
        string += "\tMin. Order Quantity: {0}\n".format(self.moq)
        string += "\tMultipack Quantity: {0}\n".format(self.multipack_quantity)
        string += "\tPackaging: {0}\n".format(self.packaging)
        string += "\tIs Authorized: {0}\n".format(self.is_authorized)
        string += "\tLast Updated: {0}\n".format(self.last_updated)
        return string


class SpecValue:
    def __init__(self, data):
        self.value = data['value']
        self.min_value = data['min_value']
        self.max_value = data['max_value']
        self.metadata = None if 'metadata' not in data else SpecMetadata(data['metadata'])
        self.attribution = None if 'attribution' not in data else Attribution(data['attribution'])
        return

    def __str__(self):
        string = "Spec Value:\n"
        string += "\tValue: {0}\n".format(self.value)
        string += "\tMin Value: {0}\n".format(self.min_value)
        string += "\tMax Value: {0}\n".format(self.max_value)
        string += str(self.metadata)
        string += str(self.attribution)
        return string


class ReferenceDesign(Asset):
    def __init__(self, data):
        Asset.__init__(self, data)
        self.title = data['title']
        self.description = data['description']
        self.attribution = None if 'attribution' not in data else Attribution(data['attribution'])
        return

    def __str__(self):
        string = "Reference Design:\n"
        string += "\tURL: {0}\n".format(self.url)
        string += "\tMimetype: {0}\n".format(self.mimetype)
        string += "\tMetadata: {0}\n".format(self.metadata)
        string += "\tTitle: {0}\n".format(self.title)
        string += "\tDescription: {0}\n".format(self.description)
        string += str(self.attribution)
        return string


class Seller:
    def __init__(self, data):
        self.uid = data['uid']
        self.name = data['name']
        self.homepage_url = data['homepage_url']
        self.display_flag = data['display_flag']
        self.has_ecommerce = data['has_ecommerce']
        return

    def __str__(self):
        string = "Seller:\n"
        string += "\tUID: {0}\n".format(self.uid)
        string += "\tName: {0}\n".format(self.name)
        string += "\tHomepage URL: {0}\n".format(self.homepage_url)
        string += "\tDisplay Flag: {0}\n".format(self.display_flag)
        string += "\tHas ECommerce: {0}\n".format(self.has_ecommerce)
        return string


class Source:
    def __init__(self, data):
        self.uid = data['uid']
        self.name = data['name']
        return

    def __str__(self):
        string = "Source:\n"
        string += "\tUID: {0}\n".format(self.uid)
        string += "\tName: {0}\n".format(self.name)
        return string


class SpecMetadata:
    def __init__(self, data):
        self.key = data['key']
        self.name = data['name']
        self.datatype = data['datatype']
        self.unit = UnitOfMeasurment(data['unit'])
        return

    def __str__(self):
        string = "Spec Metadata:\n"
        string += "\tKey: {0}\n".format(self.key)
        string += "\tName: {0}\n".format(self.name)
        string += "\tDatatype: {0}\n".format(self.datatype)
        string += str(self.unit)
        return string


class UnitOfMeasurment:
    def __init__(self, um):
        self.name = um['name']
        self.symbol = um['symbol']
        return

    def __str__(self):
        string = "Unit of Measurment:\n"
        string += "\tName: {0}\n".format(self.name)
        string += "\tSymbol: {0}\n".format(self.symbol)
        return string


##Response Schemas

class PartsMatchRequest:
    def __init__(self, data):
        self.queries = data['queries']
        self.exact_only = data['exact_only']
        return


class PartsMatchQuery:
    def __init__(self, data):
        self.q = data['q']
        self.mpn = data['mpn']
        self.brand = data['brand']
        self.sku = data['sku']
        self.seller = data['seller']
        self.mpn_or_sku = data['mpn_or_sku']
        self.start = data['start']
        self.limit = data['limit']
        self.reference = data['reference']
        return


class PartsMatchResponse:
    def __init__(self, data):
        self.request = data['request']
        self.results = data['results']
        self.msec = data['msec']
        return


class PartsMatchResult:
    def __init__(self, data):
        self.items = data['items']
        self.hits = data['hits']
        self.reference = data['reference']
        self.error = data['error']
        return


class SearchRequest:
    def __init__(self, data):
        self.q = data['q']
        self.start = data['start']
        self.limit = data['limit']
        self.sortby = data['sortby']
        self.filter = data['filter']
        self.facet = data['facet']
        self.stats = data['stats']
        return


class SearchResponse:
    def __init__(self, data):
        self.request = SearchRequest(data['request'])
        self.results = [SearchResult(x) for x in data['results']]
        self.hits = data['hits']
        self.msec = data['msec']
        self.facet_results = data['facet_results']
        self.stats_results = data['stats_results']
        self.spec_metadata = data['spec_metadata']
        self.user_country = data['user_country']
        self.user_currency = data['user_currency']
        return


class SearchResult:
    def __init__(self, data):
        self.item = Part(data['item'])
        return


class SearchFacetResult:
    def __init__(self, data):
        self.facets = data['facets']
        self.missing = data['missing']
        self.spec_drilldown_rank = data['spec_drilldown_rank']
        return


class SearchStatsResult:
    def __init__(self, data):
        self.min = data['min']
        self.max = data['max']
        self.mean = data['mean']
        self.stddev = data['stddev']
        self.count = data['count']
        self.missing = data['missing']
        self.spec_drilldown_rank = data['spec_drilldown_rank']
        return


class ClientErrorResponse(Exception):
    def __init__(self, data):
        self.message = data['message']
        return


class ServerErrorResponse(Exception):
    def __init__(self, data):
        self.message = data['message']
        return