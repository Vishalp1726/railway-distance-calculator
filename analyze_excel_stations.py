import pandas as pd
import json
from complete_api_railway_calculator import CompleteAPIRailwayCalculator

def read_excel_station_codes():
    """Read station codes from Excel file"""
    
    try:
        # Read the Excel file
        excel_file = "Train - 01st Apr 2024 to 31st Mar 2025 (1).xlsx"
        df = pd.read_excel(excel_file, sheet_name="Sheet2")
        
        print("🚂 READING EXCEL FILE WITH STATION CODES")
        print("=" * 60)
        print(f"📁 File: {excel_file}")
        print(f"📊 Sheet: Sheet2")
        print(f"📋 Rows: {len(df)}")
        print(f"🔢 Columns: {list(df.columns)}")
        
        # Show first few rows to understand structure
        print(f"\n📄 SAMPLE DATA:")
        print(df.head())
        
        # Extract unique station codes (assuming they're in a column)
        # Let's try to identify which column contains station codes
        station_codes = set()
        
        for col in df.columns:
            print(f"\n🔍 Analyzing column: {col}")
            unique_values = df[col].dropna().unique()
            print(f"  Unique values count: {len(unique_values)}")
            print(f"  Sample values: {unique_values[:10]}")
            
            # Check if this looks like station codes (short uppercase strings)
            code_like_values = []
            for val in unique_values:
                if isinstance(val, str) and len(val) <= 10 and val.isupper():
                    code_like_values.append(val)
            
            if code_like_values:
                print(f"  Station code-like values: {len(code_like_values)}")
                print(f"  Sample codes: {code_like_values[:10]}")
                station_codes.update(code_like_values)
        
        print(f"\n📊 EXTRACTED STATION CODES:")
        print(f"Total unique codes found: {len(station_codes)}")
        
        return sorted(list(station_codes))
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return []

def analyze_excel_codes_with_database():
    """Analyze Excel codes against our station database"""
    
    # Read codes from Excel
    excel_codes = read_excel_station_codes()
    
    if not excel_codes:
        print("⚠️ No station codes found in Excel file.")
        return
    
    print(f"\n🔍 ANALYZING {len(excel_codes)} CODES AGAINST DATABASE")
    print("=" * 60)
    
    # Initialize calculator
    calculator = CompleteAPIRailwayCalculator()
    
    # Test each code
    found_codes = {}
    missing_codes = []
    
    for i, code in enumerate(excel_codes):
        try:
            full_name = calculator.get_full_station_name(code)
            
            if full_name != code:
                found_codes[code] = full_name
                print(f"✅ {i+1:3}/{len(excel_codes)} {code:10} -> {full_name}")
            else:
                missing_codes.append(code)
                print(f"❌ {i+1:3}/{len(excel_codes)} {code:10} -> NOT FOUND")
                
        except Exception as e:
            missing_codes.append(code)
            print(f"💥 {i+1:3}/{len(excel_codes)} {code:10} -> ERROR: {str(e)}")
    
    # Summary
    found_count = len(found_codes)
    missing_count = len(missing_codes)
    success_rate = (found_count / len(excel_codes)) * 100
    
    print(f"\n📊 ANALYSIS SUMMARY:")
    print(f"Total codes from Excel: {len(excel_codes)}")
    print(f"✅ Found in database: {found_count} ({success_rate:.1f}%)")
    print(f"❌ Missing from database: {missing_count} ({100-success_rate:.1f}%)")
    
    # Save results
    results = {
        'excel_file_analysis': {
            'total_codes': len(excel_codes),
            'found_count': found_count,
            'missing_count': missing_count,
            'success_rate': success_rate
        },
        'found_codes': found_codes,
        'missing_codes': missing_codes,
        'all_excel_codes': excel_codes
    }
    
    with open('excel_station_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: excel_station_analysis.json")
    
    # Show missing codes for manual research
    if missing_codes:
        print(f"\n📋 MISSING CODES FOR MANUAL RESEARCH:")
        print("=" * 60)
        print(f"Please research these {len(missing_codes)} codes:")
        
        # Group by likely categories for easier research
        short_codes = [c for c in missing_codes if len(c) <= 4]
        long_codes = [c for c in missing_codes if len(c) > 4]
        
        if short_codes:
            print(f"\n🔤 SHORT CODES ({len(short_codes)}):")
            for i, code in enumerate(sorted(short_codes), 1):
                print(f"{i:2}. {code}")
        
        if long_codes:
            print(f"\n📝 LONG CODES ({len(long_codes)}):")
            for i, code in enumerate(sorted(long_codes), 1):
                print(f"{i:2}. {code}")
        
        print(f"\n📄 COPY-PASTE FORMAT FOR MANUAL RESEARCH:")
        print("manual_codes = {")
        for code in sorted(missing_codes):
            print(f"    '{code}': 'STATION_NAME_HERE',")
        print("}")
    
    return results

if __name__ == "__main__":
    results = analyze_excel_codes_with_database() 