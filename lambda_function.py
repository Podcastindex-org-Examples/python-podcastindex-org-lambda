import config
from datetime import date
import hashlib
import json
from json import JSONEncoder
import requests
import time

class SearchResponse(object):
    def __init__(self):
        self.results = []
    
        
class Podcast(object):
    def __init__(self, title, url, image):
        self.title = title
        self.url = url
        self.image = image
    
# subclass JSONEncoder
class SearchResponseEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
            
            
def lambda_handler(event, context):
    # setup some basic vars for the search api. 
    # for more information, see https://api.podcastindex.org/developer_docs
    api_key = config.api_key
    api_secret = config.api_secret
    query = event["queryStringParameters"]['q']
    url = "https://api.podcastindex.org/api/1.0/search/byterm?q=" + query

    # the api follows the Amazon style authentication
    # see https://docs.aws.amazon.com/AmazonS3/latest/dev/S3_Authentication2.html
    
    # we'll need the unix time
    epoch_time = int(time.time())
    
    # our hash here is the api key + secret + time 
    data_to_hash = api_key + api_secret + str(epoch_time)
    # which is then sha-1'd
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
    
    # now we build our request headers
    headers = {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha_1,
        'User-Agent': 'postcasting-index-python-cli'
    }
    
    # uncomment these to make debugging easier.
    print ('----------------------------------------')
    print ('api key: ' + api_key)
    print ('api secret: ' + api_secret)
    print ('query: ' + query)
    print ('url: ' + url)
    print ('headers')
    print (headers)
    print ('----------------------------------------')

    # perform the actual post request
    r = requests.post(url, headers=headers)
    
    # if it's successful, dump the contents (in a prettified json-format)
    # else, dump the error code we received
    if r.status_code == 200:
        # print ('<< Received >>')
        #print (json.dumps(json.loads(r.text), indent=2))

        response = SearchResponse()
        #response.message = 'Successful search'

        for p in json.loads(r.text)['feeds']:
            response.results.append(Podcast(p['title'], p['url'], p['image']))

        return {
            'statusCode': 200,
            'body': json.dumps(response, indent=4, cls=SearchResponseEncoder)
        }
    else:
        # print ('<< Received ' + str(r.status_code) + '>>')
        return {
            'statusCode': 500,
            'body': json.dumps('Internal service error')
        }

def main():
    # fake our request body
    request_body = {}
    request_body["queryStringParameters"] = {}
    request_body["queryStringParameters"]["q"] = "cooking"

    # call the lambda handler
    lambda_handler(request_body, '')

if __name__ == "__main__":
    main()