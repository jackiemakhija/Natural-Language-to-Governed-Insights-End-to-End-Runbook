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
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Import local modules
from src.nlp_processor import NLPProcessor
from src.insights_generator import InsightsGenerator

# Global variables
QUERY_COUNT = 0
GITHUB_REPO = "jagjeetmakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook"
SESSION_FILE = "session_history.json"

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

def save_session_history():
    """Save session history to file for persistence"""
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(st.session_state.insights_history, f, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save session history: {e}")


def load_session_history():
    """Load session history from file"""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                history = json.load(f)
                logger.info(f"Loaded {len(history)} items from session history")
                return history
    except Exception as e:
        logger.warning(f"Failed to load session history: {e}")
    return []


# Initialize session state (must be after helper definitions to avoid NameError on first load)
if 'insights_history' not in st.session_state:
    st.session_state.insights_history = load_session_history()
if 'query_count' not in st.session_state:
    st.session_state.query_count = len(st.session_state.insights_history)
if 'github_stats' not in st.session_state:
    st.session_state.github_stats = None
if 'github_stats_timestamp' not in st.session_state:
    st.session_state.github_stats_timestamp = None


def normalize_sentiment_value(value):
    """Normalize sentiment field to a lowercase string label."""
    try:
        if isinstance(value, dict):
            return str(value.get('sentiment', 'unknown')).lower()
        if value is None:
            return 'unknown'
        return str(value).lower()
    except Exception:
        return 'unknown'


def extract_topics(insight):
    """Return a safe list of topics from an insight entry."""
    topics = insight.get('key_topics', []) if isinstance(insight, dict) else []
    if topics is None:
        return []
    if isinstance(topics, list):
        return [str(t) for t in topics if t is not None]
    # Handle unexpected scalar by wrapping into list
    return [str(topics)]


def create_sentiment_distribution_chart(history):
    """Create a pie chart showing sentiment distribution"""
    if not history:
        return None
    
    sentiments = [normalize_sentiment_value(insight.get('sentiment')) for insight in history]
    sentiment_counts = Counter(sentiments)
    if not sentiment_counts:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=list(sentiment_counts.keys()),
        values=list(sentiment_counts.values()),
        hole=0.3,
        marker=dict(colors=['#28a745', '#dc3545', '#ffc107'])
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        height=300,
        margin=dict(t=40, b=0, l=0, r=0)
    )
    
    return fig


def create_confidence_trend_chart(history):
    """Create a line chart showing confidence scores over time"""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    if 'confidence' not in df:
        return None
    df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce').fillna(0)
    df['index'] = range(1, len(df) + 1)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['index'],
        y=df['confidence'],
        mode='lines+markers',
        name='Confidence',
        line=dict(color='#007bff', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Confidence Score Trend",
        xaxis_title="Analysis Number",
        yaxis_title="Confidence Score",
        yaxis=dict(range=[0, 1]),
        height=300,
        margin=dict(t=40, b=40, l=40, r=20)
    )
    
    return fig


