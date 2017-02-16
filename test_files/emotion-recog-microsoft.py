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
    Contact API and process returned content
    :param json: used for extra info (such a URL image processing)
    :param data: locally available data to be analyzed
    :param headers: request headers
    :param params: request parameters
    :return: JSON or image depending on request, or None if no data could be extracted
    """
    retries = 0
    result = None

    # TODO rotate keys if we are out of API calls

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


def analyzeImage(img):
    """
    Analyze an image with the Microsoft Emotion Recognition API
    :param img: a numpy array representing the image
    :return: a JSON object as specified by the API, or None if something went wrong
    """
    data = cv.imencode('.png', im)[1].tostring()  # convert image to string data

    # Create header
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = API_KEY
    headers['Content-Type'] = 'application/octet-stream'

    # Contact API
    return processRequest(None, data, headers, None)


cam = cv.VideoCapture(0)
retVal, im = cam.read()
print(retVal)

result = analyzeImage(im)

print(json.dumps(result, sort_keys=True, indent=4, separators={',', ': '}))

print(result[0]["scores"])

cam.release()
