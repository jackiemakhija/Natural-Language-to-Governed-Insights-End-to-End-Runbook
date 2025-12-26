"""
Insights Generator Module
Generates insights from processed data
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class InsightsGenerator:
    """Generate insights from processed data"""
    
    def __init__(self):
        """Initialize insights generator"""
        self.insights_cache = []
    
    def generate_insight(self, data: Dict[str, Any], nlp_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an insight from data and NLP results"""
        try:
            insight = {
                "timestamp": datetime.utcnow().isoformat(),
                "sentiment": nlp_result.get("sentiment", {}),
                "key_topics": nlp_result.get("key_phrases", []),
                "entities": nlp_result.get("entities", []),
                "summary": self._generate_summary(nlp_result),
                "recommendations": self._generate_recommendations(nlp_result),
                "confidence": self._calculate_confidence(nlp_result)
            }
            
            self.insights_cache.append(insight)
            logger.info("Generated new insight")
            return insight
        except Exception as e:
            logger.error(f"Failed to generate insight: {e}")
            raise
    
    def _generate_summary(self, nlp_result: Dict[str, Any]) -> str:
        """Generate a summary of the analysis"""
        sentiment = nlp_result.get("sentiment", {}).get("sentiment", "neutral")
        key_phrases = nlp_result.get("key_phrases", [])
        
        if key_phrases:
            top_phrases = ", ".join(key_phrases[:3])
            summary = f"Overall sentiment is {sentiment}. Key topics: {top_phrases}."
        else:
            summary = f"Overall sentiment is {sentiment}."
        
        return summary
    
    def _generate_recommendations(self, nlp_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        sentiment = nlp_result.get("sentiment", {}).get("sentiment", "neutral")
        
        if sentiment == "negative":
            recommendations.append("Consider addressing negative feedback promptly")
            recommendations.append("Investigate root causes of dissatisfaction")
        elif sentiment == "positive":
            recommendations.append("Maintain current positive practices")
            recommendations.append("Share success stories with team")
        else:
            recommendations.append("Monitor for changes in sentiment trends")
        
        return recommendations
    
    def _calculate_confidence(self, nlp_result: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        sentiment_scores = nlp_result.get("sentiment", {}).get("confidence_scores", {})
        
        if sentiment_scores:
            # Get the highest confidence score
            max_confidence = max(sentiment_scores.values())
            return round(max_confidence, 3)
        
        return 0.5
    
    def get_insights_history(self) -> List[Dict[str, Any]]:
        """Retrieve all generated insights"""
        return self.insights_cache
    
    def export_insights(self, filepath: str):
        """Export insights to file"""
        import json
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.insights_cache, f, indent=2)
            logger.info(f"Insights exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export insights: {e}")
            raise