def create_topics_frequency_chart(history):
    """Create a bar chart of most common topics"""
    if not history:
        return None
    
    all_topics = []
    for insight in history:
        all_topics.extend(extract_topics(insight))
    
    if not all_topics:
        return None
    
    topic_counts = Counter(all_topics).most_common(10)
    topics, counts = zip(*topic_counts)
    
    fig = go.Figure(data=[go.Bar(
        x=list(counts),
        y=list(topics),
        orientation='h',
        marker=dict(color='#17a2b8')
    )])
    
    fig.update_layout(
        title="Top 10 Topics",
        xaxis_title="Frequency",
        yaxis_title="Topic",
        height=400,
        margin=dict(t=40, b=40, l=150, r=20)
    )
    
    return fig


    def create_sentiment_timeline_chart(history):
        """Create a stacked area chart showing sentiment counts over time"""
        if not history:
            return None

        df = pd.DataFrame(history)
        if 'timestamp' not in df or 'sentiment' not in df:
            return None

        # Normalize timestamp and sentiment
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df['sentiment_normalized'] = df['sentiment'].apply(lambda s: s.get('sentiment', 'unknown') if isinstance(s, dict) else s)

        if df.empty:
            return None

        grouped = df.groupby([df['timestamp'].dt.date, 'sentiment_normalized']).size().reset_index(name='count')
        fig = px.area(
            grouped,
            x='timestamp',
            y='count',
            color='sentiment_normalized',
            title='Sentiment Over Time',
            color_discrete_map={'positive': '#28a745', 'negative': '#dc3545', 'neutral': '#ffc107'}
        )
        fig.update_layout(height=350, legend_title_text='Sentiment', margin=dict(t=50, b=20, l=40, r=20))
        fig.update_traces(mode='lines')
        return fig


    def create_confidence_distribution_chart(history):
        """Create a histogram for confidence scores"""
        if not history:
            return None

        df = pd.DataFrame(history)
        if 'confidence' not in df:
            return None

        df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')
        df = df.dropna(subset=['confidence'])
        if df.empty:
            return None

        fig = px.histogram(
            df,
            x='confidence',
            nbins=10,
            title='Confidence Distribution',
            color_discrete_sequence=['#1E88E5']
        )
        fig.update_layout(height=350, margin=dict(t=50, b=40, l=40, r=20), xaxis_title='Confidence', yaxis_title='Frequency')
        return fig


    def create_topics_treemap(history):
        """Create a treemap for topic importance"""
        if not history:
            return None

        all_topics = []
        for insight in history:
            all_topics.extend(extract_topics(insight))

        if not all_topics:
            return None

        topic_counts = Counter(all_topics)
        df = pd.DataFrame({
            'topic': list(topic_counts.keys()),
            'count': list(topic_counts.values())
        })

        fig = px.treemap(df, path=['topic'], values='count', title='Topic Coverage')
        fig.update_layout(height=350, margin=dict(t=50, b=20, l=10, r=10))
        return fig


def get_summary_stats(history):
    """Calculate summary statistics from history"""
    if not history:
        return None
    
    df = pd.DataFrame(history)

    if 'sentiment' not in df:
        return {
            'total_queries': len(df),
            'avg_confidence': df['confidence'].mean() if 'confidence' in df else 0,
            'sentiments': {},
            'unique_topics': 0
        }

    # Normalize sentiment to simple string values
    def extract_sentiment(value):
        if isinstance(value, dict):
            return value.get('sentiment', 'unknown')
        return value if value is not None else 'unknown'

    df['sentiment_normalized'] = df['sentiment'].apply(extract_sentiment)

    # Safe sentiment counts
    sentiments = df['sentiment_normalized'].value_counts(dropna=True).to_dict() if 'sentiment_normalized' in df else {}

    # Safe confidence average
    avg_confidence = df['confidence'].mean() if 'confidence' in df else 0

    total_queries = len(df)
    
    all_topics = []
    for insight in history:
        all_topics.extend(insight.get('key_topics', []))
    
    unique_topics = len(set(all_topics)) if all_topics else 0
    
    return {
        'total_queries': total_queries,
        'avg_confidence': avg_confidence,
        'sentiments': sentiments,
        'unique_topics': unique_topics
    }


