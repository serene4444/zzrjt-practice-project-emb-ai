"""Utilities for sentiment analysis using a remote model with local fallback.

This module attempts remote inference first for best quality and uses a small
local rule-based fallback when the remote service is unavailable.
"""

from functools import lru_cache
import time

import requests

SESSION = requests.Session()
REMOTE_TIMEOUT = (0.6, 1.2)
REMOTE_COOLDOWN_SECONDS = 45
REMOTE_STATE = {"next_remote_attempt_at": 0.0}


def _fallback_sentiment(text_to_analyze):
    """Infer a basic sentiment label from keyword matching.

    Args:
        text_to_analyze: Input text to classify.

    Returns:
        A dictionary containing sentiment label and score.
    """
    positive_words = {"love", "like", "great", "awesome", "good", "excellent", "happy"}
    negative_words = {"hate", "bad", "terrible", "awful", "poor", "sad", "angry"}
    lowered_text = text_to_analyze.lower()

    if any(word in lowered_text for word in positive_words):
        return {"label": "SENT_POSITIVE", "score": 0.75}
    if any(word in lowered_text for word in negative_words):
        return {"label": "SENT_NEGATIVE", "score": 0.75}
    return {"label": "SENT_NEUTRAL", "score": 0.5}


def _mark_remote_unavailable():
    """Open a cooldown window to avoid repeated slow remote retries."""
    REMOTE_STATE["next_remote_attempt_at"] = (
        time.monotonic() + REMOTE_COOLDOWN_SECONDS
    )


def _remote_available():
    """Return whether the remote service is currently eligible for retry."""
    return time.monotonic() >= REMOTE_STATE["next_remote_attempt_at"]


def _query_remote_sentiment(text_to_analyze):
    """Query the hosted Watson endpoint and parse the response.

    Args:
        text_to_analyze: Input text to classify.

    Returns:
        A sentiment dictionary if successful, otherwise None.
    """
    url = (
        "https://sn-watson-sentiment-bert.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/SentimentPredict"
    )
    payload = {"raw_document": {"text": text_to_analyze}}
    headers = {
        "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
    }

    try:
        response = SESSION.post(url, json=payload, headers=headers, timeout=REMOTE_TIMEOUT)
    except requests.exceptions.RequestException:
        _mark_remote_unavailable()
        return None

    if response.status_code != 200:
        _mark_remote_unavailable()
        return None

    try:
        sentiment = response.json().get("documentSentiment", {})
    except ValueError:
        _mark_remote_unavailable()
        return None

    if sentiment.get("label") is None:
        return None

    return {
        "label": sentiment.get("label"),
        "score": sentiment.get("score"),
    }


@lru_cache(maxsize=256)
def _sentiment_analyzer_cached(text_to_analyze):
    """Return sentiment results with memoization for repeated inputs."""
    if not text_to_analyze.strip():
        return {"label": None, "score": None}

    if _remote_available():
        remote_result = _query_remote_sentiment(text_to_analyze)
        if remote_result is not None:
            return remote_result

    return _fallback_sentiment(text_to_analyze)


def sentiment_analyzer(text_to_analyze):
    """Analyze text and return label/score sentiment metadata.

    Args:
        text_to_analyze: Input sentence from user.

    Returns:
        A dictionary with keys `label` and `score`.
    """
    return _sentiment_analyzer_cached(text_to_analyze)
