import requests
import json
import time
import pandas as pd
from collections import defaultdict
import re

class StationCodeFinder:
    def __init__(self):
        self.found_stations = {}
        self.not_found_codes = []
        self.api_calls_made = 0
        
    def get_common_station_codes(self):
        """Get list of commonly used Indian Railway station codes"""
        return [
            # Major Metro Cities
            'SBC', 'NDLS', 'BCT', 'MAS', 'HWH', 'SC', 'PUNE', 'AMD', 'LKO', 'JP', 
            'BLR', 'DEL', 'MUM', 'CHN', 'HYD', 'KOL', 'PN',
            
            # Major Junction Stations
            'CNB', 'BSB', 'ALD', 'AGC', 'MTJ', 'GKP', 'PNBE', 'GAYA', 'MFP', 'DBG', 'BGP',
            'SDAH', 'KGP', 'DGR', 'ASN', 'NJP', 'SGUJ', 'BPL', 'INDB', 'JBP', 'UJN',
            'GWL', 'RTM', 'R', 'BSP', 'DURG', 'BBS', 'CTC', 'PURI', 'BAM',
            
            # South Zone
            'BZA', 'VSKP', 'TPTY', 'GNT', 'NLR', 'RJY', 'WL', 'MS', 'CBE', 'MDU',
            'SA', 'TPJ', 'TEN', 'ED', 'VLR', 'ERS', 'TVC', 'TCR', 'CLT', 'CAN',
            'KTYM', 'PGT', 'YPR', 'MYS', 'UBL', 'MAQ', 'BGM', 'GR', 'DVG', 'MAO', 'VSG',
            
            # North Zone Extended
            'ASR', 'LDH', 'JRC', 'CDG', 'UMB', 'KKDE', 'KLK', 'HW', 'DDN', 'RNC',
            'DHN', 'TATA', 'GHY', 'DBRG', 'JTTN', 'NTSK', 'JAT', 'UHP',
            
            # West Zone
            'ST', 'BRC', 'RJT', 'BVC', 'JAM', 'DWK', 'JU', 'UDZ', 'AII', 'BKN', 'KOTA',
            
            # Maharashtra Extended
            'NK', 'AWB', 'SUR', 'KOP', 'NGP', 'AMI', 'CSMT', 'LTT', 'DR', 'KYN',
            'PNVL', 'TNA', 'KALYAN', 'DADAR', 'BORIVALI', 'ANDHERI',
            
            # Delhi NCR
            'DLI', 'DEE', 'NZM', 'ANVT', 'GZB', 'FDB', 'GGN', 'FBD',
            
            # Additional Important Codes
            'ET', 'BIA', 'RJPB', 'PPTA', 'SHC', 'CPR', 'GKP', 'BST', 'LJN',
            'BE', 'MB', 'SRE', 'RK', 'FZ', 'BTC', 'BTINDA', 'HSR', 'ROK',
            'SOG', 'LUNI', 'FA', 'BER', 'RTGH', 'MTD', 'SMPR', 'RE',
            
            # Tourist & Hill Stations
            'UDH', 'SHIMLA', 'NAINITAL', 'MUSSOORIE', 'RISHIKESH', 'HARIDWAR',
            'JAMMU', 'SRINAGAR', 'LEH', 'KATRA', 'VAISHNO_DEVI',
            
            # Port Cities
            'MUMBAI_PORT', 'CHENNAI_PORT', 'KOCHI_PORT', 'HALDIA', 'PARADIP',
            'KANDLA', 'NHAVA_SHEVA', 'TUTICORIN', 'VISAKHAPATNAM_PORT',
            
            # Industrial Cities
            'ANGUL', 'BHILAI', 'BOKARO', 'BURNPUR', 'KORBA', 'NEYVELI',
            'ROURKELA', 'SINGRAULI', 'TALCHER', 'VIZIANAGARAM',
            
            # Border Stations
            'ATTARI', 'MUNABAO', 'RAXAUL', 'HALDIBARI', 'GEDE', 'PETRAPOLE',
            
            # Regional Important Stations
            'AJMER', 'ALWAR', 'BHARATPUR', 'SIKAR', 'CHURU', 'JHUNJHUNU',
            'GANGANAGAR', 'HANUMANGARH', 'PATHANKOT', 'BATHINDA', 'FEROZEPUR',
            'ABOHAR', 'FAZILKA', 'FIROZABAD', 'ETAWAH', 'KANNAUJ', 'FARRUKHABAD',
            'SHAHJAHANPUR', 'BAREILLY', 'PILIBHIT', 'LAKHIMPUR', 'SITAPUR',
            'HARDOI', 'UNNAO', 'RAE_BARELI', 'SULTANPUR', 'FAIZABAD', 'GONDA',
            'BALRAMPUR', 'SHRAVASTI', 'BAHRAICH', 'BIJNOR', 'MUZAFFARNAGAR',
            'SHAMLI', 'BAGHPAT', 'MEERUT', 'BULANDSHAHR', 'ALIGARH', 'HATHRAS',
            'KASGANJ', 'MAINPURI', 'ETAH', 'BUDAUN', 'RAMPUR', 'SAMBHAL', 'AMROHA',
            
            # Additional codes that might be commonly used
            'ALLP', 'ALUR', 'AMH', 'APDJ', 'AVRD', 'BAY', 'BDTS', 'BG', 'BINA',
            'BJPL', 'BL', 'BNE', 'BOE', 'TVCR', 'KAWR', 'KRN', 'SOM', 'NGLs'
        ]
    
    def search_via_rapidapi(self, station_code, api_key):
        """Search station name using RapidAPI"""
        try:
            url = "https://indianrailways.p.rapidapi.com/findstations.php"
            headers = {
                'x-rapidapi-key': api_key,
                'x-rapidapi-host': 'indianrailways.p.rapidapi.com'
            }
            params = {'station': station_code}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            self.api_calls_made += 1
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and 'stations' in data:
                    for station in data['stations']:
                        if station.get('station_code', '').upper() == station_code.upper():
                            return station.get('station_name', '').upper()
                            
        except Exception as e:
            print(f"RapidAPI error for {station_code}: {str(e)}")
            
        return None
    
    def search_via_public_apis(self, station_code):
        """Search using multiple public APIs"""
        apis_to_try = [
            f"https://indian-railway-api.cyclic.app/stations/{station_code}",
            f"https://railway-api.onrender.com/station?code={station_code}",
            f"https://api.railwayapi.site/station/{station_code}",
        ]
        
        for api_url in apis_to_try:
            try:
                response = requests.get(api_url, timeout=10)
                self.api_calls_made += 1
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Handle different API response formats
                    if isinstance(data, dict):
                        name = data.get('name') or data.get('stationName') or data.get('station_name')
                        if name:
                            return name.upper()
                    elif isinstance(data, list) and len(data) > 0:
                        name = data[0].get('stationName') or data[0].get('name')
                        if name:
                            return name.upper()
                            
            except Exception as e:
                continue
        
        return None
    
    def search_via_web_scraping(self, station_code):
        """Search using web scraping (as backup)"""
        try:
            # Try Indian Railways official website pattern
            search_urls = [
                f"https://enquiry.indianrail.gov.in/mntes/station/{station_code}",
                f"https://www.trainman.in/station/{station_code}",
                f"https://www.irctc.co.in/nget/train-search?stationFrom={station_code}",
            ]
            
            for url in search_urls:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=10)
                    self.api_calls_made += 1
                    
                    if response.status_code == 200:
                        content = response.text
                        # Simple pattern matching for station names
                        patterns = [
                            rf'{station_code}.*?([A-Z\s]+STATION|[A-Z\s]+JN|[A-Z\s]+CENTRAL|[A-Z\s]+CITY)',
                            rf'({station_code})\s*-\s*([A-Z\s]+)',
                            rf'Station.*?{station_code}.*?([A-Z\s]+)',
                        ]
                        
                        for pattern in patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                # Return the first reasonable match
                                match = matches[0]
                                if isinstance(match, tuple):
                                    match = match[-1]  # Get the station name part
                                cleaned = re.sub(r'[^\w\s]', '', match).strip().upper()
                                if len(cleaned) > 3:  # Reasonable station name length
                                    return cleaned
                                    
                except:
                    continue
                    
        except Exception as e:
            pass
            
        return None
    
    def find_station_name(self, station_code, rapidapi_key=None):
        """Comprehensive station name finder"""
        station_code = station_code.strip().upper()
        
        print(f"🔍 Searching for: {station_code}")
        
        # Method 1: RapidAPI (if key provided)
        if rapidapi_key:
            name = self.search_via_rapidapi(station_code, rapidapi_key)
            if name:
                print(f"✅ Found via RapidAPI: {station_code} -> {name}")
                return name
        
        # Method 2: Public APIs
        name = self.search_via_public_apis(station_code)
        if name:
            print(f"✅ Found via Public API: {station_code} -> {name}")
            return name
        
        # Method 3: Web scraping (backup)
        name = self.search_via_web_scraping(station_code)
        if name:
            print(f"✅ Found via Web: {station_code} -> {name}")
            return name
        
        print(f"❌ Not found: {station_code}")
        return None
    
    def batch_find_stations(self, station_codes, rapidapi_key=None, delay=0.5):
        """Find station names for a batch of codes"""
        
        print(f"🚂 Starting batch search for {len(station_codes)} station codes...")
        print(f"⏱️  API delay: {delay} seconds between calls")
        print("=" * 60)
        
        found_count = 0
        
        for i, code in enumerate(station_codes):
            print(f"\n[{i+1}/{len(station_codes)}] ", end="")
            
            name = self.find_station_name(code, rapidapi_key)
            
            if name:
                self.found_stations[code] = name
                found_count += 1
            else:
                self.not_found_codes.append(code)
            
            # Progress update
            if (i + 1) % 10 == 0:
                success_rate = (found_count / (i + 1)) * 100
                print(f"\n📊 Progress: {i+1}/{len(station_codes)} | Found: {found_count} | Success Rate: {success_rate:.1f}%")
                print(f"🔧 API calls made: {self.api_calls_made}")
            
            # Rate limiting
            if delay > 0:
                time.sleep(delay)
        
        print("\n" + "=" * 60)
        print(f"✅ BATCH SEARCH COMPLETE!")
        print(f"📊 Total Found: {len(self.found_stations)}")
        print(f"❌ Not Found: {len(self.not_found_codes)}")
        print(f"🔧 Total API calls: {self.api_calls_made}")
        success_rate = (len(self.found_stations) / len(station_codes)) * 100
        print(f"📈 Overall Success Rate: {success_rate:.1f}%")
        
        return self.found_stations, self.not_found_codes
    
    def generate_station_database_code(self):
        """Generate Python code for station database"""
        
        code_lines = ["def get_comprehensive_station_lookup():"]
        code_lines.append('    """Comprehensive station code to name mapping"""')
        code_lines.append('    return {')
        
        # Sort stations alphabetically for better organization
        sorted_stations = sorted(self.found_stations.items())
        
        for code, name in sorted_stations:
            # Clean the name and format properly
            clean_name = name.strip().replace("'", "\\'")
            code_lines.append(f"        '{code}': '{clean_name}',")
        
        code_lines.append('    }')
        
        return '\n'.join(code_lines)
    
    def export_results(self, filename_prefix='station_codes'):
        """Export results in multiple formats"""
        
        # Export as JSON
        json_data = {
            'metadata': {
                'total_searched': len(self.found_stations) + len(self.not_found_codes),
                'found_count': len(self.found_stations),
                'not_found_count': len(self.not_found_codes),
                'success_rate': (len(self.found_stations) / (len(self.found_stations) + len(self.not_found_codes))) * 100,
                'api_calls_made': self.api_calls_made,
                'search_date': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'found_stations': self.found_stations,
            'not_found_codes': self.not_found_codes
        }
        
        json_filename = f"{filename_prefix}_results.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Export as CSV
        csv_data = []
        for code, name in self.found_stations.items():
            csv_data.append({'Station_Code': code, 'Station_Name': name, 'Status': 'Found'})
        
        for code in self.not_found_codes:
            csv_data.append({'Station_Code': code, 'Station_Name': '', 'Status': 'Not Found'})
        
        df = pd.DataFrame(csv_data)
        csv_filename = f"{filename_prefix}_results.csv"
        df.to_csv(csv_filename, index=False)
        
        # Export Python code
        python_code = self.generate_station_database_code()
        py_filename = f"{filename_prefix}_database.py"
        with open(py_filename, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        print(f"\n📁 EXPORTED FILES:")
        print(f"  📄 {json_filename} - Complete results in JSON format")
        print(f"  📊 {csv_filename} - Results in CSV format")
        print(f"  🐍 {py_filename} - Python code for station database")
        
        return json_filename, csv_filename, py_filename
    
    def print_summary_report(self):
        """Print detailed summary report"""
        
        print("\n" + "="*80)
        print("🚂 STATION CODE FINDER - COMPREHENSIVE REPORT")
        print("="*80)
        
        total_codes = len(self.found_stations) + len(self.not_found_codes)
        success_rate = (len(self.found_stations) / total_codes) * 100 if total_codes > 0 else 0
        
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"  Total Codes Searched: {total_codes}")
        print(f"  ✅ Found: {len(self.found_stations)} ({success_rate:.1f}%)")
        print(f"  ❌ Not Found: {len(self.not_found_codes)} ({100-success_rate:.1f}%)")
        print(f"  🔧 API Calls Made: {self.api_calls_made}")
        
        if self.found_stations:
            print(f"\n✅ FOUND STATIONS (Sample - First 20):")
            found_items = list(self.found_stations.items())[:20]
            for code, name in found_items:
                print(f"  {code:8} -> {name}")
            if len(self.found_stations) > 20:
                print(f"  ... and {len(self.found_stations) - 20} more")
        
        if self.not_found_codes:
            print(f"\n❌ NOT FOUND CODES:")
            for i, code in enumerate(self.not_found_codes[:20]):
                print(f"  {i+1:2}. {code}")
            if len(self.not_found_codes) > 20:
                print(f"  ... and {len(self.not_found_codes) - 20} more")
        
        print("\n" + "="*80)

def main():
    """Main execution function"""
    finder = StationCodeFinder()
    
    # Get station codes to search
    station_codes = finder.get_common_station_codes()
    
    print("🚂 RAILWAY STATION CODE FINDER")
    print("="*50)
    print(f"📋 Loaded {len(station_codes)} station codes to search")
    
    # Ask for RapidAPI key (optional)
    rapidapi_key = input("\n🔑 Enter RapidAPI key (optional, press Enter to skip): ").strip()
    if not rapidapi_key:
        rapidapi_key = None
        print("⚠️  No RapidAPI key provided. Will use public APIs only.")
    else:
        print("✅ RapidAPI key provided. Will use all available sources.")
    
    # Configure delay
    delay = float(input("\n⏱️  API delay in seconds (default 0.5): ") or "0.5")
    
    print(f"\n🚀 Starting search process...")
    
    # Run the batch search
    found_stations, not_found_codes = finder.batch_find_stations(
        station_codes, 
        rapidapi_key=rapidapi_key, 
        delay=delay
    )
    
    # Generate reports
    finder.print_summary_report()
    
    # Export results
    json_file, csv_file, py_file = finder.export_results()
    
    print(f"\n🎉 PROCESS COMPLETE!")
    print(f"📊 Found {len(found_stations)} out of {len(station_codes)} station codes")
    print(f"📁 Results exported to: {json_file}, {csv_file}, {py_file}")

if __name__ == "__main__":
    main() 