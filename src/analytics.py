#!/usr/bin/env python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from constants import TEXT_ANALYTICS_KEY, TEXT_ANALYTICS_ENDPOINT


class AnalyticsProvider:
    def __init__(self):
        self._client = _get_analytics_client()

    def get_sentiment(self, song_list):
        for song in song_list:
            response = self._client.analyze_sentiment(documents=[song["lyrics"]])[0]

            if "error" not in response.keys():
                song["score"] = {
                    "positive": response["confidence_scores"]["positive"],
                    "neutral": response["confidence_scores"]["neutral"],
                    "negative": response["confidence_scores"]["negative"],
                }

                yield song


def _get_analytics_client():
    text_analytics_key = os.getenv(TEXT_ANALYTICS_KEY)
    text_analytics_endpoint = os.getenv(TEXT_ANALYTICS_ENDPOINT)
    text_analytics_cred = AzureKeyCredential(text_analytics_key)

    return TextAnalyticsClient(
        endpoint=text_analytics_endpoint, credential=text_analytics_cred
    )
