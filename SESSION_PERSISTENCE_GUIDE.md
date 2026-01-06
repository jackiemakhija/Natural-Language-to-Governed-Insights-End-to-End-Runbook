# Session Persistence & Visual Analytics Guide

## Overview
The Natural Language to Governed Insights app now features **persistent session storage** and **comprehensive visual analytics**, making it easy to track and analyze insights over time.

## 🎯 Key Features

### 1. Session Persistence
- **Automatic Save**: Every query is automatically saved to a local JSON file
- **Session Recovery**: Your analysis history is restored when you reopen the app
- **Data Integrity**: Session data persists across app restarts

### 2. Visual Analytics Dashboard

#### Summary Statistics
The History tab now displays key metrics:
- **Total Queries**: Total number of analyses performed
- **Average Confidence**: Mean confidence score across all analyses
- **Positive Count**: Number of positive sentiment results
- **Unique Topics**: Number of distinct topics identified

#### Interactive Charts

**Sentiment Distribution (Pie Chart)**
- Visual breakdown of positive, negative, and neutral sentiments
- Donut chart format for easy interpretation
- Color-coded: Green (positive), Red (negative), Yellow (neutral)

**Confidence Score Trend (Line Chart)**
- Track confidence scores across analyses
- Identify patterns and trends over time
- X-axis: Analysis number, Y-axis: Confidence score (0-1)

**Top 10 Topics (Bar Chart)**
- Most frequently mentioned topics across all analyses
- Horizontal bar chart for easy reading
- Helps identify recurring themes

### 3. Data Export Functionality

**CSV Export**
- Download your analysis history as CSV
- Compatible with Excel, Google Sheets, and data analysis tools
- Includes all fields: timestamp, summary, sentiment, confidence, topics

**JSON Export**
- Download raw JSON data for programmatic access
- Preserves full data structure
- Ideal for custom analysis or integration with other systems

## 📊 How to Use

### Analyzing Text
1. Navigate to the **Analyze** tab
2. Enter your text in the input area
3. Click **Analyze Text**
4. View instant results with sentiment, confidence, and key topics
5. Results are automatically saved to your session history

### Viewing History & Analytics
1. Navigate to the **History** tab
2. View summary statistics at the top
3. Explore interactive charts:
   - Sentiment distribution
   - Confidence trends
   - Topic frequency
4. Expand individual queries for detailed information
5. Use export buttons to download your data

### Exporting Data
1. Go to the **History** tab
2. Click **📥 Download as CSV** for spreadsheet-compatible format
3. Click **📥 Download as JSON** for raw data format
4. Files are timestamped for easy organization

### Clearing History
1. Navigate to the **History** tab
2. Scroll to the bottom
3. Click **Clear History**
4. Confirm to delete all saved data (cannot be undone)

## 🔧 Technical Details

### Session Storage
- **Location**: `session_history.json` in app directory
- **Format**: JSON array of insight objects
- **Auto-Save**: Triggered after each query and when clearing history
- **Auto-Load**: Executed on app initialization

### Data Structure
Each session entry contains:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "summary": "Analysis summary text",
  "sentiment": {
    "sentiment": "positive",
    "confidence_scores": {...}
  },
  "confidence": 0.95,
  "key_topics": ["topic1", "topic2"],
  "recommendations": ["recommendation1", "recommendation2"]
}
```

### Visualization Libraries
- **Plotly**: Interactive, responsive charts
- **Pandas**: Data processing and export
- **Streamlit**: Native metrics and download buttons

## 💡 Best Practices

### For Regular Users
1. **Periodically Export Data**: Download your history for backup
2. **Review Trends**: Check the confidence trend to see analysis quality
3. **Monitor Topics**: Use the topic chart to identify recurring themes
4. **Clear When Needed**: Remove old data to start fresh analyses

### For Developers
1. **Session File Management**: Ensure write permissions for session_history.json
2. **Error Handling**: Check logs if save/load operations fail
3. **Performance**: Session file grows with each query; monitor file size
4. **Backup**: Consider implementing automated backups for production use

## 🚀 New Capabilities

### What's New in This Release
✅ Persistent session storage across app restarts
✅ Visual analytics dashboard with 3 chart types
✅ Summary statistics with key metrics
✅ CSV and JSON export functionality
✅ Enhanced History tab with expandable details
✅ Improved user experience with clear data visualization

### Benefits
- **Data Retention**: Never lose your analysis history
- **Visual Insights**: Understand patterns at a glance
- **Easy Export**: Share or analyze data externally
- **Professional Reporting**: Use charts for presentations
- **Trend Analysis**: Track changes over time

## 📈 Use Cases

### Business Analysis
- Track customer feedback sentiment over time
- Identify trending topics in support tickets
- Monitor confidence levels in automated analysis
- Export data for executive reports

### Research & Development
- Analyze test data across multiple sessions
- Compare sentiment distributions between datasets
- Export results for academic papers
- Track analysis quality metrics

### Quality Assurance
- Monitor sentiment analysis accuracy
- Identify patterns in misclassifications
- Export data for validation studies
- Review historical performance

## 🔒 Privacy & Security

- **Local Storage**: Session data stored locally on your system
- **No Cloud Sync**: Data is not uploaded to external servers
- **Manual Export**: You control when and where to export data
- **Clear Function**: Permanently delete data when needed

## 🆘 Troubleshooting

### Session Not Saving
- **Check Permissions**: Ensure write access to app directory
- **View Logs**: Check Streamlit logs for error messages
- **Disk Space**: Verify sufficient storage available

### Charts Not Displaying
- **Check Data**: Ensure you have at least one analysis in history
- **Browser Compatibility**: Use modern browser (Chrome, Firefox, Edge)
- **Clear Cache**: Refresh the page if charts don't render

### Export Issues
- **Browser Settings**: Check download folder settings
- **File Size**: Large histories may take time to generate
- **Format**: Choose CSV for spreadsheet tools, JSON for code

## 📞 Support

For issues or questions:
- **GitHub**: [Report an issue](https://github.com/jagjeetmakhija/Natural-Language-to-Governed-Insights-End-to-End-Runbook/issues)
- **HuggingFace**: [Visit the Space](https://huggingface.co/spaces/jackiemakhija/Natural-Language-to-Governed-Insights)
- **Documentation**: Check README.md and BUSINESS_USE_CASES.md

---

**Version**: 2.0  
**Last Updated**: January 2025  
**Built with**: Streamlit, Plotly, Pandas, Azure AI Services
