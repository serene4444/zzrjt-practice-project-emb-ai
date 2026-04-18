let RunSentimentAnalysis = ()=>{
    const textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                document.getElementById("system_response").innerHTML = xhttp.responseText;
            } else {
                document.getElementById("system_response").innerHTML = "Could not analyze sentiment right now. Please try again.";
            }
        }
    };
    xhttp.onerror = function() {
        document.getElementById("system_response").innerHTML = "Network error while contacting the server.";
    };
    xhttp.open("GET", "sentimentAnalyzer?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
}
