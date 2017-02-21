"""
Interacts with Microsoft Emotion Recognition API
"""
import requests
import json
import time
import cv2 as cv
from collections import Counter

class EmotionRecognition:
    POSSIBLE_EMOTIONS = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness',
                         'surprise']
    MAX_RETRIES = 10

    def __init__(self, credentials='key.txt', API_URL='https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'):
        # Endpoint and credentials
        # with open(credentials, 'r') as keyFile:
        #     self.API_KEY = keyFile.readline()
        self.API_KEY = 'aabb08051cef46f4a8ca20f3b5b8c0e8' #erics
        self.API_URL = API_URL


    def process_request(self, json_data, data, headers, params):
        """
        Contact API and process returned content
        :param json_data: used for extra info (such a URL image processing)
        :param data: locally available data to be analyzed
        :param headers: request headers
        :param params: request parameters
        :return: JSON or image depending on request, or None if no data could be extracted
        """
        retries = 0
        result = None

        # TODO rotate keys if we are out of API calls

        while True:
            response = requests.request('post', self.API_URL, json=json_data, data=data, headers=headers,
                                        params=params)

            # Handle error response
            if response.status_code == 429:
                print("Message: {0}".format(response.json()['error']['message']))
                if retries <= self.MAX_RETRIES:
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
    def analyze_image(self,img):
        """
        Analyze an image with the Microsoft Emotion Recognition API
        :param img: a numpy array representing the image
        :return: a JSON object as specified by the API, or None if something went wrong
        """
        data = cv.imencode('.png', img)[1].tostring()  # convert image to string data

        # Create header
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self.API_KEY
        headers['Content-Type'] = 'application/octet-stream'

        # Contact API
        return self.process_request(None, data, headers, None)


    def get_top_emotion(self,result):
        """
        Get emotion with the highest likelihood from the first face detected by the API
        :param json: json response from API
        :return: string representation of most probably emotion
        """
        if len(result) <= 0 or 'scores' not in result[0]:
            return None

        # Get top probability
        counter = Counter(result[0]['scores'])
        return counter.most_common(1)[0][0]