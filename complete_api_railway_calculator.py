import streamlit as st
import pandas as pd
import requests
import time
import sqlite3
import re
from datetime import datetime

st.set_page_config(
    page_title="Complete API Railway Calculator",
    page_icon="🚂",
    layout="wide"
)

class CompleteAPIRailwayCalculator:
    def __init__(self):
        self.api_calls_made = 0
        self.cache_db = "railway_cache.db"
        self.init_cache_db()
        self.init_default_stations()
        
    def init_cache_db(self):
        """Initialize SQLite cache database"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS station_codes (
                code TEXT PRIMARY KEY,
                name TEXT,
                zone TEXT,
                cached_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS distances (
                source TEXT,
                destination TEXT,
                distance INTEGER,
                method TEXT,
                cached_date TEXT,
                PRIMARY KEY (source, destination)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def init_default_stations(self):
        """Initialize with common station codes"""
        default_stations = [
            ("SBC", "BANGALORE CITY", "SW"),
            ("BCT", "MUMBAI CENTRAL", "WR"),
            ("NDLS", "NEW DELHI", "NR"),
            ("MAS", "CHENNAI CENTRAL", "SR"),
            ("HWH", "HOWRAH", "ER"),
            ("SC", "SECUNDERABAD", "SC"),
            ("PUNE", "PUNE", "CR"),
            ("PN", "PUNE", "CR"),  # Common abbreviation
            ("AMD", "AHMEDABAD", "WR"),
            ("JP", "JAIPUR", "NW"),
            ("LKO", "LUCKNOW", "NR"),
            ("BLR", "BANGALORE CITY", "SW"),  # Common abbreviation
            ("DEL", "NEW DELHI", "NR"),  # Common abbreviation
            ("MUM", "MUMBAI CENTRAL", "WR"),  # Common abbreviation
            ("CHN", "CHENNAI CENTRAL", "SR"),  # Common abbreviation
            ("HYD", "SECUNDERABAD", "SC"),  # Common abbreviation
            ("KOL", "HOWRAH", "ER")  # Common abbreviation
        ]
        
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        current_date = datetime.now().isoformat()
        
        for code, name, zone in default_stations:
            cursor.execute('''
                INSERT OR IGNORE INTO station_codes 
                (code, name, zone, cached_date) 
                VALUES (?, ?, ?, ?)
            ''', (code, name, zone, current_date))
        
        conn.commit()
        conn.close()
    
    def search_station_codes(self, query):
        """Search for station codes using RapidAPI"""
        if not query:
            return []
        
        # First check cache
        cached = self.get_cached_stations(query)
        if cached:
            return cached
        
        # Try RapidAPI if key available
        rapidapi_key = st.session_state.get('rapidapi_key', '')
        if rapidapi_key:
            return self.search_via_rapidapi(query, rapidapi_key)
        
        return []
    
    def search_via_rapidapi(self, query, api_key):
        """Search stations using RapidAPI Indian Railways"""
        try:
            url = "https://indianrailways.p.rapidapi.com/findstations.php"
            headers = {
                'x-rapidapi-key': api_key,
                'x-rapidapi-host': 'indianrailways.p.rapidapi.com'
            }
            params = {'station': query}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            self.api_calls_made += 1
            
            if response.status_code == 200:
                data = response.json()
                stations = []
                
                if isinstance(data, dict) and 'stations' in data:
                    for station in data['stations']:
                        stations.append({
                            'code': station.get('station_code', ''),
                            'name': station.get('station_name', ''),
                            'zone': ''
                        })
                
                # Cache results
                if stations:
                    self.cache_stations(stations)
                return stations
                
        except Exception as e:
            st.warning(f"RapidAPI error: {str(e)}")
            
        return []
    
    def cache_stations(self, stations):
        """Cache station results in database"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        current_date = datetime.now().isoformat()
        
        for station in stations:
            cursor.execute('''
                INSERT OR REPLACE INTO station_codes 
                (code, name, zone, cached_date) 
                VALUES (?, ?, ?, ?)
            ''', (station['code'], station['name'], station.get('zone', ''), current_date))
        
        conn.commit()
        conn.close()
    
    def get_cached_stations(self, query=None):
        """Get stations from cache"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        
        if query:
            cursor.execute('''
                SELECT code, name, zone FROM station_codes 
                WHERE code LIKE ? OR name LIKE ?
                ORDER BY name
            ''', (f'%{query.upper()}%', f'%{query.upper()}%'))
        else:
            cursor.execute('SELECT code, name, zone FROM station_codes ORDER BY name')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'code': r[0], 'name': r[1], 'zone': r[2]} for r in results]
    
    def find_station_by_name(self, name):
        """Find best matching station code"""
        if not name:
            return name
        
        name = str(name).strip().upper()
        
        # Check cache for exact match first
        stations = self.get_cached_stations(name)
        
        for station in stations:
            if station['code'] == name or name in station['name'].upper():
                return station['code']
        
        # If no match found, search online
        if st.session_state.get('rapidapi_key'):
            online_stations = self.search_via_rapidapi(name, st.session_state['rapidapi_key'])
            for station in online_stations:
                if station['code'] == name or name in station['name'].upper():
                    return station['code']
        
        # Return original if no match found
        return name
    
    def get_distance_via_api(self, source, destination, api_method='google'):
        """Get distance using various APIs"""
        
        # Check cache first
        cached = self.get_cached_distance(source, destination)
        if cached:
            return cached['distance'], cached['method']
        
        if api_method == 'google' and st.session_state.get('google_api_key'):
            return self.get_google_distance(source, destination)
        else:
            return self.estimate_distance_by_coordinates(source, destination)
    
    def get_google_distance(self, source, destination):
        """Get distance using Google Maps API"""
        api_key = st.session_state.get('google_api_key', '')
        if not api_key:
            return None, "No Google API key"
        
        try:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            params = {
                'origins': f"{source} railway station, India",
                'destinations': f"{destination} railway station, India",
                'mode': 'transit',
                'transit_mode': 'rail',
                'key': api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            self.api_calls_made += 1
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'OK':
                    rows = data.get('rows', [])
                    if rows and rows[0].get('elements'):
                        element = rows[0]['elements'][0]
                        
                        if element.get('status') == 'OK':
                            distance_m = element['distance']['value']
                            distance_km = round(distance_m / 1000)
                            
                            # Cache the result
                            self.cache_distance(source, destination, distance_km, 'Google Maps API')
                            
                            return distance_km, 'Google Maps API'
                        else:
                            # Fallback to estimation if no route found
                            return self.estimate_distance_by_coordinates(source, destination)
                else:
                    return self.estimate_distance_by_coordinates(source, destination)
            else:
                return self.estimate_distance_by_coordinates(source, destination)
                
        except Exception as e:
            return self.estimate_distance_by_coordinates(source, destination)
    
    def estimate_distance_by_coordinates(self, source, destination):
        """Estimate distance using haversine formula with coordinates"""
        coordinates = {
            # Major Metro Cities
            'BANGALORE CITY': (12.9716, 77.5946), 'SBC': (12.9716, 77.5946),
            'MUMBAI CENTRAL': (19.0760, 72.8777), 'BCT': (19.0760, 72.8777),
            'NEW DELHI': (28.6139, 77.2090), 'NDLS': (28.6139, 77.2090),
            'CHENNAI CENTRAL': (13.0827, 80.2707), 'MAS': (13.0827, 80.2707),
            'KOLKATA': (22.5726, 88.3639), 'HOWRAH': (22.5726, 88.3639), 'HWH': (22.5726, 88.3639),
            'HYDERABAD': (17.3850, 78.4867), 'SECUNDERABAD': (17.3850, 78.4867), 'SC': (17.3850, 78.4867),
            'PUNE': (18.5204, 73.8567), 'AHMEDABAD': (23.0225, 72.5714), 'AMD': (23.0225, 72.5714),
            
            # Delhi NCR
            'DELHI SARAI ROHILLA': (28.6517, 77.1917), 'DEE': (28.6517, 77.1917),
            'OLD DELHI': (28.6665, 77.2315), 'DLI': (28.6665, 77.2315),
            'HAZRAT NIZAMUDDIN': (28.5833, 77.2500), 'NZM': (28.5833, 77.2500),
            'ANAND VIHAR': (28.6469, 77.3158), 'ANVT': (28.6469, 77.3158),
            'GHAZIABAD': (28.6692, 77.4538), 'GZB': (28.6692, 77.4538),
            'FARIDABAD': (28.4089, 77.3178), 'FDB': (28.4089, 77.3178),
            'GURGAON': (28.4595, 77.0266), 'GGN': (28.4595, 77.0266),
            
            # Mumbai Suburban
            'CHHATRAPATI SHIVAJI MAHARAJ TERMINUS': (18.9398, 72.8355), 'CSMT': (18.9398, 72.8355),
            'LOKMANYA TILAK TERMINUS': (19.0688, 72.8856), 'LTT': (19.0688, 72.8856),
            'DADAR': (19.0176, 72.8562), 'DR': (19.0176, 72.8562),
            'KURLA': (19.0728, 72.8826), 'LNL': (19.0728, 72.8826),
            'THANE': (19.1972, 72.9581), 'TNA': (19.1972, 72.9581),
            'KALYAN': (19.2437, 73.1631), 'KYN': (19.2437, 73.1631),
            'PANVEL': (18.9894, 73.1106), 'PNVL': (18.9894, 73.1106),
            
            # Maharashtra
            'NASHIK ROAD': (19.9975, 73.7898), 'NK': (19.9975, 73.7898),
            'AURANGABAD': (19.8762, 75.3433), 'AWB': (19.8762, 75.3433),
            'SOLAPUR': (17.6599, 75.9064), 'SUR': (17.6599, 75.9064),
            'KOLHAPUR': (16.7050, 74.2433), 'KOP': (16.7050, 74.2433),
            'NAGPUR': (21.1458, 79.0882), 'NGP': (21.1458, 79.0882),
            'AMRAVATI': (20.9319, 77.7523), 'AMI': (20.9319, 77.7523),
            
            # Gujarat
            'SURAT': (21.1702, 72.8311), 'ST': (21.1702, 72.8311),
            'VADODARA': (22.3072, 73.1812), 'BRC': (22.3072, 73.1812),
            'RAJKOT': (22.3039, 70.8022), 'RJT': (22.3039, 70.8022),
            'BHAVNAGAR': (21.7645, 72.1519), 'BVC': (21.7645, 72.1519),
            'JAMNAGAR': (22.4707, 70.0577), 'JAM': (22.4707, 70.0577),
            'DWARKA': (22.2394, 68.9678), 'DWK': (22.2394, 68.9678),
            
            # Rajasthan
            'JAIPUR': (26.9124, 75.7873), 'JP': (26.9124, 75.7873),
            'JODHPUR': (26.2389, 73.0243), 'JU': (26.2389, 73.0243),
            'UDAIPUR CITY': (24.5854, 73.7125), 'UDZ': (24.5854, 73.7125),
            'AJMER': (26.4499, 74.6399), 'AII': (26.4499, 74.6399),
            'BIKANER': (28.0229, 73.3119), 'BKN': (28.0229, 73.3119),
            'KOTA': (25.2138, 75.8648), 'KOTA': (25.2138, 75.8648),
            
            # Uttar Pradesh
            'LUCKNOW': (26.8467, 80.9462), 'LKO': (26.8467, 80.9462),
            'KANPUR CENTRAL': (26.4499, 80.3319), 'CNB': (26.4499, 80.3319),
            'VARANASI': (25.3176, 82.9739), 'BSB': (25.3176, 82.9739),
            'ALLAHABAD': (25.4358, 81.8463), 'ALD': (25.4358, 81.8463),
            'AGRA CANTT': (27.1767, 78.0081), 'AGC': (27.1767, 78.0081),
            'MATHURA': (27.4924, 77.6737), 'MTJ': (27.4924, 77.6737),
            'GHAZIPUR CITY': (25.5881, 83.5775), 'GCT': (25.5881, 83.5775),
            'GORAKHPUR': (26.7606, 83.3732), 'GKP': (26.7606, 83.3732),
            
            # Bihar
            'PATNA': (25.5941, 85.1376), 'PNBE': (25.5941, 85.1376),
            'GAYA': (24.7914, 85.0002), 'GAYA': (24.7914, 85.0002),
            'MUZAFFARPUR': (26.1197, 85.3910), 'MFP': (26.1197, 85.3910),
            'DARBHANGA': (26.1542, 85.8918), 'DBG': (26.1542, 85.8918),
            'BHAGALPUR': (25.2425, 86.9842), 'BGP': (25.2425, 86.9842),
            
            # West Bengal
            'SEALDAH': (22.5675, 88.3418), 'SDAH': (22.5675, 88.3418),
            'KHARAGPUR': (22.3460, 87.3200), 'KGP': (22.3460, 87.3200),
            'DURGAPUR': (23.4803, 87.3119), 'DGR': (23.4803, 87.3119),
            'ASANSOL': (23.6739, 86.9524), 'ASN': (23.6739, 86.9524),
            'SILIGURI': (26.7271, 88.3953), 'SGUJ': (26.7271, 88.3953),
            'NEW JALPAIGURI': (26.7271, 88.3953), 'NJP': (26.7271, 88.3953),
            
            # Madhya Pradesh
            'BHOPAL': (23.2599, 77.4126), 'BPL': (23.2599, 77.4126),
            'INDORE': (22.7196, 75.8577), 'INDB': (22.7196, 75.8577),
            'JABALPUR': (23.1685, 79.9338), 'JBP': (23.1685, 79.9338),
            'UJJAIN': (23.1765, 75.7885), 'UJN': (23.1765, 75.7885),
            'GWALIOR': (26.2183, 78.1828), 'GWL': (26.2183, 78.1828),
            'RATLAM': (23.3315, 75.0367), 'RTM': (23.3315, 75.0367),
            
            # Chhattisgarh
            'RAIPUR': (21.2514, 81.6296), 'R': (21.2514, 81.6296),
            'BILASPUR': (22.0797, 82.1391), 'BSP': (22.0797, 82.1391),
            'DURG': (21.1901, 81.2849), 'DURG': (21.1901, 81.2849),
            
            # Odisha
            'BHUBANESWAR': (20.2961, 85.8245), 'BBS': (20.2961, 85.8245),
            'CUTTACK': (20.4625, 85.8828), 'CTC': (20.4625, 85.8828),
            'PURI': (19.8135, 85.8312), 'PURI': (19.8135, 85.8312),
            'BERHAMPUR': (19.2823, 84.7941), 'BAM': (19.2823, 84.7941),
            
            # Andhra Pradesh & Telangana
            'VIJAYAWADA': (16.5062, 80.6480), 'BZA': (16.5062, 80.6480),
            'VISAKHAPATNAM': (17.7231, 83.3012), 'VSKP': (17.7231, 83.3012),
            'TIRUPATI': (13.6288, 79.4192), 'TPTY': (13.6288, 79.4192),
            'GUNTUR': (16.3067, 80.4365), 'GNT': (16.3067, 80.4365),
            'NELLORE': (14.4426, 79.9865), 'NLR': (14.4426, 79.9865),
            'RAJAHMUNDRY': (17.0005, 81.8040), 'RJY': (17.0005, 81.8040),
            'WARANGAL': (17.9689, 79.5941), 'WL': (17.9689, 79.5941),
            
            # Tamil Nadu
            'CHENNAI EGMORE': (13.0780, 80.2619), 'MS': (13.0780, 80.2619),
            'COIMBATORE': (11.0168, 76.9558), 'CBE': (11.0168, 76.9558),
            'MADURAI': (9.9252, 78.1198), 'MDU': (9.9252, 78.1198),
            'SALEM': (11.6643, 78.1460), 'SA': (11.6643, 78.1460),
            'TIRUCHIRAPALLI': (10.7905, 78.7047), 'TPJ': (10.7905, 78.7047),
            'TIRUNELVELI': (8.7139, 77.7567), 'TEN': (8.7139, 77.7567),
            'ERODE': (11.3410, 77.7172), 'ED': (11.3410, 77.7172),
            'VELLORE': (12.9165, 79.1325), 'VLR': (12.9165, 79.1325),
            
            # Kerala
            'ERNAKULAM': (9.9312, 76.2673), 'ERS': (9.9312, 76.2673), 'KOCHI': (9.9312, 76.2673),
            'TRIVANDRUM CENTRAL': (8.5241, 76.9366), 'TVC': (8.5241, 76.9366),
            'THRISSUR': (10.5276, 76.2144), 'TCR': (10.5276, 76.2144),
            'KOZHIKODE': (11.2588, 75.7804), 'CLT': (11.2588, 75.7804),
            'KANNUR': (11.8745, 75.3704), 'CAN': (11.8745, 75.3704),
            'KOTTAYAM': (9.5916, 76.5222), 'KTYM': (9.5916, 76.5222),
            'PALAKKAD': (10.7867, 76.6548), 'PGT': (10.7867, 76.6548),
            
            # Karnataka
            'YESVANTPUR': (13.022, 77.5264), 'YPR': (13.0222, 77.5264),
            'MYSORE': (12.3076, 76.6947), 'MYS': (12.3076, 76.6947),
            'HUBLI': (15.3647, 75.1240), 'UBL': (15.3647, 75.1240),
            'MANGALORE CENTRAL': (12.8406, 74.8984), 'MAQ': (12.8406, 74.8984),
            'BELGAUM': (15.8497, 74.4977), 'BGM': (15.8497, 74.4977),
            'GULBARGA': (17.3297, 76.8343), 'GR': (17.3297, 76.8343),
            'DAVANGERE': (14.4644, 75.9218), 'DVG': (14.4644, 75.9218),
            
            # Goa
            'MADGAON': (15.2993, 74.1240), 'MAO': (15.2993, 74.1240), 'GOA': (15.2993, 74.1240),
            'VASCO DA GAMA': (15.3959, 73.8203), 'VSG': (15.3959, 73.8203),
            
            # Punjab & Haryana
            'AMRITSAR': (31.6340, 74.8723), 'ASR': (31.6340, 74.8723),
            'LUDHIANA': (30.9010, 75.8573), 'LDH': (30.9010, 75.8573),
            'JALANDHAR': (31.3260, 75.5762), 'JRC': (31.3260, 75.5762),
            'CHANDIGARH': (30.7333, 76.7794), 'CDG': (30.7333, 76.7794),
            'AMBALA': (30.3782, 76.7767), 'UMB': (30.3782, 76.7767),
            'KURUKSHETRA': (29.9693, 76.8789), 'KKDE': (29.9693, 76.8789),
            
            # Himachal Pradesh & Uttarakhand
            'KALKA': (30.8398, 76.9735), 'KLK': (30.8398, 76.9735),
            'HARIDWAR': (29.9457, 78.1642), 'HW': (29.9457, 78.1642),
            'DEHRADUN': (30.3165, 78.0322), 'DDN': (30.3165, 78.0322),
            
            # Jharkhand
            'RANCHI': (23.3441, 85.3096), 'RNC': (23.3441, 85.3096),
            'DHANBAD': (23.7957, 86.4304), 'DHN': (23.7957, 86.4304),
            'JAMSHEDPUR': (22.8046, 86.2029), 'TATA': (22.8046, 86.2029),
            
            # Northeast States
            'GUWAHATI': (26.1445, 91.7362), 'GHY': (26.1445, 91.7362),
            'DIBRUGARH': (27.4728, 94.9120), 'DBRG': (27.4728, 94.9120),
            'JORHAT': (26.7509, 94.2037), 'JTTN': (26.7509, 94.2037),
            'TINSUKIA': (27.4900, 95.3600), 'NTSK': (27.4900, 95.3600),
            
            # Jammu & Kashmir
            'JAMMU TAWI': (32.7266, 74.8570), 'JAT': (32.7266, 74.8570),
            'UDHAMPUR': (32.9150, 75.1420), 'UHP': (32.9150, 75.1420)
        }
        
        source_coords = coordinates.get(source.upper())
        dest_coords = coordinates.get(destination.upper())
        
        if source_coords and dest_coords:
            distance = self.haversine_distance(source_coords, dest_coords)
            # Rail distance is typically 30% longer than air distance
            rail_distance = int(distance * 1.3)
            
            # Cache the result
            self.cache_distance(source, destination, rail_distance, 'Estimated (Coordinates)')
            
            return rail_distance, 'Estimated (Coordinates)'
        
        return 0, 'No coordinates available'
    
    def haversine_distance(self, coord1, coord2):
        """Calculate distance between two coordinates using haversine formula"""
        import math
        
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Earth's radius in kilometers
        R = 6371
        
        # Convert coordinates to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def cache_distance(self, source, destination, distance, method):
        """Cache distance result in database"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        current_date = datetime.now().isoformat()
        
        # Cache both directions
        for src, dst in [(source, destination), (destination, source)]:
            cursor.execute('''
                INSERT OR REPLACE INTO distances 
                (source, destination, distance, method, cached_date) 
                VALUES (?, ?, ?, ?, ?)
            ''', (src, dst, distance, method, current_date))
        
        conn.commit()
        conn.close()
    
    def get_cached_distance(self, source, destination):
        """Get cached distance"""
        conn = sqlite3.connect(self.cache_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT distance, method FROM distances 
            WHERE source = ? AND destination = ?
        ''', (source, destination))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'distance': result[0], 'method': result[1]}
        return None
    
    def parse_route(self, route_text):
        """Parse journey segments from route text with '-' delimiter"""
        if pd.isna(route_text) or route_text == '':
            return []
        
        text = str(route_text).strip()
        
        # Handle multi-segment journey with '-' delimiter (e.g., "PN-JP-PN")
        if '-' in text:
            segments = [segment.strip() for segment in text.split('-')]
            # Convert station names/codes to proper codes
            resolved_segments = []
            for segment in segments:
                if segment:  # Skip empty segments
                    resolved_code = self.find_station_by_name(segment)
                    resolved_segments.append(resolved_code)
            return resolved_segments
        
        # Fallback to old format for backward compatibility
        parts = re.split(r'\s+TO\s+', text, flags=re.IGNORECASE)
        if len(parts) == 2:
            source = self.find_station_by_name(parts[0])
            destination = self.find_station_by_name(parts[1])
            return [source, destination]
        
        # Single station or unrecognized format
        return [self.find_station_by_name(text)]
    
    def calculate_distance(self, source, destination, api_method='google'):
        """Calculate distance between two stations"""
        if not source or not destination:
            return 0, 'No stations provided'
        
        # Clean and find station codes
        source = self.find_station_by_name(source)
        destination = self.find_station_by_name(destination)
        
        # Get distance via API
        distance, method = self.get_distance_via_api(source, destination, api_method)
        
        return distance or 0, method
    
    def calculate_journey_distance(self, segments, api_method='google'):
        """Calculate total distance for multi-segment journey"""
        if not segments or len(segments) < 2:
            return 0, 'Insufficient segments for journey'
        
        total_distance = 0
        methods_used = []
        journey_details = []
        
        # Calculate distance for each segment of the journey
        for i in range(len(segments) - 1):
            source = segments[i]
            destination = segments[i + 1]
            
            if source and destination:
                distance, method = self.calculate_distance(source, destination, api_method)
                total_distance += distance
                methods_used.append(method)
                journey_details.append(f"{source} to {destination}: {distance} km")
        
        # Determine primary method used
        if methods_used:
            # Use the most common method, or the first one if tied
            primary_method = max(set(methods_used), key=methods_used.count)
        else:
            primary_method = 'No valid segments'
        
        return total_distance, primary_method, journey_details
    
    def process_file_separate_columns(self, df, from_col, to_col, date_col=None, api_method='google'):
        """Process dataframe with separate From and To columns"""
        results = []
        
        progress = st.progress(0)
        status = st.empty()
        total = len(df)
        
        for i, row in df.iterrows():
            progress.progress((i + 1) / total)
            status.text(f"Processing {i+1}/{total} - API calls: {self.api_calls_made}")
            
            # Get source and destination from separate columns
            source_text = str(row[from_col]).strip() if pd.notna(row[from_col]) else ''
            destination_text = str(row[to_col]).strip() if pd.notna(row[to_col]) else ''
            
            # Find station codes
            source = self.find_station_by_name(source_text)
            destination = self.find_station_by_name(destination_text)
            
            # Calculate distance
            distance, method = self.calculate_distance(source, destination, api_method)
            
            result = {
                'Original_From': source_text,
                'Original_To': destination_text,
                'Source_Station': source,
                'Destination_Station': destination,
                'Distance_Travelled': distance,
                'Method': method
            }
            
            if date_col and date_col in row and pd.notna(row[date_col]):
                result['Travel_Date'] = str(row[date_col])
            
            results.append(result)
            
            # Rate limiting for API calls
            if distance > 0 and method == 'Google Maps API':
                time.sleep(0.1)
        
        progress.empty()
        status.empty()
        return pd.DataFrame(results)

    def process_file_single_route(self, df, route_col, date_col=None, api_method='google'):
        """Process dataframe with single route column supporting multi-segment journeys"""
        results = []
        
        progress = st.progress(0)
        status = st.empty()
        total = len(df)
        
        for i, row in df.iterrows():
            progress.progress((i + 1) / total)
            status.text(f"Processing {i+1}/{total} - API calls: {self.api_calls_made}")
            
            route_text = row[route_col]
            segments = self.parse_route(route_text)
            
            if len(segments) >= 2:
                # Multi-segment journey
                total_distance, method, journey_details = self.calculate_journey_distance(segments, api_method)
                
                result = {
                    'Source & Destination': route_text,
                    'Journey_Segments': ' → '.join(segments),
                    'Total_Distance': total_distance,
                    'Method': method,
                    'Journey_Details': ' | '.join(journey_details)
                }
            elif len(segments) == 1:
                # Single station - no journey
                result = {
                    'Source & Destination': route_text,
                    'Journey_Segments': segments[0] if segments else '',
                    'Total_Distance': 0,
                    'Method': 'Single station - no journey',
                    'Journey_Details': 'No journey segments'
                }
            else:
                # No valid segments
                result = {
                    'Source & Destination': route_text,
                    'Journey_Segments': '',
                    'Total_Distance': 0,
                    'Method': 'No valid segments',
                    'Journey_Details': 'Could not parse route'
                }
            
            if date_col and date_col in row and pd.notna(row[date_col]):
                result['Travel_Date'] = str(row[date_col])
            
            results.append(result)
            
            # Rate limiting for API calls
            if result['Total_Distance'] > 0 and method == 'Google Maps API':
                time.sleep(0.1)
        
        progress.empty()
        status.empty()
        return pd.DataFrame(results)

def main():
    st.title("🚂 Complete API Railway Calculator")
    st.markdown("**Get comprehensive railway station codes and distances using APIs**")
    
    calculator = CompleteAPIRailwayCalculator()
    
    # API Configuration Sidebar
    with st.sidebar:
        st.header("🔧 API Configuration")
        
        st.subheader("Google Maps API")
        google_api_key = st.text_input(
            "Google Maps API Key", 
            type="password",
            help="For accurate distance calculations"
        )
        if google_api_key:
            st.session_state['google_api_key'] = google_api_key
        
        st.subheader("RapidAPI")
        rapidapi_key = st.text_input(
            "RapidAPI Key", 
            type="password",
            help="For comprehensive station code lookups"
        )
        if rapidapi_key:
            st.session_state['rapidapi_key'] = rapidapi_key
        
        st.subheader("Settings")
        api_method = st.selectbox(
            "Distance Calculation Method",
            ['google', 'coordinates'],
            help="Choose your preferred method for distance calculation"
        )
        
        st.info(f"API calls made: {calculator.api_calls_made}")
        
        # API Setup Guide
        with st.expander("📋 API Setup Guide"):
            st.markdown("""
            **Google Maps API (Free Tier: 40,000 requests/month):**
            1. Go to [Google Cloud Console](https://console.cloud.google.com/)
            2. Create/select a project
            3. Enable "Distance Matrix API"
            4. Create API key in Credentials
            5. Copy and paste above
            
            **RapidAPI (Free plans available):**
            1. Go to [RapidAPI](https://rapidapi.com/)
            2. Search for "Indian Railways"
            3. Subscribe to free plan
            4. Copy API key
            """)
    
    # Main Content Tabs
    tab1, tab2, tab3 = st.tabs(["📄 File Processing", "🔍 Station Search", "🧮 Distance Calculator"])
    
    with tab1:
        st.subheader("Upload and Process File")
        
        uploaded_file = st.file_uploader(
            "Upload Excel/CSV file with routes",
            type=['xlsx', 'xls', 'csv']
        )
        
        if uploaded_file:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Loaded {len(df)} rows")
                
                # Show preview
                st.subheader("Data Preview")
                st.dataframe(df.head())
                
                # Column selection
                st.subheader("Column Selection")
                col1, col2, col3 = st.columns(3)
                with col1:
                    from_col = st.selectbox("Select 'From' Column", df.columns, 
                                          help="Column containing source station names/codes")
                with col2:
                    to_col = st.selectbox("Select 'To' Column", df.columns,
                                        help="Column containing destination station names/codes")
                with col3:
                    date_col = st.selectbox("Select Date Column (optional)", [None] + list(df.columns),
                                          help="Optional: Travel date column")
                
                # Option for single route column (journey format)
                st.subheader("Alternative: Journey Route Column")
                use_single_route = st.checkbox("Use single journey column instead (format: 'PN-JP-PN' for multi-segment journey)")
                
                if use_single_route:
                    route_col = st.selectbox("Select 'Source & Destination' Column", df.columns,
                                           help="Column with journey segments separated by '-' (e.g., 'PN-JP-PN' for Pune to Jodhpur to Pune)")
                
                if st.button("🚀 Process with API", type="primary"):
                    with st.spinner("Processing with APIs..."):
                        if use_single_route:
                            results_df = calculator.process_file_single_route(df, route_col, date_col, api_method)
                        else:
                            results_df = calculator.process_file_separate_columns(df, from_col, to_col, date_col, api_method)
                    
                    st.success("✅ Processing complete!")
                    
                    # Display results
                    st.subheader("📊 Results")
                    st.dataframe(results_df)
                    
                    # Download button
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results",
                        csv,
                        "railway_distances_api.csv",
                        "text/csv"
                    )
                    
                    # Statistics
                    # Handle both old and new column formats
                    distance_col = 'Total_Distance' if 'Total_Distance' in results_df.columns else 'Distance_Travelled'
                    
                    # Row counting metrics
                    total_rows = len(results_df)
                    distance_found_rows = len(results_df[results_df[distance_col] > 0])
                    success_rate = (distance_found_rows / total_rows * 100) if total_rows > 0 else 0
                    unique_methods = results_df['Method'].value_counts()
                    
                    st.subheader("📈 Statistics")
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Rows Processed", f"{total_rows:,}")
                    with col_b:
                        st.metric("Distance Found", f"{distance_found_rows:,}")
                    with col_c:
                        st.metric("Success Rate", f"{success_rate:.1f}%")
                    
                    # Method breakdown chart
                    if len(unique_methods) > 1:
                        st.subheader("🔍 Method Breakdown")
                        st.bar_chart(unique_methods)
                        
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    with tab2:
        st.subheader("Station Code Search")
        
        search_query = st.text_input("🔍 Search for station (enter station name or code)")
        
        if search_query:
            with st.spinner("Searching stations..."):
                results = calculator.search_station_codes(search_query)
            
            if results:
                st.success(f"Found {len(results)} stations:")
                
                # Create a dataframe for better display
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
                
            else:
                st.warning("❌ No stations found. Try a different search term.")
                st.info("💡 Make sure you have entered your RapidAPI key in the sidebar for online search.")
        
        # Show cached stations
        if st.button("📋 Show All Cached Stations"):
            all_stations = calculator.get_cached_stations()
            if all_stations:
                st.success(f"📊 {len(all_stations)} stations in cache:")
                stations_df = pd.DataFrame(all_stations)
                st.dataframe(stations_df, use_container_width=True)
    
    with tab3:
        st.subheader("Calculate Distance")
        
        # Toggle between single journey and point-to-point
        calc_mode = st.radio(
            "Calculation Mode:",
            ["Point-to-Point", "Multi-Segment Journey"],
            help="Choose between calculating distance between two stations or a complete journey"
        )
        
        if calc_mode == "Point-to-Point":
            col1, col2 = st.columns(2)
            
            with col1:
                source = st.text_input("🚉 Source Station (name or code)")
            with col2:
                destination = st.text_input("🏁 Destination Station (name or code)")
            
            if st.button("🧮 Calculate Distance", type="primary"):
                if source and destination:
                    with st.spinner("Calculating distance..."):
                        distance, method = calculator.calculate_distance(source, destination, api_method)
                    
                    if distance:
                        st.success(f"✅ **Distance:** {distance} km")
                        st.info(f"📊 **Method:** {method}")
                        
                        # Show resolved station codes
                        col_a, col_b = st.columns(2)
                        with col_a:
                            resolved_source = calculator.find_station_by_name(source)
                            st.write(f"**Source:** {resolved_source}")
                        with col_b:
                            resolved_dest = calculator.find_station_by_name(destination)
                            st.write(f"**Destination:** {resolved_dest}")
                    else:
                        st.error("❌ Could not calculate distance")
                        st.info("💡 Try entering different station names or check your API keys.")
                else:
                    st.warning("⚠️ Please enter both source and destination stations")
        
        else:  # Multi-Segment Journey
            journey_input = st.text_input(
                "🛤️ Journey Route (use '-' to separate stations)",
                placeholder="e.g., PN-JP-PN for Pune to Jodhpur to Pune",
                help="Enter station codes or names separated by '-' for multi-segment journey"
            )
            
            if st.button("🧮 Calculate Journey Distance", type="primary"):
                if journey_input:
                    with st.spinner("Calculating journey distance..."):
                        segments = calculator.parse_route(journey_input)
                        
                        if len(segments) >= 2:
                            total_distance, method, journey_details = calculator.calculate_journey_distance(segments, api_method)
                            
                            if total_distance:
                                st.success(f"✅ **Total Journey Distance:** {total_distance} km")
                                st.info(f"📊 **Primary Method:** {method}")
                                
                                # Show journey breakdown
                                st.subheader("🛤️ Journey Breakdown:")
                                st.write(f"**Route:** {' → '.join(segments)}")
                                
                                for detail in journey_details:
                                    st.write(f"• {detail}")
                            else:
                                st.error("❌ Could not calculate journey distance")
                        else:
                            st.warning("⚠️ Please enter at least 2 stations for a journey")
                else:
                    st.warning("⚠️ Please enter a journey route")

if __name__ == "__main__":
    main() 