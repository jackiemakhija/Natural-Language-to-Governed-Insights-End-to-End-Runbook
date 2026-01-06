"""
Natural Language to Governed Insights - Streamlit App
Hugging Face Spaces Deployment
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import logging

# Import local modules
from src.nlp_processor import NLPProcessor
from src.insights_generator import InsightsGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Natural Language to Governed Insights",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .insight-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .positive {
        color: #2E7D32;
        font-weight: bold;
    }
    .negative {
        color: #C62828;
        font-weight: bold;
    }
    .neutral {
        color: #F57C00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'insights_history' not in st.session_state:
    st.session_state.insights_history = []
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0


def load_sample_data():
    """Load sample data from JSON file"""
    sample_data_path = Path(__file__).parent / "data" / "sample_data.json"
    try:
        with open(sample_data_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load sample data: {e}")
        return {"queries": [], "sample_feedback": []}


def initialize_services():
    """Initialize NLP and Insights services with demo mode support"""
    # Check if Azure credentials are provided
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    
    # Demo mode indicator
    demo_mode = not (endpoint and key)
    
    if demo_mode:
        st.sidebar.warning("⚠️ Running in DEMO MODE - Using mock responses")
        st.sidebar.info("To use real Azure AI services, configure secrets in HF Space settings")
        nlp_processor = None
    else:
        try:
            nlp_processor = NLPProcessor(endpoint, key)
            st.sidebar.success("✅ Connected to Azure AI Services")
        except Exception as e:
            st.sidebar.error(f"Failed to connect to Azure: {e}")
            nlp_processor = None
    
    insights_generator = InsightsGenerator()
    
    return nlp_processor, insights_generator, demo_mode


def analyze_text_demo(text):
    """Demo mode analysis (mock responses)"""
    # Simple sentiment detection based on keywords
    positive_keywords = ['excellent', 'great', 'good', 'love', 'amazing', 'wonderful', 'positive', 'happy']
    negative_keywords = ['bad', 'terrible', 'poor', 'disappointed', 'awful', 'hate', 'negative', 'unhappy']
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_keywords if word in text_lower)
    negative_count = sum(1 for word in negative_keywords if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = {"positive": 0.75, "neutral": 0.15, "negative": 0.10}
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = {"positive": 0.10, "neutral": 0.15, "negative": 0.75}
    else:
        sentiment = "neutral"
        confidence = {"positive": 0.30, "neutral": 0.50, "negative": 0.20}
    
    # Extract simple key phrases (3-grams)
    words = text.split()
    key_phrases = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1) if i < 3]
    
    return {
        "query": text,
        "sentiment": {
            "sentiment": sentiment,
            "confidence_scores": confidence
        },
        "key_phrases": key_phrases if key_phrases else ["customer feedback", "service quality"],
        "entities": []
    }


def process_query(query_text, nlp_processor, insights_generator, demo_mode):
    """Process a natural language query"""
    with st.spinner("Analyzing query..."):
        try:
            # Process with NLP
            if demo_mode:
                nlp_result = analyze_text_demo(query_text)
            else:
                nlp_result = nlp_processor.process_natural_language_query(query_text)
            
            # Generate insights
            insight = insights_generator.generate_insight(
                {"text": query_text, "timestamp": datetime.now().isoformat()},
                nlp_result
            )
            
            # Store in history
            st.session_state.insights_history.append(insight)
            st.session_state.query_count += 1
            
            return insight, nlp_result
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            st.error(f"Error: {e}")
            return None, None


def display_insight(insight, nlp_result):
    """Display insight results"""
    if not insight:
        return
    
    # Sentiment display
    sentiment = insight['sentiment']['sentiment']
    sentiment_class = sentiment.lower()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Sentiment</h3>
            <p class="{sentiment_class}">{sentiment.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Confidence</h3>
            <p>{insight['confidence']:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Key Topics</h3>
            <p>{len(insight['key_topics'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("### 📊 Analysis Results")
    
    st.markdown(f"**Summary:** {insight['summary']}")
    
    # Key phrases
    if insight['key_topics']:
        st.markdown("**Key Topics:**")
        st.write(", ".join(insight['key_topics']))
    
    # Recommendations
    if insight['recommendations']:
        st.markdown("**💡 Recommendations:**")
        for i, rec in enumerate(insight['recommendations'], 1):
            st.markdown(f"{i}. {rec}")
    
    # Sentiment confidence scores
    st.markdown("**Sentiment Confidence Scores:**")
    scores = insight['sentiment']['confidence_scores']
    score_cols = st.columns(3)
    
    with score_cols[0]:
        st.metric("Positive", f"{scores['positive']:.1%}")
    with score_cols[1]:
        st.metric("Neutral", f"{scores['neutral']:.1%}")
    with score_cols[2]:
        st.metric("Negative", f"{scores['negative']:.1%}")


def main():
    """Main application"""
    # Header
    st.markdown('<p class="main-header">🧠 Natural Language to Governed Insights</p>', unsafe_allow_html=True)
    st.markdown("Transform natural language questions into governed insights using Azure AI")
    
    # Initialize services
    nlp_processor, insights_generator, demo_mode = initialize_services()
    
    # Sidebar
    st.sidebar.title("📋 About")
    st.sidebar.info("""
    This application demonstrates natural language processing and insight generation using Azure AI services.
    
    **Features:**
    - Sentiment analysis
    - Key phrase extraction
    - Entity recognition
    - Automated recommendations
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.metric("Queries Processed", st.session_state.query_count)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🔍 Analyze Text", "📊 Sample Data", "📈 History"])
    
    with tab1:
        st.markdown("### Enter your query or feedback")
        
        query_input = st.text_area(
            "Enter text to analyze:",
            placeholder="e.g., 'What are the main customer complaints this month?'",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        
        if analyze_button and query_input:
            insight, nlp_result = process_query(query_input, nlp_processor, insights_generator, demo_mode)
            if insight:
                display_insight(insight, nlp_result)
        elif analyze_button:
            st.warning("Please enter some text to analyze")
        
        # Sample queries
        st.markdown("### 💡 Try These Sample Queries")
        sample_data = load_sample_data()
        
        sample_queries = [q['text'] for q in sample_data.get('queries', [])]
        if sample_queries:
            cols = st.columns(2)
            for idx, sample_query in enumerate(sample_queries[:4]):
                with cols[idx % 2]:
                    if st.button(f"📝 {sample_query}", key=f"sample_{idx}"):
                        insight, nlp_result = process_query(sample_query, nlp_processor, insights_generator, demo_mode)
                        if insight:
                            display_insight(insight, nlp_result)
    
    with tab2:
        st.markdown("### 📊 Sample Feedback Data")
        sample_data = load_sample_data()
        
        if sample_data.get('sample_feedback'):
            for feedback in sample_data['sample_feedback']:
                with st.expander(f"{feedback['id']} - {feedback['category'].title()}"):
                    st.write(f"**Text:** {feedback['text']}")
                    st.write(f"**Date:** {feedback['date']}")
                    
                    if st.button(f"Analyze This Feedback", key=f"analyze_{feedback['id']}"):
                        insight, nlp_result = process_query(feedback['text'], nlp_processor, insights_generator, demo_mode)
                        if insight:
                            display_insight(insight, nlp_result)
    
    with tab3:
        st.markdown("### 📈 Analysis History")
        
        if st.session_state.insights_history:
            for idx, insight in enumerate(reversed(st.session_state.insights_history)):
                with st.expander(f"Query {len(st.session_state.insights_history) - idx} - {insight['sentiment']['sentiment'].title()}"):
                    st.markdown(f"**Timestamp:** {insight['timestamp']}")
                    st.markdown(f"**Summary:** {insight['summary']}")
                    st.markdown(f"**Confidence:** {insight['confidence']:.1%}")
            
            if st.button("Clear History"):
                st.session_state.insights_history = []
                st.session_state.query_count = 0
                st.rerun()
        else:
            st.info("No analysis history yet. Start by analyzing some text!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit • Powered by Azure AI Services</p>
        <p>🔒 Enterprise-grade governance and compliance built-in</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
