import unittest

from SentimentAnalysis.sentiment_analysis import sentiment_analyzer


class TestSentimentAnalyzer(unittest.TestCase): 
    def test_sentiment_analyzer(self):
        # Test with a positive statement
        result_1 = sentiment_analyzer('I love working with AI models!')
        self.assertEqual(result_1['label'], 'SENT_POSITIVE')

        # Test with a negative statement
        result_2 = sentiment_analyzer('I hate working with AI models!')
        self.assertEqual(result_2['label'], 'SENT_NEGATIVE')

        # Test with a neutral statement
        result_3 = sentiment_analyzer('I am working with AI models.')
        self.assertEqual(result_3['label'], 'SENT_NEUTRAL')


if __name__ == "__main__":
    unittest.main()





