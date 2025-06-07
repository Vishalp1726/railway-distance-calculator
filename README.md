# 🚂 Complete API Railway Calculator

A comprehensive Streamlit application for calculating railway distances and processing journey data with multi-segment route support.

## ✨ Features

### 📄 File Processing
- Upload Excel/CSV files with journey data
- Support for multi-segment journeys (e.g., `PN-JP-PN` for Pune to Jodhpur to Pune)
- Automatic distance calculation for complete journeys
- Export results with detailed breakdowns

### 🔍 Station Search
- Search for railway station codes and names
- Cached station database for faster lookups
- Support for RapidAPI integration for comprehensive station data

### 🧮 Distance Calculator
- **Multi-Segment Journey**: Calculate total distance for complex routes
- **Point-to-Point**: Simple distance between two stations
- Multiple calculation methods (Google Maps API, coordinate-based estimation)

### 📊 Analytics & Statistics
- **Total Rows Processed**: Number of journeys processed
- **Distance Found**: Successful distance calculations
- **Success Rate**: Processing efficiency percentage
- **Method Breakdown**: Visual chart of calculation methods used

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python_scripts
```

2. Install required packages:
```bash
pip install streamlit pandas requests sqlite3
```

3. Run the application:
```bash
streamlit run complete_api_railway_calculator.py
```

### Usage

1. **File Processing**: Upload your Excel/CSV file with "Source & Destination" column
2. **Journey Format**: Use `-` delimiter for multi-segment journeys (e.g., `PN-JP-PN`)
3. **API Configuration**: Add Google Maps and RapidAPI keys for enhanced accuracy
4. **Download Results**: Get comprehensive results with distance calculations

## 📋 Supported Journey Formats

- **Multi-segment**: `PN-JP-PN` (Pune → Jodhpur → Pune)
- **Simple routes**: `PUNE-DELHI` 
- **Station codes**: `SBC-NDLS-SBC`
- **Mixed formats**: `Pune-JP-Mumbai`

## 🔧 API Configuration

### Google Maps API (Recommended)
- Provides accurate rail transit distances
- Free tier: 40,000 requests/month
- Setup: Enable Distance Matrix API in Google Cloud Console

### RapidAPI (Optional)
- Comprehensive Indian Railways station database
- Enhanced station code lookups
- Multiple free plan options available

## 📊 Output Columns

- **Source & Destination**: Original journey input
- **Journey_Segments**: Resolved station codes
- **Total_Distance**: Complete journey distance in km
- **Method**: Calculation method used
- **Journey_Details**: Segment-wise distance breakdown

## 🏛️ Built-in Station Database

Includes 200+ major Indian railway stations with coordinates for offline distance estimation.

## 📈 Statistics Dashboard

- **Processing Metrics**: Total rows, success rate, API usage
- **Method Analytics**: Visual breakdown of calculation methods
- **Quality Control**: Identify problematic routes and station codes

## 🛠️ Technical Features

- **SQLite Caching**: Reduces API calls and improves performance
- **Multi-API Support**: Fallback mechanisms for reliability
- **Error Handling**: Graceful handling of invalid routes
- **Rate Limiting**: Prevents API quota exhaustion
- **Batch Processing**: Efficient handling of large datasets

## 📱 User Interface

- **Clean Design**: Modern Streamlit interface
- **Progress Tracking**: Real-time processing updates
- **Interactive Tabs**: Organized feature sections
- **Responsive Layout**: Works on different screen sizes

## 🔒 Data Privacy

- All processing happens locally
- API keys stored securely in session
- No data transmitted except for API calls
- SQLite cache stored locally

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the built-in help tooltips
2. Review the API setup guide in the sidebar
3. Ensure proper journey format with `-` delimiter
4. Verify API keys are correctly configured

---

**Made with ❤️ for efficient railway journey processing** 