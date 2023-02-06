import os
import sys
import time
from array import array

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import (
    OperationStatusCodes,
    VisualFeatureTypes,
)
from dotenv import load_dotenv
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image

load_dotenv()

serverIP = os.getenv("SERVER_IP")

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.getenv("azure_api_key")
endpoint = os.getenv("endpoint_path")

computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
print("===== Read File - remote =====")
# Get an image with text
read_image_url = "http://sc-dr.tw/shangchan/upload/images/scqa_Disposal_Warning04"

# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url,  raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()
'''
END - Read File - remote
'''

print("End of Computer Vision quickstart.")
