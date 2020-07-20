from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1
from google.cloud.automl_v1.proto import service_pb2

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="adobot-283815-1b29c0d004b0.json"

def inline_text_payload(text):
  return {'text_snippet': {'content': text, 'mime_type': 'text/plain'} }

def get_prediction(text, model_name="projects/635112130949/locations/us-central1/models/TCN3179860195295625216"):
  options = ClientOptions(api_endpoint='automl.googleapis.com')
  prediction_client = automl_v1.PredictionServiceClient(client_options=options)

  payload = inline_text_payload(text)

  params = {}
  request = prediction_client.predict(model_name, payload, params)
  return request  # waits until request is returned



if __name__ == '__main__':
  a = get_prediction("After fixing image resolution at 300 (like we need for our annual) our images are coming out at insane sizes like 70 MB, they won't upload to Jostens....")
  print(a)