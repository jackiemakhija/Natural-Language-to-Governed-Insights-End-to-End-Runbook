"""
Main application entry point for Natural Language Governed Insights
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

from src.data_ingestion import DataIngestion
from src.nlp_processor import NLPProcessor
from src.insights_generator import InsightsGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_configuration():
    """Load configuration from settings file"""
    config_path = Path(__file__).parent / "config" / "settings.json"
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main application workflow"""
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_configuration()
    
    logger.info("Starting Natural Language Governed Insights Application")
    
    # Initialize components
    try:
        # Data Ingestion
        storage_account = os.getenv('AZURE_STORAGE_ACCOUNT_NAME') or config['azure']['storage']['account_name']
        data_ingestion = DataIngestion(storage_account)
        
        # NLP Processor
        nlp_endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT') or config['azure']['text_analytics']['endpoint']
        nlp_key = os.getenv('AZURE_TEXT_ANALYTICS_KEY') or config['azure']['text_analytics']['key']
        nlp_processor = NLPProcessor(nlp_endpoint, nlp_key)
        
        # Insights Generator
        insights_generator = InsightsGenerator()
        
        # Load sample data
        sample_data_path = Path(__file__).parent / "data" / "sample_data.json"
        with open(sample_data_path, 'r') as f:
            sample_data = json.load(f)
        
        # Process sample queries
        logger.info("Processing sample queries...")
        for query in sample_data.get('queries', []):
            logger.info(f"Processing query: {query['text']}")
            
            # Process with NLP
            nlp_result = nlp_processor.process_natural_language_query(query['text'])
            
            # Generate insights
            insight = insights_generator.generate_insight(query, nlp_result)
            
            print(f"\n{'='*60}")
            print(f"Query: {query['text']}")
            print(f"Sentiment: {insight['sentiment']['sentiment']}")
            print(f"Summary: {insight['summary']}")
            print(f"Recommendations:")
            for rec in insight['recommendations']:
                print(f"  - {rec}")
            print(f"{'='*60}\n")
        
        # Process sample feedback
        logger.info("Processing sample feedback...")
        for feedback in sample_data.get('sample_feedback', []):
            logger.info(f"Processing feedback: {feedback['id']}")
            
            nlp_result = nlp_processor.process_natural_language_query(feedback['text'])
            insight = insights_generator.generate_insight(feedback, nlp_result)
        
        # Export insights
        output_path = Path(__file__).parent / "insights_output.json"
        insights_generator.export_insights(str(output_path))
        
        logger.info(f"All insights exported to {output_path}")
        logger.info("Application completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
