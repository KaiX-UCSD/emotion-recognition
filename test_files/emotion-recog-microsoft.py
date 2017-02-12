"""
Interacts with Microsoft Emotion Recognition API
"""
import requests
import json
import time
import cv2 as cv

MAX_RETRIES = 10

# Endpoint and credentials
with open('key.txt', 'r') as keyFile:
    API_KEY = keyFile.readline()
API_URL = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'


def processRequest(json, data, headers, params):
    """
    Process request from API and return appropriate format
    """
    retries = 0
    result = None

    while True:
        response = requests.request('post', API_URL, json=json, data=data, headers=headers,
                                    params=params)

        # Handle error response
        if response.status_code == 429:
            print("Message: {0}".format(response.json()['error']['message']))
            if retries <= MAX_RETRIES:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying')
                break

        # Handle successful response
        elif response.status_code == 200 or response.status_code == 201:
            # Get the type of the content returned
            if ('content-length' in response.headers and
                        int(response.headers['content-length']) == 0):
                result = None
            elif ('content-type' in response.headers and
                      isinstance(response.headers['content-type'], str)):
                if 'application/json' in response.headers['content-type'].lower():  # json
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():  # image
                    result = response.content

        # Handle ambiguous response
        else:
            print('Error code {0}'.format(response.status_code))
            print('Message: {0}'.format(response.json()['error']['message']))

        break
    return result


# TODO get rid of hard coded link
# with open('face1.jpg', 'rb') as f:
#     data = f.read()

cam = cv.VideoCapture(0)
retVal, im = cam.read()

print(retVal)

cv.imshow('face', im)
data = cv.imencode('.png', im)[1].tostring()

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = API_KEY
headers['Content-Type'] = 'application/octet-stream'

result = processRequest(None, data, headers, None)

print(json.dumps(result, sort_keys=True, indent=4, separators={',', ': '}))
