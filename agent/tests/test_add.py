import json
import requests
from agent.config import server_url
from datetime import datetime


def add_a_metadata_record(data, set_spec=''):

    data = {
        'record': json.dumps(data),
        'set_spec': set_spec
    }
    response = requests.post(
        url="{}/add".format(server_url),
        params=data
    )
    if response.status_code != 200:
        raise RuntimeError('Request failed with return code: %s' % (
            response.status_code))

    print(response.text)
    return response.text


def gen_unique_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def add_metadata_records(repeats=1):
    cnt = 0
    for rep in range(repeats):
        for data in JSON_DICTS:
            cnt += 1
            print('Add record {}'.format(cnt))
            data['identifier']['identifier'] = gen_unique_id()
            add_a_metadata_record(data, set_spec='test102')


JSON_DICTS = [
    {
        'additionalFields': {
            'coverageBegin': '',
            'coverageEnd': '',
            'onlineResources': [
                {'desc': 'Original Metadata Record',
                 'func': 'metadata',
                 'href': 'http://qa.dirisa.org/Portals/test-mike/testcustmike/metadata/metadata.2018-02-28.9981326861/getOriginalXml',
                 'name': 'Original Metadata Record'}],
            'source_uri': '',
            'status': 'complete'
        },
        'alternateIdentifiers': [{
            'alternateIdentifier': 'http://schema.datacite.org/schema/meta/kernel-3.1/example/datacite-example-full-v3.1.xml',
            'alternateIdentifierType': 'URL'}],
        'bounds': [-68.302, 30.233, -66.302, 32.233000000000004],
        'contributors': [{
            'affiliation': 'California Digital Library',
            'contributorName': 'Starr, Joan',
            'contributorType': 'ProjectLeader',
            'nameIdentifier': '0000-0002-7285-027X',
            'nameIdentifierScheme': 'ORCID',
            'schemeURI': 'http://orcid.org/'}],
        'creators': [{
            'affiliation': 'DataCite',
            'creatorName': 'Miller, Elizabeth',
            'nameIdentifier': '0000-0001-5000-0007',
            'nameIdentifierScheme': 'ORCID',
            'schemeURI': 'http://orcid.org/'}],
        'dates': [{'date': '2014-10-17', 'dateType': 'Updated'}],
        'description': [{
            'description': 'XML example of all DataCite '
                           'Metadata Schema v3.1 properties.',
            'descriptionType': 'Abstract'}],
        'errors': [],
        'formats': ['application/xml'],
        'geoLocations': [{
            'geoLocationBox': '41.090 -71.032  42.893 -68.211',
            'geoLocationPlace': 'Atlantic Ocean',
            'geoLocationPoint': '31.233 -67.302'}],
        'identifier': {
            'identifier': '10.5072/example-full', 'identifierType': 'DOI'},
        'language': 'en-us',
        'publicationYear': '2014',
        'publisher': 'DataCite',
        'relatedIdentifiers': [{
            'relatedIdentifier': 'http://data.datacite.org/application/citeproc+json/10.5072/example-full',
            'relatedIdentifierType': 'URL',
            'relatedMetadataScheme': 'citeproc+json',
            'relatedType': 'IsMetadataFor',
            'relationType': 'HasMetadata',
            'schemeType': '',
            'schemeURI': 'https://github.com/citation-style-language/schema/raw/master/csl-data.json'},
            {
            'relatedIdentifier': 'arXiv:0706.0001',
            'relatedIdentifierType': 'arXiv',
            'relatedMetadataScheme': '',
            'relatedType': 'IsMetadataFor',
            'relationType': 'IsReviewedBy',
            'schemeType': '',
            'schemeURI': ''}],
        'resourceType': 'XML',
        'resourceTypeGeneral': 'Software',
        'rights': [{
            'rights': 'CC0 1.0 Universal',
            'rightsURI': 'http://creativecommons.org/publicdomain/zero/1.0/'}],
        'schemaSpecific': {},
        'sizes': ['3KB', '25ml'],
        'subjects': [{
            'schemeURI': 'http://dewey.info/',
            'subject': '000 computer science',
            'subjectScheme': 'dewey'}],
        'subtitle': '',
        'title': 'Full DataCite XML Example',
        'titles': [
            {'title': 'Full DataCite XML Example', 'titleType': ''},
            {'title': 'Demonstration of DataCite Properties.',
             'titleType': 'Subtitle'}],
        'version': '3.1',
        'xsiSchema': 'http://datacite.org/schema/kernel-3 '
                     'http://schema.datacite.org/meta/kernel-3/metadata.xsd'
    },
    {
        "subtitle": "",
        "contributors": [],
        "userId": "",
        "xsiSchema": "http://datacite.org/schema/kernel-3",
        "owner": "",
        "subjects": [
            {
                "subjectScheme": "",
                "schemeURI": "",
                "subject": "SOC"
            }
        ],
        "additionalFields": {
            "onlineResources": [
            ],
            "coverageBegin": "",
            "coverageEnd": ""
        },
        "geoLocations": [
            {
                "geoLocationBox": "-34.83416999999997 16.451910000000055 -22.12502999999998 32.944980000000044"
            }
        ],
        "userVersion": "",
        "description": [
            {
                "descriptionType": "",
                "description": "Soil Organic Carbon (SOC) represents all the organic carbon in the soil to a depth of 1m. SOC is derived from the data provided by the Africa Soil Information System (AfSIS). In this case the organic carbon of the top 300mm of the natural soil was NOT reduced by land cover factors.\n\nUnits: average gC/m2 within 1km x 1km pixel"
            }
        ],
        "publicationYear": "2017",
        "relatedIdentifiers": [],
        "creators": [
            {
                "creatorName": "Prof J Soap",
                "affiliation": "UCT"
            },
            {
                "creatorName": "Prof MJ Mets",
                "affiliation": "UWC"
            }
        ],
        "publisher": "UCT",
        "dates": [
            {
                "date": "2017-01-22",
                "dateType": "Accepted"
            },
            {
                "date": "2017-02-03",
                "dateType": "Issued"
            }
        ],
        "language": "eng",
        "rights": [
            {
                "rights": "",
                "rightsURI": ""
            }
        ],
        "resourceType": "on",
        "sizes": [],
        "resourceTypeGeneral": "",
        "bounds": [],
        "alternateIdentifiers": [],
        "titles": [
            {
                "title": "Soil Organic Carbon Unperturbed (gC/sq.m)"
            },
            {
                "titleType": "AlternativeTitle",
                "title": "Carbon Unperturbed (gC/sq.m)"
            }
        ],
        "identifier": {
            "identifier": "12345/ABC",
            "identifierType": "DOI"
        }
    },
    {
        "subtitle": "",
        "contributors": [],
        "userId": "",
        "xsiSchema": "http://datacite.org/schema/kernel-3",
        "owner": "",
        "subjects": [
            {
                "subjectScheme": "Dewey",
                "schemeURI": "http://dewey.info/",
                "subject": "SOC"
            },
            {
                "subjectScheme": "",
                "schemeURI": "",
                "subject": "COS"
            }
        ],
        "additionalFields": {
            "onlineResources": [
            ],
            "coverageBegin": "",
            "coverageEnd": ""
        },
        "geoLocations": [
            {
                "geoLocationBox": "-34.83416999999997 16.451910000000055 -22.12502999999998 32.944980000000044"
            }
        ],
        "userVersion": "",
        "description": [
            {
                "descriptionType": "",
                "description": "Soil Organic Carbon (SOC) represents all the organic carbon in the soil to a depth of 1m. SOC is derived from the data provided by the Africa Soil Information System (AfSIS). In this case the organic carbon of the top 300mm of the natural soil was NOT reduced by land cover factors.\n\nUnits: average gC/m2 within 1km x 1km pixel"
            }
        ],
        "publicationYear": "2017",
        "relatedIdentifiers": [],
        "creators": [
            {
                "creatorName": "Prof J Soap",
                "affiliation": "UCT"
            }
        ],
        "publisher": "UCT",
        "dates": [
            {
                "date": "2017-01-22",
                "dateType": "Accepted"
            },
            {
                "date": "2017-02-03",
                "dateType": "Issued"
            }
        ],
        "language": "eng",
        "rights": [
            {
                "rights": "",
                "rightsURI": ""
            }
        ],
        "resourceType": "on",
        "sizes": [],
        "resourceTypeGeneral": "",
        "bounds": [],
        "alternateIdentifiers": [],
        "titles": [
            {
                "titleType": "",
                "title": "Soil Organic Carbon Unperturbed (gC/sq.m)"
            }
        ],
        "identifier": {
            "identifier": "12345/XYZ",
            "identifierType": "DOI"
        }
    },
]

if __name__ == "__main__":
    add_metadata_records(10)
