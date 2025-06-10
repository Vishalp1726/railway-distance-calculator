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
        """Initialize with comprehensive station codes"""
        default_stations = [
            # Major Cities (Original)
            ("SBC", "BANGALORE CITY", "SW"),
            ("BCT", "MUMBAI CENTRAL", "WR"),
            ("NDLS", "NEW DELHI", "NR"),
            ("MAS", "CHENNAI CENTRAL", "SR"),
            ("HWH", "HOWRAH", "ER"),
            ("SC", "SECUNDERABAD", "SC"),
            ("PUNE", "PUNE JUNCTION RAILWAY STATION", "CR"),
            ("PN", "PUNE", "CR"),
            ("AMD", "AHMEDABAD", "WR"),
            ("JP", "JAIPUR", "NW"),
            ("LKO", "LUCKNOW", "NR"),
            ("BLR", "BANGALORE CITY", "SW"),
            ("DEL", "NEW DELHI", "NR"),
            ("MUM", "MUMBAI CENTRAL", "WR"),
            ("CHN", "CHENNAI CENTRAL", "SR"),
            ("HYD", "SECUNDERABAD", "SC"),
            ("KOL", "HOWRAH", "ER"),
            
            # Comprehensive Station Mappings
            ("HYB", "HYDERABAD DECCAN RAILWAY STATION", "SC"),
            ("SCL", "SILCHAR", "NFR"),
            ("DMV", "DIMAPUR RAILWAY STATION", "NFR"),
            ("NBQ", "NEW BONGAIGAON JUNCTION", "NFR"),
            ("CNGR", "CHENGANNUR", "SR"),
            ("OGL", "ONGOLE", "SCR"),
            ("SGNR", "SHRI GANGA NAGAR CHORAHA", "NWR"),
            ("BTI", "BATHINDA JUNCTION", "NR"),
            ("KOJ", "KOKRAJHAR", "NFR"),
            ("SGAC", "SOGARIA (KOTA)", "WCR"),
            ("JJKR", "JAJPUR KEONJHAR ROAD", "ECoR"),
            ("DEE", "DELHI SARAI ROHILLA", "NR"),
            ("MAJN", "MANGALORE JUNCTION", "KR"),
            ("BKSC", "BOKARO STEEL CITY", "ECR"),
            ("NOQ", "NEW ALIPURDUAR", "NFR"),
            ("VSKC", "VISAKHAPATNAM RAILWAY STATION", "ECoR"),
            ("ROU", "ROURKELA JUNCTION", "ECoR"),
            ("DEC", "DELHI CANTONMENT", "NR"),
            ("NLS", "NELLORE SOUTH RAILWAY STATION", "SCR"),
            ("KLBG", "KALABURAGI", "SWR"),
            ("JMU", "JAMUI", "ECR"),
            ("RKMP", "HABIBGANJ RAILWAY STATION", "WCR"),
            ("SGR", "SANGAMESHWAR RAILWAY STATION", "KR"),
            ("SRR", "SHORANUR JUNCTION", "SR"),
            ("ALLP", "ALAPPUZHA (ALLEPPEY)", "SR"),
            ("KCVL", "THIRUVANANTHAPURAM NORTH (KOCHUVELI)", "SR"),
            ("MANLI", "JOGINDER NAGAR", "NR"),
            ("PRNC", "PURNIA COURT", "NFR"),
            ("KGQ", "KASARAGOD RAILWAY STATION", "SR"),
            ("MMCT", "MUMBAI CENTRAL", "WR"),
            ("KQG", "KOLAGALLU RAILWAY STATION", "SCR"),
            ("MLDT", "MALDA TOWN RAILWAY STATION", "NFR"),
            ("BRPD", "BARPETA ROAD", "NFR"),
            ("LJN", "LUCKNOW JUNCTION", "NER"),
            ("RJBP", "RAJENDRANAGAR TERMINAL", "ECR"),
            ("LTT", "LOKMANYA TILAK TERMINUS RAILWAY STATION", "CR"),
            ("SBP", "SAMBALPUR JUNCTION", "ECoR"),
            ("MZS", "MURKONGSELEK", "NFR"),
            ("SRTL", "CHERTHALA (SHERTHALAI) RAILWAY STATION", "SR"),
            ("AGTL", "AGARTALA RAILWAY STATION", "NFR"),
            ("AGRL", "AGRA CANTT", "NCR"),
            ("SMVB", "SATYAMANGALA", "SR"),
            ("LLT", "LALITPUR", "NCR"),
            ("AADR", "AADRASH NAGAR", "WR"),
            ("LPI", "LIPI", "ER"),
            ("KUN", "KUNDAPURA", "KR"),
            ("GHHY", "GUNDICHAPURAM", "SR"),
            ("BKMI", "BANKIM NAGAR", "ER"),
            ("ADI", "AHMEDABAD", "WR"),
            ("NKP", "NARKATIAGANJ", "NER"),
            ("RPJ", "RAJPURA", "NR"),
            ("HTE", "HATIA", "SER"),
            ("GGN", "GURGAON", "NR"),
            ("TDL", "TINDHARIA", "NFR"),
            ("PER", "PERUNGUDI", "SR"),
            ("NHLN", "NAHLAIN", "WR"),
            ("THE", "THEOG", "NR"),
            ("NCB", "NADIAD", "WR"),
            ("NSTK", "NSTK", "NFR"),
            ("GGVT", "GAYA JUNCTION", "ECR"),
            ("KOAA", "KOLKATA", "ER"),
            ("WH", "WADI", "SCR"),
            ("QLN", "QUILON", "SR"),
            ("BMKI", "BIHAR", "ECR"),
            
            # Additional mappings for variations
            ("O NZM", "HAZRAT NIZAMUDDIN", "NR"),
            ("MLLDT", "MALDA TOWN", "NFR"),
            
            # Comprehensive station mappings from your list
            ("ASR", "AMRITSAR JUNCTION", "NR"),
            ("CDG", "CHANDIGARH", "NR"),
            ("BBS", "BHUBANESWAR", "ECoR"),
            ("NDLS", "NEW DELHI", "NR"),
            ("PNBE", "PATNA JUNCTION", "ECR"),
            ("UDZ", "UDAIPUR CITY", "NWR"),
            ("NJP", "NEW JALPAIGURI", "NFR"),
            ("BZA", "VIJAYAWADA JUNCTION", "SCR"),
            ("MAO", "MADGAON", "KR"),
            ("GHY", "GUWAHATI", "NFR"),
            ("HWH", "HOWRAH JUNCTION", "ER"),
            ("VSKP", "VISAKHAPATNAM", "ECoR"),
            ("NLR", "NELLORE", "SCR"),
            ("R", "RAIPUR JUNCTION", "SECR"),
            ("DBRG", "DIBRUGARH TOWN", "NFR"),
            ("RNC", "RANCHI", "SER"),
            ("GGN", "GURUGRAM", "NR"),
            ("SBC", "BANGALORE CITY", "SWR"),
            ("SC", "SECUNDERABAD JUNCTION", "SCR"),
            ("GNT", "GUNTUR JUNCTION", "SCR"),
            ("MAS", "CHENNAI CENTRAL", "SR"),
            ("JRC", "JALANDHAR CITY", "NR"),
            ("JU", "JODHPUR JUNCTION", "NWR"),
            ("GWL", "GWALIOR", "NCR"),
            ("TNA", "THANE", "CR"),
            ("CAN", "KANNUR", "SR"),
            ("ERN", "ERNAKULAM JUNCTION", "SR"),
            ("JBP", "JABALPUR", "WCR"),
            ("SDAH", "SEALDAH", "ER"),
            ("KUR", "KHURDA ROAD JUNCTION", "ECoR"),
            ("ERS", "ERNAKULAM TOWN", "SR"),
            ("NZM", "HAZRAT NIZAMUDDIN", "NR"),
            ("CSMT", "MUMBAI CST", "CR"),
            ("DHN", "DHANBAD JUNCTION", "ECR"),
            ("YPR", "YESVANTPUR JUNCTION", "SWR"),
            ("PUNE", "PUNE JUNCTION", "CR"),
            ("BAM", "BRAHMAPUR", "ECoR"),
            ("JAB", "YAMUNA BRIDGE AGRA", "NCR"),
            ("JAM", "JAMNAGAR", "WR"),
            ("RJY", "RAJAHMUNDRY", "ECoR"),
            ("PGT", "PURULIA JUNCTION", "SER"),
            ("BSB", "VARANASI JUNCTION", "NER"),
            ("TATA", "TATANAGAR JUNCTION", "SER"),
            ("BGP", "BHAGALPUR", "ECR"),
            ("CNB", "KANPUR CENTRAL", "NCR"),
            ("GKP", "GORAKHPUR JUNCTION", "NER"),
            ("ST", "SURAT", "WR"),
            ("KTYM", "KOTTAYAM", "SR"),
            ("MAQ", "MANGALORE CENTRAL", "KR"),
            ("CLT", "KOLLAM JUNCTION", "SR"),
            ("TVC", "TRIVANDRUM CENTRAL", "SR"),
            ("DDN", "DEHRADUN", "NR"),
            ("JAT", "JAMMU TAWI", "NR"),
            ("INDB", "INDORE JUNCTION", "WCR"),
            ("BKMI", "BIKANER JUNCTION", "NWR"),
            ("NKP", "NARKATIAGANJ JUNCTION", "NER"),
            ("HW", "HARIDWAR JUNCTION", "NR"),
            ("SCB", "SAMBALPUR", "ECoR"),
            ("ET", "ITARSI JUNCTION", "WCR"),
            ("DBRT", "DIBRUGARH TOWN", "NFR"),
            ("DPJ", "DARJEELING", "NFR"),
            ("VSG", "VASCO DA GAMA", "KR"),
            ("HX", "HASSAN JUNCTION", "SWR"),
            ("Vapi", "VAPI", "WR"),
            ("HADS", "HATHRAS CITY", "NCR"),
            ("YNK", "YAMUNANAGAR", "NR"),
            ("KYTM", "KOTTAYAM", "SR"),
            ("KCG", "HYDERABAD KACHEGUDA", "SCR"),
            ("JSG", "JHARSUGUDA JUNCTION", "ECoR"),
            ("SHM", "SHALIMAR", "ER"),
            ("DWX", "DEWAS JUNCTION", "WCR"),
            ("SPJ", "SITAPUR JUNCTION", "NER"),
            ("CWA", "CHHIWARA", "WCR"),
            ("NSK", "NASHIK ROAD", "CR"),
            ("CTP", "CUTTACK", "ECoR"),
            ("JDB", "JAGADABANDHAN", "ER"),
            ("ATP", "ANANTAPUR", "SCR"),
            ("MTJ", "MATHURA JUNCTION", "NCR"),
            ("USL", "USLAPUR", "SCR"),
            ("LDH", "LUDHIANA JUNCTION", "NR"),
            ("BGM", "BELAGAVI", "SWR"),
            ("PRYJ", "PRAYAGRAJ JUNCTION", "NCR"),
            ("UD", "UDHAMPUR", "NR"),
            ("TIR", "TIRUPUR", "SR"),
            ("TCR", "THRISSUR", "SR"),
            ("CTC", "CUTTACK", "ECoR"),
            ("BPL", "BHOPAL JUNCTION", "WCR"),
            ("UBL", "HUBLI JUNCTION", "SWR"),
            ("BLS", "BALASORE", "ECoR"),
            ("PURI", "PURI", "ECoR"),
            ("BSP", "BILASPUR JUNCTION", "SECR"),
            ("AII", "AJMER JUNCTION", "NWR"),
            ("MRJ", "MIRAJ JUNCTION", "CR"),
            ("UHL", "UNHA", "NR"),
            ("UMB", "AMBALA CANTONMENT", "NR"),
            ("PRR", "PURULIA JUNCTION", "SER"),
            ("PGW", "PHAGWARA JUNCTION", "NR"),
            ("KOTA", "KOTA JUNCTION", "WCR"),
            ("MLDT", "MALDA TOWN", "NFR"),
            ("HTE", "HATIA", "SER"),
            ("MTM", "MACHILIPATNAM", "SCR"),
            ("HYD", "HYDERABAD DECCAN", "SCR"),
            ("BE", "BHARUCH JUNCTION", "WR"),
            ("ABR", "ABU ROAD", "NWR"),
            ("LKR", "LUCKNOW", "NR"),
            ("MANALI", "MANALI", "NR"),
            ("PPTA", "PATLIPUTRA JUNCTION", "ECR"),
            ("NTSK", "NEW TINSUKIA JUNCTION", "NFR"),
            ("BPC", "BERHAMPORE COURT", "ER"),
            ("BVI", "BORIVALI", "WR"),
            ("AWT", "ALWAR JUNCTION", "NWR"),
            ("BRC", "VADODARA JUNCTION", "WR"),
            ("RPAN", "RANGAPAN", "NFR"),
            ("VG", "VIRAMGAM JUNCTION", "WR"),
            ("BSR", "VASAI ROAD", "WR"),
            ("KAWR", "KARWAR", "KR"),
            ("ASH", "AISHBAGH", "NER"),
            ("MLPN", "MAHESHMUNDA", "ECR"),
            ("AGC", "AGRA CANTONMENT", "NCR"),
            ("PNE", "PUNE", "CR"),
            ("DGHA", "DIGHA", "SER"),
            ("KYN", "KALYAN JUNCTION", "CR"),
            ("NITR", "NITTUR", "SWR"),
            ("CKP", "CHAKRADHARPUR", "SER"),
            ("KLK", "KALKA", "NR"),
            ("NNDLS", "NEW DELHI", "NR"),
            ("MYS", "MYSORE JUNCTION", "SWR"),
            ("GZB", "GHAZIABAD", "NR"),
            ("MB", "MORADABAD JUNCTION", "NR"),
            ("NK", "NASIK ROAD", "CR"),
            ("MMR", "MANMAD JUNCTION", "CR"),
            ("AY", "AYODHYA JUNCTION", "NR"),
            ("AYC", "AYODHYA CANTT", "NR"),
            ("GBZ", "GHAZIABAD", "NR"),
            ("NE", "NERAL", "CR"),
            ("TPT", "TIRUPATI", "SCR"),
            ("Kurnool", "KURNOOL CITY", "SCR"),
            ("CNAN", "CHENGANNUR", "SR"),
            ("RTDL", "RATANGARH", "NWR"),
            ("CPK", "CHAPRA JUNCTION", "ECR"),
            ("JSGR", "JHARSUGUDA", "ECoR"),
            ("VLI", "VELLORE CANTONMENT", "SR"),
            ("DDU", "PANDIT DEEN DAYAL UPADHYAYA JUNCTION", "NCR"),
            ("DURG", "DURG JUNCTION", "SECR"),
            ("KYQ", "KAMAKHYA JUNCTION", "NFR"),
            ("BJP", "BIJAPUR", "SWR"),
            ("BAY", "BALLARI JUNCTION", "SWR"),
            ("MBNR", "MAHBUBNAGAR", "SCR"),
            ("KYJ", "KAYAMKULAM JUNCTION", "SR"),
            ("KZJ", "KAZIPET JUNCTION", "SCR"),
            ("PNVL", "PANVEL JUNCTION", "CR"),
            ("JUC", "JALANDHAR CANTONMENT", "NR"),
            ("BvRM", "BHAVNAGAR TERMINUS", "WR"),
            ("FK", "FARIDKOT", "NR"),
            ("NZB", "NIZAMABAD JUNCTION", "SCR"),
            ("BPB", "BADARPUR JUNCTION", "NFR"),
            ("NDLLS", "NEW DELHI", "NR"),
            ("BGS", "BEGU SARAI", "ECR"),
            ("HAD", "HALDWANI", "NR"),
            ("MCA", "MACHILIPATNAM", "SCR"),
            ("KDR", "KANDHAR", "WCR"),
            ("KGP", "KHARAGPUR JUNCTION", "SER"),
            ("KIR", "KATIHAR JUNCTION", "NFR"),
            ("NMZ", "NEW MIRZAPUR", "NCR"),
            ("GAYA", "GAYA JUNCTION", "ECR"),
            ("AJ", "AJGAIN", "NR"),
            ("TRC", "THIRUVARUR JUNCTION", "SR"),
            ("JSME", "JASIDIH JUNCTION", "ECR"),
            ("JYP", "JEYPORE", "ECoR"),
            ("BKN", "BIKANER JUNCTION", "NWR"),
            ("HHW", "HARIDWAR JUNCTION", "NR"),
            ("KOP", "KOLHAPUR CSMT", "CR"),
            ("SMET", "SRIKAKULAM ROAD", "ECoR"),
            ("HAS", "HASSAN JUNCTION", "SWR"),
            ("AWB", "AURANGABAD", "CR"),
            ("NDL", "NANDYAL JUNCTION", "SCR"),
            ("TVCN", "TIRUVOTTIYUR", "SR"),
            ("JHS", "JHANSI JUNCTION", "NCR"),
            ("PTKC", "PATHANKOT CANTONMENT", "NR"),
            ("TBM", "TAMBARAM", "SR"),
            ("KXCG", "KACHEGUDA", "SCR"),
            ("SV", "SIWAN JUNCTION", "ECR"),
            ("DDR", "DAUND JUNCTION", "CR"),
            ("TPTY", "TIRUPTI", "SCR"),
            ("PRNA", "PURNEA JUNCTION", "NFR"),
            ("DR", "DADAR", "CR"),
            ("SUR", "SOLAPUR JUNCTION", "CR"),
            ("BLJK", "BHALUKJUNG", "NFR"),
            ("DHM", "DHAMARA GHAT", "ER"),
            ("SLO", "SAMALKOT JUNCTION", "ECoR"),
            ("MLDYT", "MALDA TOWN", "NFR"),
            ("MCI", "MANCHERIAL", "SCR"),
            
            # Common variations
            ("KOCHI", "ERNAKULAM", "SR"),
            ("JAMMU", "JAMMU TAWI", "NR"),
            ("KOLKATA", "HOWRAH", "ER"),
            ("CHANDIGARH", "CHANDIGARH", "NR"),
            ("SINGRAULI", "SINGRAULI", "ECR"),
            ("SHOLAVANDAN", "SHOLAVANDAN", "SR"),
            ("SRIGANGANAGAR", "SHRI GANGA NAGAR", "NWR"),
            ("BHATINDA", "BATHINDA JUNCTION", "NR"),
            ("MAJHERHAT", "MAJHERHAT", "ER"),
            ("MANALI", "MANALI", "NR"),
            ("ANGUL", "ANGUL", "ECoR"),
            ("BIHAR SHARIF", "BIHAR SHARIF", "ECR"),
            ("SABARMATI", "SABARMATI", "WR"),
            ("SURTANJI", "SURTANJI", "NFR"),
            ("DUMKA", "DUMKA", "ECR"),
            ("OLD NIZAMUDDIN", "HAZRAT NIZAMUDDIN", "NR"),
            ("Bhuntar", "BHUNTAR", "NR"),
            ("Goa", "MADGAON", "KR"),
            ("MLDR", "MALADHAR", "WR"),
            ("KRNT", "KURNOOL CITY", "SCR"),
            ("STA", "SATNA", "WCR"),
            ("KGI", "KALGACCHI", "ER"),
            ("LMG", "LAMJUNG", "NFR"),
            ("ANGL", "ANGUL", "ECoR"),
            ("KTU", "KOTTURU", "SR"),
            ("HZBN", "HUZURABAD", "SCR"),
            ("VGLJ", "VAIGAI", "SR"),
            ("KAWRA", "KARWAR", "KR"),
            ("SRE", "SAHARANPUR JUNCTION", "NR"),
            ("EE", "ELURU", "SCR"),
            ("KARWAR", "KARWAR", "KR"),
            ("HPT", "HOSAPETE JUNCTION", "SWR"),
            ("WL", "WARANGAL", "SCR"),
            ("NZZM", "HAZRAT NIZAMUDDIN", "NR"),
            ("KRWA", "KIRWALI", "NR"),
            ("MAY", "MAYILADUTHURAI JUNCTION", "SR"),
            ("CPT", "TIRUCHCHIRAPPALLI JUNCTION", "SR"),
            ("DRU", "KADUR JUNCTION", "SWR"),
            ("SDMV", "SIDHPUR", "WR"),
            ("LTTT", "LOKMANYA TILAK TERMINUS", "CR"),
            ("SINI", "SINI JUNCTION", "SER"),
            ("SRTYL", "SERTOLI", "KR"),
            ("UJN", "UJJAIN JUNCTION", "WCR"),
            ("BDTS", "BANDRA TERMINUS", "WR"),
            ("gGKP", "GORAKHPUR JUNCTION", "NER"),
            ("BWN", "BARDWAN JUNCTION", "ER"),
            ("HUBL", "HUBLI JUNCTION", "SWR"),
            ("BHP", "BERHAMPORE COURT", "ER"),
            ("KBLG", "KALABURAGI", "SWR"),
            ("RJPB", "RAJENDRA NAGAR", "ECR")
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
    
    def get_distance_via_api(self, source, destination):
        """Get distance using Google Maps API only"""
        
        # Check cache first
        cached = self.get_cached_distance(source, destination)
        if cached:
            return cached['distance'], cached['method']
        
        # Always use Google API (hardcoded key)
        return self.get_google_distance(source, destination)
    
    def get_google_distance(self, source, destination):
        """Get distance using Google Maps API with hardcoded key"""
        # Hardcoded Google API key
        api_key = "AIzaSyB4X9GmjJBnW4iqXQ3Q6uXcFUyy0ZeS8-o"
        
        try:
            url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            params = {
                'origins': f"{source} railway station, India",
                'destinations': f"{destination} railway station, India",
                'mode': 'transit',
                'transit_mode': 'train',
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
                            # No route found - return 0
                            return 0, 'Google API: No route found'
                else:
                    return 0, f'Google API error: {data.get("status", "Unknown")}'
            else:
                return 0, f'Google API HTTP error: {response.status_code}'
                
        except Exception as e:
            return 0, f'Google API exception: {str(e)}'

    
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
    
    def calculate_distance(self, source, destination):
        """Calculate distance between two stations"""
        if not source or not destination:
            return 0, 'No stations provided'
        
        # Clean and find station codes
        source = self.find_station_by_name(source)
        destination = self.find_station_by_name(destination)
        
        # Get distance via Google API
        distance, method = self.get_distance_via_api(source, destination)
        
        return distance or 0, method
    
    def calculate_journey_distance(self, segments):
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
                distance, method = self.calculate_distance(source, destination)
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
    
    def process_file_separate_columns(self, df, from_col, to_col, date_col=None):
        """Process dataframe with separate From and To columns"""
        results = []
        
        progress = st.progress(0)
        status = st.empty()
        cancel_placeholder = st.empty()
        total = len(df)
        
        for i, row in df.iterrows():
            # Check for cancellation
            if st.session_state.get('processing_cancelled', False):
                status.warning(f"⚠️ Processing cancelled at row {i+1}/{total}")
                break
                
            progress.progress((i + 1) / total)
            status.text(f"Processing {i+1}/{total} - API calls: {self.api_calls_made}")
            
            # Show cancel button
            with cancel_placeholder.container():
                if st.button("❌ Cancel Processing", key=f"cancel_sep_{i}", type="secondary"):
                    st.session_state.processing_cancelled = True
                    st.warning("⏹️ Processing cancellation requested...")
                    break
            
            # Get source and destination from separate columns
            source_text = str(row[from_col]).strip() if pd.notna(row[from_col]) else ''
            destination_text = str(row[to_col]).strip() if pd.notna(row[to_col]) else ''
            
            # Find station codes
            source = self.find_station_by_name(source_text)
            destination = self.find_station_by_name(destination_text)
            
            # Calculate distance using Google API
            distance, method = self.calculate_distance(source, destination)
            
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
        cancel_placeholder.empty()
        return pd.DataFrame(results)

    def process_file_single_route(self, df, route_col, date_col=None):
        """Process dataframe with single route column supporting multi-segment journeys"""
        results = []
        
        progress = st.progress(0)
        status = st.empty()
        cancel_placeholder = st.empty()
        total = len(df)
        
        for i, row in df.iterrows():
            # Check for cancellation
            if st.session_state.get('processing_cancelled', False):
                status.warning(f"⚠️ Processing cancelled at row {i+1}/{total}")
                break
                
            progress.progress((i + 1) / total)
            status.text(f"Processing {i+1}/{total} - API calls: {self.api_calls_made}")
            
            # Show cancel button
            with cancel_placeholder.container():
                if st.button("❌ Cancel Processing", key=f"cancel_single_{i}", type="secondary"):
                    st.session_state.processing_cancelled = True
                    st.warning("⏹️ Processing cancellation requested...")
                    break
            
            route_text = row[route_col]
            segments = self.parse_route(route_text)
            
            if len(segments) >= 2:
                # Multi-segment journey
                total_distance, method, journey_details = self.calculate_journey_distance(segments)
                
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
        cancel_placeholder.empty()
        return pd.DataFrame(results)

def main():
    st.title("🚂 Complete API Railway Calculator")
    st.markdown("**Get comprehensive railway station codes and distances using APIs**")
    
    calculator = CompleteAPIRailwayCalculator()
    
    # API Status Sidebar
    with st.sidebar:
        st.header("🔧 API Status")
        
        st.success("✅ Google Maps API: Configured")
        st.info("🔑 Using hardcoded Google API key")
        st.info("🚂 Distance calculation: Google Maps only")
        st.info(f"📊 API calls made: {calculator.api_calls_made}")
        
        st.subheader("RapidAPI (Optional)")
        rapidapi_key = st.text_input(
            "RapidAPI Key", 
            type="password",
            help="Optional: For enhanced station code lookups"
        )
        if rapidapi_key:
            st.session_state['rapidapi_key'] = rapidapi_key
            st.success("✅ RapidAPI: Connected")
        else:
            st.warning("⚠️ RapidAPI: Not configured (station search limited)")
        
        # API Info
        with st.expander("ℹ️ API Information"):
            st.markdown("""
            **Google Maps API:**
            - ✅ Pre-configured with hardcoded key
            - 🎯 Always used for distance calculations
            - 🚫 No coordinate-based fallback
            
            **RapidAPI (Optional):**
            - 🔍 Enhanced station code search
            - 📋 Get your key from [RapidAPI](https://rapidapi.com/)
            - 🆓 Free plans available
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
                    # Initialize processing cancellation state
                    st.session_state.processing_cancelled = False
                    
                    with st.spinner("Processing with Google Maps API..."):
                        if use_single_route:
                            results_df = calculator.process_file_single_route(df, route_col, date_col)
                        else:
                            results_df = calculator.process_file_separate_columns(df, from_col, to_col, date_col)
                        
                        # Check if processing was cancelled
                        if st.session_state.get('processing_cancelled', False):
                            st.warning("⚠️ Processing was cancelled! Showing partial results.")
                            st.info(f"📊 Processed {len(results_df)} out of {len(df)} total rows")
                        else:
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
                    with st.spinner("Calculating distance with Google Maps API..."):
                        distance, method = calculator.calculate_distance(source, destination)
                    
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
                    with st.spinner("Calculating journey distance with Google Maps API..."):
                        segments = calculator.parse_route(journey_input)
                        
                        if len(segments) >= 2:
                            total_distance, method, journey_details = calculator.calculate_journey_distance(segments)
                            
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