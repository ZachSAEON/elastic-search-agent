
# CherryPy testng details
server_domain = 'localhost'
server_port = 9210
server_url = 'http://{}:{}'.format(server_domain, server_port)

# ES details
es_domain = 'localhost'
es_port = 9200
metadata_index_name = 'md_index_1'
token_index_name = 'rt_index_1'

# OAI PMH Repo Identity details
repositoryName = 'SAEON'
baseURL = 'http://{}'
protocolVersion = '2'
adminEmail = 'info@saeon.ac.za'
earliestDatestamp = '{}-01-01T00:00:00Z'
deletedRecord = 'persistent'
granularity = 'YYYY-MM-DDThh:mm:ssZ'
compressions = ['gzip', 'deflate']
scheme = 'oai'
repositoryIdentifier = '{}/oaipmh'
delimiter = ':'
sampleIdentifier = 'oai:{}/oaipmh:12425'
