import requests


def sentiment_analyzer(text_to_analyse):
	"""Analyze sentiment for input text via the hosted Watson NLP endpoint."""
	url = (
		"https://sn-watson-sentiment-bert.labs.skills.network/v1/"
		"watson.runtime.nlp.v1/NlpService/SentimentPredict"
	)
	payload = {"raw_document": {"text": text_to_analyse}}
	header = {
		"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"
	}

	response = requests.post(url, json=payload, headers=header, timeout=10)

	if response.status_code == 200:
		sentiment = response.json().get("documentSentiment", {})
		return {
			"label": sentiment.get("label"),
			"score": sentiment.get("score"),
		}

	# The endpoint returns 500 for invalid or empty text in this lab service.
	return {"label": None, "score": None}