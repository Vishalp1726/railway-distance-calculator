import re
from complete_api_railway_calculator import CompleteAPIRailwayCalculator

class MissingStationFinder:
    def __init__(self):
        self.calculator = CompleteAPIRailwayCalculator()
        self.found_stations = {}
        self.missing_codes = []
        
    def extract_all_station_codes_from_script(self):
        """Extract all station codes mentioned in the calculator script"""
        
        # Read the calculator script
        with open('complete_api_railway_calculator.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract codes from quick lookup method
        quick_lookup_codes = set(self.calculator.get_quick_station_lookup().keys())
        
        # Extract codes from coordinate database
        coordinate_section_match = re.search(r'coordinates = \{(.*?)\}', content, re.DOTALL)
        coordinate_codes = set()
        if coordinate_section_match:
            coord_content = coordinate_section_match.group(1)
            # Find all quoted strings that look like station codes
            coord_matches = re.findall(r"'([A-Z]+[A-Z0-9]*)':", coord_content)
            coordinate_codes = set(coord_matches)
        
        # Extract codes from default stations
        default_section_match = re.search(r'default_stations = \[(.*?)\]', content, re.DOTALL)
        default_codes = set()
        if default_section_match:
            default_content = default_section_match.group(1)
            default_matches = re.findall(r'"([A-Z]+[A-Z0-9]*)"', default_content)
            default_codes = set(default_matches)
        
        # Combine all found codes
        all_codes = quick_lookup_codes | coordinate_codes | default_codes
        
        return {
            'quick_lookup': quick_lookup_codes,
            'coordinates': coordinate_codes, 
            'defaults': default_codes,
            'all_unique': all_codes
        }
    
    def test_station_codes(self, codes_to_test):
        """Test which station codes can be resolved to full names"""
        
        print(f"🔍 Testing {len(codes_to_test)} station codes...")
        print("=" * 60)
        
        found_count = 0
        
        for i, code in enumerate(sorted(codes_to_test)):
            try:
                # Use the calculator's existing method
                full_name = self.calculator.get_full_station_name(code)
                
                if full_name != code:
                    # Found a full name
                    self.found_stations[code] = full_name
                    print(f"✅ {code:8} -> {full_name}")
                    found_count += 1
                else:
                    # Could not find full name
                    self.missing_codes.append(code)
                    print(f"❌ {code:8} -> NOT FOUND")
                    
            except Exception as e:
                self.missing_codes.append(code)
                print(f"💥 {code:8} -> ERROR: {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"📊 SUMMARY:")
        print(f"✅ Found: {found_count}/{len(codes_to_test)} ({found_count/len(codes_to_test)*100:.1f}%)")
        print(f"❌ Missing: {len(self.missing_codes)}")
        
        return self.found_stations, self.missing_codes
    
    def generate_missing_codes_list(self):
        """Generate a formatted list of missing codes for manual research"""
        
        if not self.missing_codes:
            print("🎉 All station codes found! No manual research needed.")
            return
        
        print(f"\n📋 MISSING STATION CODES FOR MANUAL RESEARCH:")
        print("=" * 60)
        print(f"Please search these {len(self.missing_codes)} codes on Google and provide full names:")
        print()
        
        # Format for easy copying
        for i, code in enumerate(sorted(self.missing_codes), 1):
            print(f"{i:2}. {code}")
        
        print(f"\n💡 SEARCH TIPS:")
        print(f"- Search: '[CODE] railway station India'")
        print(f"- Search: '[CODE] train station full name'") 
        print(f"- Check: indianrail.gov.in, irctc.co.in, trainman.in")
        print(f"- Look for: 'Station Code: [CODE] - [FULL NAME]'")
        
        # Generate copy-paste friendly format
        print(f"\n📄 COPY-PASTE FORMAT:")
        print("# Please fill in the station names:")
        for code in sorted(self.missing_codes):
            print(f"'{code}': 'FULL_STATION_NAME_HERE',")
    
    def add_manual_research_results(self, manual_results):
        """Add manually researched station names"""
        
        print(f"📥 Adding {len(manual_results)} manually researched stations...")
        
        for code, name in manual_results.items():
            if code in self.missing_codes:
                self.found_stations[code] = name.upper().strip()
                self.missing_codes.remove(code)
                print(f"✅ Added: {code} -> {name}")
            else:
                print(f"⚠️  Code {code} was not in missing list")
        
        remaining = len(self.missing_codes)
        total_found = len(self.found_stations)
        
        print(f"\n📊 UPDATED SUMMARY:")
        print(f"✅ Total Found: {total_found}")
        print(f"❌ Still Missing: {remaining}")
        
        if remaining == 0:
            print("🎉 All station codes now have full names!")
    
    def generate_updated_station_database(self):
        """Generate complete station database code"""
        
        print(f"\n🔧 Generating updated station database...")
        
        # Combine with existing database
        existing_lookup = self.calculator.get_quick_station_lookup()
        combined_stations = {**existing_lookup, **self.found_stations}
        
        # Generate Python code
        code_lines = []
        code_lines.append("def get_comprehensive_station_lookup():")
        code_lines.append('    """Comprehensive station code to name mapping - Auto-generated"""')
        code_lines.append('    return {')
        
        # Sort alphabetically for better organization
        for code in sorted(combined_stations.keys()):
            name = combined_stations[code].replace("'", "\\'")
            code_lines.append(f"        '{code}': '{name}',")
        
        code_lines.append('    }')
        
        # Write to file
        with open('updated_station_database.py', 'w', encoding='utf-8') as f:
            f.write('\n'.join(code_lines))
        
        print(f"✅ Updated database saved to: updated_station_database.py")
        print(f"📊 Total stations: {len(combined_stations)}")
        
        return combined_stations

def main():
    """Main function to find missing stations"""
    
    print("🚂 MISSING STATION CODE FINDER")
    print("=" * 50)
    
    finder = MissingStationFinder()
    
    # Extract all codes from the script
    print("📂 Extracting station codes from railway calculator...")
    extracted_codes = finder.extract_all_station_codes_from_script()
    
    print(f"\n📊 EXTRACTED CODES:")
    print(f"Quick Lookup: {len(extracted_codes['quick_lookup'])} codes")
    print(f"Coordinates: {len(extracted_codes['coordinates'])} codes") 
    print(f"Defaults: {len(extracted_codes['defaults'])} codes")
    print(f"Total Unique: {len(extracted_codes['all_unique'])} codes")
    
    # Test which codes can be resolved
    found_stations, missing_codes = finder.test_station_codes(extracted_codes['all_unique'])
    
    # Generate list for manual research
    finder.generate_missing_codes_list()
    
    if missing_codes:
        print(f"\n🤝 NEXT STEPS:")
        print(f"1. Search the {len(missing_codes)} missing codes on Google")
        print(f"2. Fill in the station names in the format shown above")
        print(f"3. Run this script again with the manual results")
        
        # Save current progress
        import json
        progress_data = {
            'found_stations': found_stations,
            'missing_codes': missing_codes,
            'total_codes': len(extracted_codes['all_unique'])
        }
        
        with open('station_search_progress.json', 'w') as f:
            json.dump(progress_data, f, indent=2)
        
        print(f"💾 Progress saved to: station_search_progress.json")
    
    return finder

if __name__ == "__main__":
    finder = main()
    
    # Example of how to add manual research results:
    print(f"\n" + "="*60)
    print("📝 TO ADD MANUAL RESEARCH RESULTS:")
    print("finder.add_manual_research_results({")
    print("    'CODE1': 'Full Station Name 1',")
    print("    'CODE2': 'Full Station Name 2',")
    print("    # ... add more")
    print("})")
    print("finder.generate_updated_station_database()") 