def fetch_github_stats():
    """Fetch GitHub repository statistics with caching"""
    import time
    
    # Use cached stats if available (cache for 1 hour)
    current_time = time.time()
    if (st.session_state.github_stats is not None and 
        st.session_state.github_stats_timestamp is not None and
        current_time - st.session_state.github_stats_timestamp < 3600):
        return st.session_state.github_stats
    
    try:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Natural-Language-to-Governed-Insights-App"
        }
        token = os.getenv("GITHUB_TOKEN") or os.getenv("HF_GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}",
            headers=headers,
            timeout=5
        )
        
        logger.info(f"GitHub API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stats = {
                "stars": int(data.get("stargazers_count", 0)),
                "forks": int(data.get("forks_count", 0)),
                "watchers": int(data.get("watchers_count", 0)),
                "open_issues": int(data.get("open_issues_count", 0)),
                "url": str(data.get("html_url", "")),
                "description": str(data.get("description", ""))
            }
            
            # Cache the stats
            st.session_state.github_stats = stats
            st.session_state.github_stats_timestamp = current_time
            logger.info(f"Fetched GitHub stats: {stats}")
            return stats
        else:
            logger.warning(f"GitHub API error: {response.status_code} - {response.text}")
            if response.status_code == 403:
                logger.warning("GitHub API rate limit or auth required. Set GITHUB_TOKEN or HF_GITHUB_TOKEN.")
            
    except requests.exceptions.Timeout:
        logger.warning("GitHub API request timeout")
    except requests.exceptions.ConnectionError:
        logger.warning("GitHub API connection error")
    except Exception as e:
        logger.error(f"Failed to fetch GitHub stats: {e}", exc_info=True)
    
    # Return default or cached values
    return {
        "stars": 0,
        "forks": 0,
        "watchers": 0,
        "open_issues": 0,
        "url": f"https://github.com/{GITHUB_REPO}",
        "description": "Natural Language to Governed Insights"
    }



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
            if not nlp_result:
                raise ValueError("No NLP result returned")
            
            # Generate insights
            insight = insights_generator.generate_insight(
                {"text": query_text, "timestamp": datetime.now().isoformat()},
                nlp_result
            )
            
            # Store in history
            st.session_state.insights_history.append(insight)
            st.session_state.query_count += 1
            
            # Save session history
            save_session_history()
            
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
    sentiment = normalize_sentiment_value(insight.get('sentiment'))
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
    
    st.markdown(f"**Summary:** {insight.get('summary', 'No summary available')}")
    
    # Key phrases
    if insight.get('key_topics'):
        st.markdown("**Key Topics:**")
        st.write(", ".join(extract_topics(insight)))
    
    # Recommendations
    if insight.get('recommendations'):
        st.markdown("**💡 Recommendations:**")
        for i, rec in enumerate(insight.get('recommendations', []), 1):
            st.markdown(f"{i}. {rec}")
    
    # Sentiment confidence scores
    st.markdown("**Sentiment Confidence Scores:**")
    scores = insight.get('sentiment', {}).get('confidence_scores', {}) or {'positive': 0, 'neutral': 0, 'negative': 0}
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
    
    # Fetch and display GitHub stats with retry logic
    try:
        if st.session_state.github_stats is None:
            with st.sidebar.spinner("Loading GitHub stats..."):
                st.session_state.github_stats = fetch_github_stats()
        
        github_stats = st.session_state.github_stats
        if github_stats is None:
            github_stats = fetch_github_stats()
    except Exception as e:
        logger.error(f"Error fetching GitHub stats: {e}")
        github_stats = {"stars": 0, "forks": 0, "url": f"https://github.com/{GITHUB_REPO}"}
    
    st.sidebar.markdown("### 📥 App Downloaded Till Date")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        stars = github_stats.get("stars", 0)
        st.metric("⭐ GitHub Stars", f"{stars}")
    with col2:
        forks = github_stats.get("forks", 0)
        st.metric("🍴 Forks", f"{forks}")
    
    repo_url = github_stats.get("url", f"https://github.com/{GITHUB_REPO}")
    st.sidebar.markdown(f"[🔗 View on GitHub →]({repo_url})")

    # Last fetched timestamp
    if st.session_state.github_stats_timestamp:
        last_fetched = datetime.fromtimestamp(st.session_state.github_stats_timestamp).strftime("%Y-%m-%d %H:%M")
        st.sidebar.caption(f"Last fetched at: {last_fetched} (UTC)")
    else:
        st.sidebar.caption("GitHub stats not yet fetched")

    if stars == 0 and forks == 0:
        st.sidebar.caption("GitHub stats may show 0 if unauthenticated or rate-limited. Optionally set GITHUB_TOKEN.")
    
    st.sidebar.markdown("---")
    
    # Query metrics
    st.sidebar.metric("📝 Queries Processed", st.session_state.query_count)
    if st.session_state.insights_history:
        last_insight = st.session_state.insights_history[-1]
        st.sidebar.metric("💬 Last Sentiment", last_insight['sentiment']['sentiment'].title())
        st.sidebar.metric("🏷️ Key Topics", len(last_insight['key_topics']))
    else:
        st.sidebar.metric("💬 Last Sentiment", "—")
        st.sidebar.metric("🏷️ Key Topics", 0)
    
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
        st.markdown("### 📈 Analysis History & Insights")
        
        if st.session_state.insights_history:
            # Summary Statistics
            stats = get_summary_stats(st.session_state.insights_history)
            
            if stats:
                st.markdown("#### 📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Queries", stats['total_queries'])
                
                with col2:
                    st.metric("Avg Confidence", f"{stats['avg_confidence']:.1%}")
                
                with col3:
                    positive_count = stats['sentiments'].get('positive', 0)
                    st.metric("Positive", positive_count)
                
                with col4:
                    st.metric("Unique Topics", stats['unique_topics'])
            
            # Charts
            st.markdown("#### 📉 Visual Analytics")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                sentiment_chart = create_sentiment_distribution_chart(st.session_state.insights_history)
                if sentiment_chart:
                    st.plotly_chart(sentiment_chart, use_container_width=True)
            
            with chart_col2:
                confidence_chart = create_confidence_trend_chart(st.session_state.insights_history)
                if confidence_chart:
                    st.plotly_chart(confidence_chart, use_container_width=True)
            
            # Topics frequency
            topics_chart = create_topics_frequency_chart(st.session_state.insights_history)
            if topics_chart:
                st.plotly_chart(topics_chart, use_container_width=True)

            # Advanced visuals
            st.markdown("#### 📈 Trend & Distribution")
            adv_col1, adv_col2 = st.columns(2)

            with adv_col1:
                timeline_chart = create_sentiment_timeline_chart(st.session_state.insights_history)
                if timeline_chart:
                    st.plotly_chart(timeline_chart, use_container_width=True)

            with adv_col2:
                confidence_dist_chart = create_confidence_distribution_chart(st.session_state.insights_history)
                if confidence_dist_chart:
                    st.plotly_chart(confidence_dist_chart, use_container_width=True)

            treemap_chart = create_topics_treemap(st.session_state.insights_history)
            if treemap_chart:
                st.plotly_chart(treemap_chart, use_container_width=True)
            
            # Export functionality
            st.markdown("#### 💾 Export Data")
            
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                # Convert history to DataFrame for CSV export
                df = pd.DataFrame(st.session_state.insights_history)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"insights_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with export_col2:
                # JSON export
                json_data = json.dumps(st.session_state.insights_history, indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_data,
                    file_name=f"insights_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Detailed History
            st.markdown("#### 📝 Detailed History")
            
            for idx, insight in enumerate(reversed(st.session_state.insights_history)):
                sentiment_label = normalize_sentiment_value(insight.get('sentiment')).title()
                with st.expander(f"Query {len(st.session_state.insights_history) - idx} - {sentiment_label}"):
                    st.markdown(f"**Timestamp:** {insight.get('timestamp', 'N/A')}")
                    st.markdown(f"**Summary:** {insight.get('summary', 'No summary available')}")
                    confidence_val = insight.get('confidence', 0)
                    st.markdown(f"**Confidence:** {confidence_val:.1%}")
                    topics_display = ", ".join(extract_topics(insight))
                    if topics_display:
                        st.markdown(f"**Topics:** {topics_display}")
            
            if st.button("Clear History"):
                st.session_state.insights_history = []
                st.session_state.query_count = 0
                save_session_history()
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
