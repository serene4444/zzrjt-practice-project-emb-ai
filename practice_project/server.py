"""Flask entrypoint for the sentiment analysis web application."""

from flask import Flask, render_template, request

from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")


@app.route("/sentimentAnalyzer")
def sent_analyzer():
    """Analyze user-provided text and return a human-readable sentiment message."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return "Please enter text to analyze."

    response = sentiment_analyzer(text_to_analyze)

    if response.get("label") is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'{response['label']}' with a score of {response['score']}."
    )


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
