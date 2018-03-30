#!/usr/bin/env python

import cherrypy
import json
from agent.config import metadata_index_name
from agent.config import server_port
from agent.config import token_index_name
from agent.oaipmh import process_request
from agent.persist import Metadata
from agent.search import MetadataSearch
from agent.search import search_all
from agent.search import search
from agent.utils import get_request_host
from agent.utils import json_handler
from agent.utils import format_json_dates
from elasticsearch_dsl import Search
import xml.etree.ElementTree as ET


class AgentAPI(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add(self, **kwargs):
        cherrypy.log(str(kwargs))
        output = {'success': False}
        record = kwargs.get('record')
        if record is None:
            msg = "Error: 'record' argument is required"
            output['msg'] = msg
            return output
        try:
            record = json.loads(record)
        except Exception as e:
            msg = "Error: json format {}".format(e)
            output['msg'] = msg
            return output

        set_spec = kwargs.get('set_spec', '')

        try:
            identifier = record['identifier']['identifier']
        except:
            msg = "identifier is required"
            output['msg'] = msg
            return output
        if identifier == '':
            msg = "identifier is required"
            output['msg'] = msg
            return output

        # Hack to fix rights
        rights = record.get('rights')
        if rights == '':
            record['rights'] = []

        # Hack to fix dates
        dates = record.get('dates')
        lst = []
        for date_dict in dates:
            if date_dict.get('date', '') != '':
                new = dict()
                if date_dict.get('dateType'):
                    new['dateType'] = date_dict.get('dateType')
                the_date = date_dict['date']
                if '/' in the_date:
                    the_dates = the_date.split('/')
                    new['date'] = {'gte': the_dates[0], 'lte': the_dates[1]}
                else:
                    new['date'] = {'gte': the_date, 'lte': the_date}
                lst.append(new)
        # print(lst)
        record['dates'] = lst

        # Replace record if it already exists ie. delete first
        srch = Metadata.search()
        srch = srch.filter('match', record_id=identifier)
        srch.execute()
        if srch.count() == 1:
            srch.delete()

        # Metadata.init()
        try:
            md = Metadata(
                record=record, record_id=identifier, set_spec=set_spec)
        except Exception as e:
            msg = "Error: {}: {}".format('Creation failed', e)
            output['msg'] = msg
            return output

        try:
            md.save()
        except Exception as e:
            msg = "Error: {}: {} - {}".format(
                'Save failed', identifier, e)
            output['msg'] = msg
            return output

        output['success'] = True
        return output

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete_all(self):
        output = {'success': False}
        cherrypy.log('delete_all')
        s = Search(index=metadata_index_name)
        s.delete()
        s = Search(index=token_index_name)
        s.delete()
        output['success'] = True
        return output

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete(self, **kwargs):
        output = {'success': False}
        cherrypy.log('delete_all')
        record_id = kwargs.get('record_id')
        if record_id is None:
            msg = "Error: 'record_id' argument is required"
            output['msg'] = msg
            return output

        force = kwargs.get('force', 'false').lower() == 'true'

        srch = Metadata.search()
        srch = srch.filter('match', record_id=record_id)
        srch.execute()
        if srch.count() == 0:
            msg = "Error: record {} not found".format(record_id)
            output['msg'] = msg
            return output
        if srch.count() > 1 and not force:
            msg = "Error: duplicate records found with id {}. ".format(
                record_id)
            msg.append('Use force=true argument to delete all duplicates')
            output['msg'] = msg
            return output
        srch.delete()
        output['success'] = True
        output['msg'] = 'Record {} deleted'.format(record_id)
        return output

    @cherrypy.expose
    @cherrypy.tools.json_out(handler=json_handler)
    def search(self, **kwargs):
        output = {'success': False}
        if kwargs:
            new_kwargs = {}
            for k in kwargs:
                new_k = 'record.{}'.format(k)
                new_kwargs[new_k] = kwargs[k]
            response = search(**new_kwargs)
        else:
            response = search_all()

        if not response['success']:
            output['error'] = response['error']
            return output

        items = format_json_dates(response['result'])

        output['success'] = True
        output['result_length'] = len(items)
        output['results'] = items

        return output

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def faceted_search(self, **kwargs):
        output = {'success': False}
        subjects = kwargs.get('subjects', '')
        try:
            # fs = MetadataSearch(subjects, filters={'record.publicationYear': '2014'})
            fs = MetadataSearch(subjects)
            aa = fs.build_search()
            print(aa.to_dict())
            response = fs.execute()
        except Exception as e:
            msg = 'Error: faceted_search failed with {}'.format(e)
            output['msg'] = msg
            return output
        print(response.hits.total, 'hits total')

        facet_response = response.facets.to_dict()

        aggs = response.aggregations.to_dict()
        print(aggs)

        lines = []
        for facet_name in facet_response:
            facet_result = dict()
            for (value, count, selected) in facet_response[facet_name]:
                facet_result[value] = count
            lines.append({facet_name: facet_result})

        output['success'] = True
        output['result_length'] = len(lines)
        output['results'] = lines

        return output

    @cherrypy.expose
    def oaipmh(self, **kwargs):
        request = cherrypy.request
        cherrypy.log('oaipmh')

        response = process_request(
            request, request.query_string, **kwargs)

        # prepare return on XML
        cherrypy.response.headers['Content-Type'] = \
            'application/xml;charset=UTF-8'
        cherrypy.response.headers['Content-Length'] = len(response)
        return response

    @cherrypy.expose
    def default(self, *args, **kwargs):
        request = cherrypy.request
        host = get_request_host(request)
        url = "http://{}".format(host)
        cherrypy.log('root')

        root = ET.Element("html")
        body = ET.SubElement(root, "body")
        child = ET.SubElement(body, "h2")
        child.text = 'Welcome to the SAEON Metadata Search Agent'
        api = ET.SubElement(body, "h3")
        api.text = 'JSON API'
        ET.SubElement(api, "br")
        search = ET.SubElement(api, "a", {
            'href': '{}/search'.format(url)
        })
        search.text = 'Search'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "Return selected records in a 'SAEON JSON DataCite' format"
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = 'Arguments:'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* field/value pairs: provide any number of fields with the search value'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* "fields": limit output to only fields given in this comma separated list'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* "from": from date'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* "to": to date'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* "sort": sort results by the given field in ascending order'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* "start": position of the first record returned, default is 1'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* "size": number of records - default is 100'

        # Add
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "br")
        add = ET.SubElement(api, "a", {
            'href': '{}/add'.format(url)
        })
        add.text = 'Add'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "Add a record to a collection"
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = 'Arguments:'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "* record: json dict in 'SAEON JSON DataCite' format"
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "* spec_set: optional name of collection"

        # Delete
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "br")
        add = ET.SubElement(api, "a", {
            'href': '{}/delete'.format(url)
        })
        add.text = 'Delete'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "Delete a given record"
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = 'Arguments:'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "* record_id: record identifier to be deleted"
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "* force: optional to force deletion of duplicated records"

        # Faceted Search
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "br")
        search = ET.SubElement(api, "a", {
            'href': '{}/faceted_search'.format(url)
        })
        search.text = 'Faceted Search'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "Return all known facets"

        # OAI-PMH
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "br")
        oai = ET.SubElement(body, "h3")
        oai.text = 'OAI-Protocal for Metadata Harverting'
        child = ET.SubElement(oai, "br")
        verbs = ET.SubElement(oai, "span")
        verbs.text = 'Verbs'
        child = ET.SubElement(verbs, "br")

        child = ET.SubElement(verbs, "a", {
            'href': '{}/oaipmh?verb=Identity'.format(url)
        })
        child.text = 'Identity'
        child = ET.SubElement(verbs, "br")

        child = ET.SubElement(verbs, "a", {
            'href': '{}/oaipmh?verb=ListMetadataFormats'.format(url)
        })
        child.text = 'ListMetadataFormats'
        child = ET.SubElement(verbs, "br")

        child = ET.SubElement(verbs, "a", {
            'href': '{}/oaipmh?verb=ListIdentifiers'.format(url)
        })
        child.text = 'ListIdentifiers'
        child = ET.SubElement(verbs, "br")

        child = ET.SubElement(verbs, "a", {
            'href': '{}/oaipmh?verb=ListRecords'.format(url)
        })
        child.text = 'ListRecords'
        child = ET.SubElement(verbs, "br")

        child = ET.SubElement(verbs, "a", {
            'href': '{}/oaipmh?verb=GetRecord'.format(url)
        })
        child.text = 'GetRecord'
        child = ET.SubElement(verbs, "br")

        return ET.tostring(root)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': server_port})
    cherrypy.quickstart(AgentAPI(), '/')
