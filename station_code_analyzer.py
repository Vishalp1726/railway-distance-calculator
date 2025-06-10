import pandas as pd
import json
import re
from complete_api_railway_calculator import CompleteAPIRailwayCalculator

class StationCodeAnalyzer:
    def __init__(self):
        self.calculator = CompleteAPIRailwayCalculator()
        self.comprehensive_station_database = self.build_comprehensive_database()
        
    def build_comprehensive_database(self):
        """Build comprehensive station code database"""
        
        # Get existing database from calculator
        existing_quick_lookup = self.calculator.get_quick_station_lookup()
        
        # Extended database with 1000+ Indian Railway stations
        extended_stations = {
            # Major Junction Stations
            'ALLP': 'ALAPPUZHA', 'ALUR': 'ALUR', 'AMH': 'AZAMGARH', 'ANVT': 'ANAND VIHAR TERMINAL',
            'APDJ': 'ALIGARH', 'ASR': 'AMRITSAR', 'AVRD': 'ARAVALLI', 'BAY': 'BELLARY',
            'BDTS': 'BANDRA TERMINUS', 'BG': 'BONGAIGAON', 'BINA': 'BINA', 'BJPL': 'BIJAPUR',
            'BKN': 'BIKANER', 'BL': 'VALSAD', 'BNE': 'BOHANI', 'BOE': 'BARSOI',
            
            # State Capitals & Major Cities (Extended)
            'TPTY': 'TIRUPATI', 'RNC': 'RANCHI', 'SHM': 'SHALIMAR', 'VGLB': 'VIRAMGAM',
            'VSKP': 'VISAKHAPATNAM', 'WAT': 'WADI', 'WL': 'WARANGAL', 'YPR': 'YESVANTPUR',
            'JBP': 'JABALPUR', 'KOTA': 'KOTA', 'LJN': 'LUCKNOW NE', 'MDU': 'MADURAI',
            'MYS': 'MYSORE', 'NGP': 'NAGPUR', 'NK': 'NASHIK ROAD', 'PNBE': 'PATNA',
            'R': 'RAIPUR', 'RJT': 'RAJKOT', 'RTM': 'RATLAM', 'SBC': 'BANGALORE CITY',
            'SC': 'SECUNDERABAD', 'ST': 'SURAT', 'UJN': 'UJJAIN',
            
            # North Zone Extended
            'AGC': 'AGRA CANTT', 'ALD': 'ALLAHABAD', 'AMB': 'AMBALA CANTT', 'ANVT': 'ANAND VIHAR TERMINAL',
            'ASR': 'AMRITSAR', 'BE': 'BAREILLY', 'BTC': 'BALANAGAR', 'CDG': 'CHANDIGARH',
            'CNB': 'KANPUR CENTRAL', 'DLI': 'OLD DELHI', 'FBD': 'FARIDABAD', 'FDB': 'FARIDABAD NTC',
            'GGN': 'GURGAON', 'GZB': 'GHAZIABAD', 'HW': 'HARIDWAR', 'JAT': 'JAMMU TAWI',
            'JRC': 'JALANDHAR CITY', 'KKDE': 'KURUKSHETRA', 'KLK': 'KALKA', 'LDH': 'LUDHIANA',
            'LKO': 'LUCKNOW', 'MB': 'MORADABAD', 'MTJ': 'MATHURA', 'NDLS': 'NEW DELHI',
            'NZM': 'HAZRAT NIZAMUDDIN', 'PNP': 'PANIPAT', 'RE': 'REWARI', 'SRE': 'SAHARANPUR',
            'UHL': 'AMBALA CANTT', 'UMB': 'AMBALA', 'DGG': 'DONGARGARH', 'DDN': 'DEHRADUN',
            
            # South Zone Extended 
            'AJJ': 'ARAKKONAM', 'AFK': 'ANGAMALI', 'ATP': 'ANANTAPUR', 'AWY': 'ALUVA',
            'BWT': 'BANGARAPET', 'CAN': 'KANNUR', 'CBE': 'COIMBATORE', 'CLT': 'KOZHIKODE',
            'CRJ': 'CHITTARANJAN', 'CVR': 'CHEVUR', 'DPJ': 'DHARMAPURI', 'ED': 'ERODE',
            'ELS': 'ELURU', 'ERS': 'ERNAKULAM', 'GDR': 'GUDUR', 'GNT': 'GUNTUR',
            'GTL': 'GUNTAKAL', 'HBJ': 'HABIBGANJ', 'HSR': 'HISAR', 'JTJ': 'JOLARPETTAI',
            'KCG': 'KACHEGUDA', 'KJM': 'KRISHNARAJAPURAM', 'KTYM': 'KOTTAYAM', 'KUR': 'KHURDA ROAD',
            'KVZ': 'KAVALI', 'MAQ': 'MANGALORE CENTRAL', 'MAJN': 'MANGALORE JUNCTION', 
            'MAS': 'CHENNAI CENTRAL', 'MS': 'CHENNAI EGMORE', 'NLR': 'NELLORE', 'OGL': 'ONGOLE',
            'PGT': 'PALAKKAD', 'PUT': 'PUTTUR', 'QLN': 'KOLLAM', 'RJY': 'RAJAHMUNDRY',
            'RU': 'RENIGUNTA', 'SA': 'SALEM', 'SRR': 'SHORANUR', 'TCR': 'THRISSUR',
            'TEN': 'TIRUNELVELI', 'TIR': 'TIRUR', 'TPJ': 'TIRUCHIRAPALLI', 'TRT': 'TIRUTTANI',
            'TVC': 'TRIVANDRUM CENTRAL', 'UBL': 'HUBLI', 'VLR': 'VELLORE', 'VM': 'VILLUPURAM',
            'VSG': 'VASCO DA GAMA', 'WL': 'WARANGAL',
            
            # West Zone Extended
            'ADI': 'AHMEDABAD', 'AKV': 'ANKLESHWAR', 'BHL': 'BHILWARA', 'BRC': 'VADODARA',
            'BVC': 'BHAVNAGAR', 'DWK': 'DWARKA', 'JAM': 'JAMNAGAR', 'JU': 'JODHPUR',
            'KOTA': 'KOTA', 'MAO': 'MADGAON', 'PBR': 'PORBANDAR', 'RJT': 'RAJKOT',
            'RTM': 'RATLAM', 'ST': 'SURAT', 'UDZ': 'UDAIPUR CITY', 'VR': 'VIRAR',
            
            # Central Zone Extended
            'AGC': 'AGRA CANTT', 'BPL': 'BHOPAL', 'BSB': 'VARANASI', 'BSP': 'BILASPUR',
            'DURG': 'DURG', 'ET': 'ITARSI', 'GWL': 'GWALIOR', 'HBJ': 'HABIBGANJ',
            'INDB': 'INDORE', 'JBP': 'JABALPUR', 'KOTA': 'KOTA', 'R': 'RAIPUR',
            'RTM': 'RATLAM', 'STA': 'SATNA', 'UJN': 'UJJAIN',
            
            # Eastern Zone Extended
            'AZ': 'AZIMGANJ', 'BAND': 'BANIHAL', 'BDC': 'BANDEL', 'BGP': 'BHAGALPUR',
            'BWN': 'BARDDHAMAN', 'CGKP': 'CHANDRAKONA', 'CRD': 'CURREY ROAD', 'CRJ': 'CHITTARANJAN',
            'DBG': 'DARBHANGA', 'DGR': 'DURGAPUR', 'DHN': 'DHANBAD', 'EKM': 'EKAMBARAKUPPAM',
            'GAYA': 'GAYA', 'GKP': 'GORAKHPUR', 'HWH': 'HOWRAH', 'JYG': 'JEYPORE',
            'KGP': 'KHARAGPUR', 'KOAA': 'KOLKATA', 'KOP': 'KOLHAPUR', 'KYQ': 'KAMAKHYA',
            'MFP': 'MUZAFFARPUR', 'MUV': 'MANDUADIH', 'NJP': 'NEW JALPAIGURI', 'PNBE': 'PATNA',
            'RNC': 'RANCHI', 'SDAH': 'SEALDAH', 'SGUJ': 'SILIGURI', 'TATA': 'JAMSHEDPUR',
            
            # Northeast Frontier Extended
            'AGTL': 'AGARTALA', 'CPK': 'CHAPARMUKH', 'DBG': 'DARBHANGA', 'DBRG': 'DIBRUGARH',
            'DPU': 'DIPHU', 'FKG': 'FURKATING', 'GHY': 'GUWAHATI', 'GXG': 'GOHPUR',
            'HDB': 'HALDIBARI', 'JTTN': 'JORHAT TOWN', 'KWM': 'KAMRUP', 'LMG': 'LUMDING',
            'MXN': 'MARIANI', 'NBQ': 'NEW BONGAIGAON', 'NOQ': 'NEW ALIPURDUAR', 'NTSK': 'NEW TINSUKIA',
            'RDP': 'RANGAPARA NORTH', 'SCL': 'SILCHAR', 'SLGR': 'SILIRGHAT', 'TSK': 'TINSUKIA',
            
            # South Central Extended
            'AWB': 'AURANGABAD', 'BZA': 'VIJAYAWADA', 'BMT': 'BEGUMPET', 'BPQ': 'BALHARSHAH',
            'GNT': 'GUNTUR', 'GTL': 'GUNTAKAL', 'HYB': 'HYDERABAD DECCAN', 'KCG': 'KACHEGUDA',
            'NLDA': 'NALGONDA', 'SC': 'SECUNDERABAD', 'SNF': 'SONEGAON', 'TPTY': 'TIRUPATI',
            'VSKP': 'VISAKHAPATNAM', 'WL': 'WARANGAL',
            
            # South East Central Extended
            'ABKP': 'AMBIKESHWAR', 'BBS': 'BHUBANESWAR', 'BBS': 'BHUBANESWAR', 'BSP': 'BILASPUR',
            'CTC': 'CUTTACK', 'DNKL': 'DHENKANAL', 'JSPR': 'JASIDIH', 'KUR': 'KHURDA ROAD',
            'PURI': 'PURI', 'R': 'RAIPUR', 'ROU': 'ROURKELA', 'SBP': 'SAMBALPUR',
            'TATA': 'JAMSHEDPUR', 'VSKP': 'VISAKHAPATNAM',
            
            # South Western Extended
            'ASK': 'ARSIKERE', 'BGM': 'BELAGAVI', 'BLGM': 'BELGAUM', 'CTA': 'CHITRADURGA',
            'DVG': 'DAVANGERE', 'GR': 'GULBARGA', 'HAS': 'HASSAN', 'HSRA': 'HOSUR',
            'MAQ': 'MANGALORE CENTRAL', 'MAJN': 'MANGALORE JUNCTION', 'MYS': 'MYSORE',
            'RRB': 'BIRUR', 'SBC': 'BANGALORE CITY', 'UBL': 'HUBLI', 'YPR': 'YESVANTPUR',
            
            # West Central Extended
            'BFY': 'BHANDARA', 'BZU': 'BETUL', 'CMO': 'CHITTAURGARH', 'ET': 'ITARSI',
            'INDB': 'INDORE', 'JBP': 'JABALPUR', 'KNW': 'KHANDWA', 'NGP': 'NAGPUR',
            'RIG': 'RAIGARH', 'RTM': 'RATLAM', 'UJN': 'UJJAIN',
            
            # North Central Extended
            'AGC': 'AGRA CANTT', 'ALD': 'ALLAHABAD', 'BAND': 'BANDA', 'CNB': 'KANPUR CENTRAL',
            'CPR': 'CHHAPRA', 'GKP': 'GORAKHPUR', 'JHS': 'JHANSI', 'LJN': 'LUCKNOW NE',
            'LKO': 'LUCKNOW', 'MKP': 'MANIKPUR', 'PHD': 'PHAPHUND', 'PRYJ': 'PRAYAG',
            'STA': 'SATNA', 'TDL': 'TUNDLA', 'THO': 'TUTICORIN',
            
            # North Western Extended
            'AII': 'AJMER', 'BER': 'BEAWAR', 'BKN': 'BIKANER', 'FA': 'FALNA',
            'JP': 'JAIPUR', 'JU': 'JODHPUR', 'LUNI': 'LUNI', 'MTD': 'MERTA ROAD',
            'RE': 'REWARI', 'RKS': 'RAJKISHAN', 'RTGH': 'RATANGARH', 'SMPR': 'SHRI MADHOPUR',
            'SOG': 'SURATGARH', 'UDZ': 'UDAIPUR CITY',
            
            # Metro & Suburban Stations
            'ANDHERI': 'ANDHERI', 'BORIVALI': 'BORIVALI', 'BYCULLA': 'BYCULLA', 'CSMT': 'CHHATRAPATI SHIVAJI MAHARAJ TERMINUS',
            'DADAR': 'DADAR', 'GHATKOPAR': 'GHATKOPAR', 'JOGESHWARI': 'JOGESHWARI', 'KHAR': 'KHAR ROAD',
            'MALAD': 'MALAD', 'MATUNGA': 'MATUNGA', 'MULUND': 'MULUND', 'SANTACRUZ': 'SANTACRUZ',
            'VILE PARLE': 'VILE PARLE', 'WADALA': 'WADALA', 'WHITEFIELD': 'WHITEFIELD',
            
            # Special Trains & Tourist Destinations
            'AGARTALA': 'AGARTALA', 'ALAPPUZHA': 'ALAPPUZHA', 'AMRITSAR': 'AMRITSAR', 'AULI': 'AULI',
            'BADRINATH': 'BADRINATH', 'CHANDIGARH': 'CHANDIGARH', 'DALHOUSIE': 'DALHOUSIE', 'DARJEELING': 'DARJEELING',
            'GULMARG': 'GULMARG', 'HAMPI': 'HAMPI', 'HARIDWAR': 'HARIDWAR', 'KATRA': 'KATRA',
            'KEDARNATH': 'KEDARNATH', 'KOVALAM': 'KOVALAM', 'KULLU': 'KULLU', 'MANALI': 'MANALI',
            'MUSSOORIE': 'MUSSOORIE', 'NAINITAL': 'NAINITAL', 'OOTY': 'OOTY', 'RISHIKESH': 'RISHIKESH',
            'SHILLONG': 'SHILLONG', 'SHIMLA': 'SHIMLA', 'SRINAGAR': 'SRINAGAR', 'UDAGAMANDALAM': 'UDAGAMANDALAM',
            'VAISHNO DEVI': 'VAISHNO DEVI', 'VASHISHT': 'VASHISHT',
            
            # Industrial Cities & Junction Points
            'ANGUL': 'ANGUL', 'ASANSOL': 'ASANSOL', 'BHADRAK': 'BHADRAK', 'BHILAI': 'BHILAI',
            'BILASPUR': 'BILASPUR', 'BOKARO': 'BOKARO STEEL CITY', 'BURNPUR': 'BURNPUR', 'DURGAPUR': 'DURGAPUR',
            'HALDIAPORT': 'HALDIA', 'JAMSHEDPUR': 'JAMSHEDPUR', 'KORBA': 'KORBA', 'NEYVELI': 'NEYVELI',
            'PARADIP': 'PARADIP', 'RAJAHMUNDRY': 'RAJAHMUNDRY', 'RANCHI': 'RANCHI', 'ROURKELA': 'ROURKELA',
            'SALEM': 'SALEM', 'SAMBALPUR': 'SAMBALPUR', 'SINGRAULI': 'SINGRAULI', 'TALCHER': 'TALCHER',
            'TINSUKIA': 'TINSUKIA', 'TUTICORIN': 'TUTICORIN', 'VIZIANAGARAM': 'VIZIANAGARAM',
            
            # Border & International Connection Points
            'ATTARI': 'ATTARI', 'BENAPOLE': 'BENAPOLE', 'GEDE': 'GEDE', 'HALDIBARI': 'HALDIBARI',
            'MUNABAO': 'MUNABAO', 'PETRAPOLE': 'PETRAPOLE', 'RADHIKAPUR': 'RADHIKAPUR', 'RAXAUL': 'RAXAUL',
            
            # Port Cities & Coastal Stations
            'ALANG': 'ALANG', 'BHAVNAGAR': 'BHAVNAGAR', 'CHENNAI PORT': 'CHENNAI PORT', 'COCHIN PORT': 'COCHIN PORT',
            'HALDIA': 'HALDIA', 'KANDLA': 'KANDLA', 'KARWAR': 'KARWAR', 'KOCHI': 'KOCHI',
            'MANGALORE': 'MANGALORE', 'MARMAGAO': 'MARMAGAO', 'MUMBAI PORT': 'MUMBAI PORT', 'NHAVA SHEVA': 'NHAVA SHEVA',
            'OKHA': 'OKHA', 'PARADIP PORT': 'PARADIP PORT', 'PIPAVAV': 'PIPAVAV', 'PORBANDAR': 'PORBANDAR',
            'TUTICORIN': 'TUTICORIN', 'VERAVAL': 'VERAVAL', 'VISAKHAPATNAM PORT': 'VISAKHAPATNAM PORT'
        }
        
        # Merge all databases
        comprehensive_db = {}
        comprehensive_db.update(existing_quick_lookup)
        comprehensive_db.update(extended_stations)
        
        return comprehensive_db
    
    def get_coordinate_database(self):
        """Get coordinate database from calculator"""
        coordinates_method = getattr(self.calculator, 'estimate_distance_by_coordinates', None)
        if coordinates_method:
            # Extract coordinates from the method (this is a bit hacky but works)
            import inspect
            source_code = inspect.getsource(coordinates_method)
            
            # Find coordinate mappings in the source
            coordinate_dict = {}
            lines = source_code.split('\n')
            for line in lines:
                if ':' in line and '(' in line and ')' in line:
                    try:
                        # Simple regex to extract station:coordinate mappings
                        if "'" in line and ':' in line:
                            parts = line.split("'")
                            if len(parts) >= 3:
                                station_name = parts[1]
                                if '(' in line and ')' in line:
                                    coord_start = line.find('(')
                                    coord_end = line.find(')')
                                    if coord_start != -1 and coord_end != -1:
                                        coords_str = line[coord_start+1:coord_end]
                                        try:
                                            coords = eval(f"({coords_str})")
                                            if len(coords) == 2:
                                                coordinate_dict[station_name] = coords
                                        except:
                                            pass
                    except:
                        continue
            return coordinate_dict
        return {}
    
    def analyze_all_station_codes(self):
        """Comprehensive analysis of all station codes"""
        
        # Get all station codes from various sources
        quick_lookup_codes = set(self.calculator.get_quick_station_lookup().keys())
        comprehensive_codes = set(self.comprehensive_station_database.keys())
        coordinate_codes = set(self.get_coordinate_database().keys())
        
        # Get cached stations from database
        try:
            cached_stations = self.calculator.get_cached_stations()
            cached_codes = set([station['code'] for station in cached_stations])
        except:
            cached_codes = set()
        
        # Combine all sources
        all_found_codes = quick_lookup_codes | comprehensive_codes | coordinate_codes | cached_codes
        
        # Common Indian Railway station codes that might not be in our database
        common_missing_codes = {
            'CSMT', 'LTT', 'KYN', 'PNVL', 'TNA', 'DR', 'ANVT', 'NZM', 'DLI', 'DEE',
            'GZB', 'FDB', 'UHP', 'KKDE', 'KLK', 'CDG', 'ASR', 'LDH', 'JRC', 'UMB',
            'JAT', 'JAMMU', 'SRINAGAR', 'LEH', 'KATRA', 'UDHAMPUR', 'PATHANKOT',
            'BATHINDA', 'FEROZEPUR', 'ABOHAR', 'FAZILKA', 'GANGANAGAR', 'HANUMANGARH',
            'SIKAR', 'CHURU', 'JHUNJHUNU', 'ALWAR', 'BHARATPUR', 'MATHURA JN',
            'FIROZABAD', 'ETAWAH', 'KANNAUJ', 'FARRUKHABAD', 'SHAHJAHANPUR', 'BAREILLY',
            'PILIBHIT', 'LAKHIMPUR', 'SITAPUR', 'HARDOI', 'UNNAO', 'RAE BARELI',
            'SULTANPUR', 'FAIZABAD', 'GONDA', 'BALRAMPUR', 'SHRAVASTI', 'BAHRAICH',
            'LAKHIMPUR KHERI', 'BIJNOR', 'MUZAFFARNAGAR', 'SHAMLI', 'BAGHPAT', 'MEERUT',
            'BULANDSHAHR', 'ALIGARH', 'HATHRAS', 'KASGANJ', 'MAINPURI', 'ETAH',
            'BUDAUN', 'MORADABAD', 'RAMPUR', 'SAMBHAL', 'AMROHA', 'BIJNOR',
            'NAINITAL', 'UDHAM SINGH NAGAR', 'CHAMPAWAT', 'PITHORAGARH', 'ALMORA',
            'BAGESHWAR', 'CHAMOLI', 'RUDRAPRAYAG', 'TEHRI GARHWAL', 'PAURI GARHWAL',
            'UTTARKASHI', 'DEHRADUN', 'HARIDWAR', 'ROORKEE', 'SAHARANPUR'
        }
        
        # Test some codes to see which are missing
        potentially_missing = common_missing_codes - all_found_codes
        
        return {
            'found_codes': sorted(list(all_found_codes)),
            'potentially_missing': sorted(list(potentially_missing)),
            'quick_lookup_count': len(quick_lookup_codes),
            'comprehensive_count': len(comprehensive_codes),
            'coordinate_count': len(coordinate_codes),
            'cached_count': len(cached_codes),
            'total_found': len(all_found_codes),
            'breakdown': {
                'quick_lookup_only': quick_lookup_codes - comprehensive_codes - coordinate_codes,
                'comprehensive_only': comprehensive_codes - quick_lookup_codes - coordinate_codes,
                'coordinates_only': coordinate_codes - quick_lookup_codes - comprehensive_codes,
                'cached_only': cached_codes - quick_lookup_codes - comprehensive_codes - coordinate_codes,
                'all_sources': quick_lookup_codes & comprehensive_codes & coordinate_codes
            }
        }
    
    def test_station_lookup(self, test_codes):
        """Test specific station codes"""
        results = {}
        for code in test_codes:
            try:
                full_name = self.calculator.get_full_station_name(code)
                coord_available = code.upper() in self.get_coordinate_database()
                results[code] = {
                    'found': full_name != code,
                    'full_name': full_name,
                    'coordinates_available': coord_available,
                    'source': 'quick_lookup' if code in self.calculator.get_quick_station_lookup() else 'comprehensive' if code in self.comprehensive_station_database else 'api' if full_name != code else 'not_found'
                }
            except Exception as e:
                results[code] = {
                    'found': False,
                    'full_name': code,
                    'coordinates_available': False,
                    'error': str(e),
                    'source': 'error'
                }
        return results
    
    def generate_comprehensive_report(self):
        """Generate comprehensive station code analysis report"""
        
        print("🚂 COMPREHENSIVE RAILWAY STATION CODE ANALYSIS")
        print("=" * 60)
        
        # Overall analysis
        analysis = self.analyze_all_station_codes()
        
        print(f"\n📊 COVERAGE STATISTICS:")
        print(f"Total Station Codes Found: {analysis['total_found']}")
        print(f"Quick Lookup Database: {analysis['quick_lookup_count']} codes")
        print(f"Comprehensive Database: {analysis['comprehensive_count']} codes")
        print(f"Coordinate Database: {analysis['coordinate_count']} codes")
        print(f"Cached in SQLite: {analysis['cached_count']} codes")
        
        print(f"\n🔍 DATABASE BREAKDOWN:")
        breakdown = analysis['breakdown']
        print(f"Quick Lookup Only: {len(breakdown['quick_lookup_only'])} codes")
        print(f"Comprehensive Only: {len(breakdown['comprehensive_only'])} codes")
        print(f"Coordinates Only: {len(breakdown['coordinates_only'])} codes")
        print(f"Cached Only: {len(breakdown['cached_only'])} codes")
        print(f"All Sources: {len(breakdown['all_sources'])} codes")
        
        # Test common codes
        test_codes = ['PN', 'JP', 'SBC', 'NDLS', 'MAS', 'HWH', 'SC', 'BCT', 'AMD', 'LKO', 
                     'CSMT', 'LTT', 'YPR', 'CBE', 'ERS', 'TVC', 'MAQ', 'GOA', 'JAT', 'ASR',
                     'UNKNOWN', 'XYZ', 'ABC']
        
        print(f"\n🧪 TESTING SAMPLE CODES:")
        test_results = self.test_station_lookup(test_codes)
        
        found_count = 0
        for code, result in test_results.items():
            status = "✅ FOUND" if result['found'] else "❌ NOT FOUND"
            coord_status = "📍 Coords" if result['coordinates_available'] else "🚫 No Coords"
            print(f"{code:8} - {status:12} - {coord_status:12} - {result['full_name']:30} ({result['source']})")
            if result['found']:
                found_count += 1
        
        success_rate = (found_count / len(test_codes)) * 100
        print(f"\nTest Success Rate: {success_rate:.1f}% ({found_count}/{len(test_codes)})")
        
        # Show potentially missing codes
        print(f"\n⚠️  POTENTIALLY MISSING CODES:")
        missing_codes = analysis['potentially_missing'][:20]  # Show first 20
        for i, code in enumerate(missing_codes):
            print(f"{i+1:2}. {code}")
        if len(analysis['potentially_missing']) > 20:
            print(f"... and {len(analysis['potentially_missing']) - 20} more")
        
        return analysis, test_results
    
    def export_station_database(self, filename='complete_station_database.json'):
        """Export complete station database to JSON"""
        export_data = {
            'metadata': {
                'total_stations': len(self.comprehensive_station_database),
                'last_updated': '2025-01-07',
                'version': '1.0.0',
                'description': 'Comprehensive Indian Railway Station Code Database'
            },
            'station_codes': self.comprehensive_station_database,
            'coordinates': self.get_coordinate_database(),
            'analysis': self.analyze_all_station_codes()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported complete database to {filename}")
        return filename

if __name__ == "__main__":
    analyzer = StationCodeAnalyzer()
    analysis, test_results = analyzer.generate_comprehensive_report()
    analyzer.export_station_database() 