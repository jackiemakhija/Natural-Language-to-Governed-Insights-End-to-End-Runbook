"""
NLP Processor Module
Handles natural language processing and understanding
"""

import logging
from typing import List, Dict, Any
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

logger = logging.getLogger(__name__)


class NLPProcessor:
    """Natural Language Processing handler"""
    
    def __init__(self, endpoint: str, key: str):
        """Initialize NLP processor with Azure credentials"""
        self.endpoint = endpoint
        self.key = key
        self.client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of given text"""
        try:
            response = self.client.analyze_sentiment(documents=[text])[0]
            
            result = {
                "sentiment": response.sentiment,
                "confidence_scores": {
                    "positive": response.confidence_scores.positive,
                    "neutral": response.confidence_scores.neutral,
                    "negative": response.confidence_scores.negative
                }
            }
            logger.info(f"Sentiment analysis completed: {result['sentiment']}")
            return result
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        try:
            response = self.client.extract_key_phrases(documents=[text])[0]
            key_phrases = response.key_phrases
            logger.info(f"Extracted {len(key_phrases)} key phrases")
            return key_phrases
        except Exception as e:
            logger.error(f"Key phrase extraction failed: {e}")
            raise
    
    def recognize_entities(self, text: str) -> List[Dict[str, Any]]:
        """Recognize named entities in text"""
        try:
            response = self.client.recognize_entities(documents=[text])[0]
            
            entities = [
                {
                    "text": entity.text,
                    "category": entity.category,
                    "subcategory": entity.subcategory,
                    "confidence_score": entity.confidence_score
                }
                for entity in response.entities
            ]
            logger.info(f"Recognized {len(entities)} entities")
            return entities
        except Exception as e:
            logger.error(f"Entity recognition failed: {e}")
            raise
    
    def process_natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query"""
        result = {
            "query": query,
            "sentiment": self.analyze_sentiment(query),
            "key_phrases": self.extract_key_phrases(query),
            "entities": self.recognize_entities(query)
        }
        return result
