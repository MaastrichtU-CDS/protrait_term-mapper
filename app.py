from flask import Flask, request, send_from_directory
from flask_cors import CORS
from rdflib.term import URIRef
from datasources.triples import SPARQLTripleStore

from fairifier.termmapping import TermMapper
import os

# triple_addr = 'http://172.18.22.17:3030/ds'
# endpoint = 'http://172.18.22.17:7200/repositories/data'
# endpoint = 'http://172.18.22.17:7200/repositories/johan_test'
endpoint = 'http://localhost:7200/repositories/data'
endpoint = os.environ.get("ENDPOINT_URL", endpoint)
print("Using SPARQL endpoint: " + endpoint)
mapper = TermMapper(SPARQLTripleStore(endpoint, update_endpoint=endpoint + '/statements'))

app = Flask(__name__, static_folder="build", static_url_path='')
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# Serve the react built content
@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

@app.route('/classes', methods=['GET'])
def get_classes():
    unmapped_classes = mapper.get_unmapped_types()

    return {
        'classes': unmapped_classes
    }

@app.route("/values", methods=['GET', 'POST'])
def get_local_values():
    uri = URIRef(request.form.get('class'))
    values = mapper.get_values_for_class(uri)
    targets = mapper.get_targets_for_class(uri)
    mappings = mapper.get_mappings_for_class(uri)

    print(values)

    return {
        'localValues': values, 
        'targets': [{'uri': str(target['uri']), 'label': str(target['label'])} for target in targets], 
        'mappings': {mapping['value']: str(mapping['target']) for mapping in mappings}
    }

@app.route("/mappings", methods=['GET'])
def get_mappings():
    mappings = mapper.get_mappings()
    return {
        'storedMappings': mappings
    }

@app.route("/add-mapping", methods=['POST'])
def add_mapping():
    source_class = URIRef(request.form.get('class'))
    value = request.form.get('value')
    target = URIRef(request.form.get('target'))

    mapper.add_mapping(target, source_class, value)

    mappings = mapper.get_mappings_for_class(URIRef(source_class))

    return {
        'mappings': {mapping['value']: str(mapping['target'])for mapping in mappings}
    }

@app.route("/delete-mapping", methods=["POST"])
def delete_mapping():
    source_class = URIRef(request.form.get('class'))
    value = request.form.get('value')
    target = URIRef(request.form.get('target'))

    mapper.delete_mapping(source_class, value, target)
    return {
        'storedMappings': mapper.get_mappings()
    }

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')