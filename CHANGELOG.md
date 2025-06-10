# Changelog

All notable changes to the Railway Distance Calculator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.0] - 2025-01-07

### Added
- **Multi-segment journey support** with `-` delimiter (e.g., `PN-JP-PN`)
- **Complete Streamlit web interface** with 3 main tabs
- **Google Maps API integration** for accurate distance calculations
- **RapidAPI integration** for comprehensive station database
- **SQLite caching system** for improved performance
- **Statistics dashboard** with row-based metrics:
  - Total Rows Processed
  - Distance Found
  - Success Rate
- **Built-in station database** with 200+ major Indian railway stations
- **Real-time progress tracking** during file processing
- **Export functionality** for calculated results
- **Error handling** for invalid routes and API failures
- **Rate limiting** to prevent API quota exhaustion

### Features
- Support for Excel (.xlsx, .xls) and CSV file uploads
- Point-to-point and multi-segment journey calculations
- Station code search and lookup
- Method breakdown visualization
- Responsive UI design

### Technical
- **Python 3.7+** compatibility
- **Streamlit 1.45+** web framework
- **Pandas** for data processing
- **Requests** for API communications
- **SQLite3** for local caching

---

## How to Use This Changelog

- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

---

## Future Planned Versions

### [v1.1.0] - Planned
- International railway station support
- Bulk processing improvements
- Enhanced error reporting
- Additional API providers

### [v1.2.0] - Planned  
- Route optimization suggestions
- Historical distance tracking
- Advanced analytics dashboard
- Export format options (PDF, JSON)

### [v2.0.0] - Future
- Machine learning distance predictions
- Real-time train schedule integration
- Multi-language support
- Mobile app companion 