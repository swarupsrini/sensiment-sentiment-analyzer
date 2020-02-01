from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions


def analyze(input_text):

    # Setup
    with open(".ibm-api-key", "r") as f:
        key = f.read()
    service_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/57bf40d3-1788-445f-8717-63ab3b83442e"
    authenticator = IAMAuthenticator(apikey=key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(service_url=service_url)

    # Analyze
    response = natural_language_understanding.analyze(
        text=input_text,
        features=Features(emotion=EmotionOptions())).get_result()

    return response["emotion"]["document"]["emotion"]


if __name__ == "__main__":
    print(analyze("Hi there, my name is Bob and I am sad"))
