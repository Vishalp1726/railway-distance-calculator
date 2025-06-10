from find_missing_stations import MissingStationFinder

def add_manual_research_results():
    """Add manually researched station names"""
    
    # Create finder instance
    finder = MissingStationFinder()
    
    # Load existing progress
    import json
    try:
        with open('station_search_progress.json', 'r') as f:
            progress = json.load(f)
        finder.found_stations = progress['found_stations']
        finder.missing_codes = progress['missing_codes']
    except:
        print("⚠️ Could not load previous progress. Starting fresh...")
    
    # Manually researched station names - based on official Indian Railway station codes
    manual_results = {
        'AHMEDABAD': 'AHMEDABAD JUNCTION',
        'AJMER': 'AJMER JUNCTION', 
        'ALLAHABAD': 'PRAYAGRAJ JUNCTION',  # Renamed from Allahabad
        'AMBALA': 'AMBALA CANTT',
        'AMRAVATI': 'AMRAVATI',
        'AMRITSAR': 'AMRITSAR JUNCTION',
        'ANVT': 'ANAND VIHAR TERMINAL',
        'ASANSOL': 'ASANSOL JUNCTION',
        'AURANGABAD': 'AURANGABAD',
        'BELGAUM': 'BELAGAVI',  # Renamed from Belgaum
        'BERHAMPUR': 'BERHAMPUR',
        'BHAGALPUR': 'BHAGALPUR JUNCTION',
        'BHAVNAGAR': 'BHAVNAGAR TERMINUS',
        'BHOPAL': 'BHOPAL JUNCTION',
        'BHUBANESWAR': 'BHUBANESWAR',
        'BIKANER': 'BIKANER JUNCTION',
        'BILASPUR': 'BILASPUR JUNCTION',
        'CHANDIGARH': 'CHANDIGARH',
        'COIMBATORE': 'COIMBATORE JUNCTION',
        'CSMT': 'CHHATRAPATI SHIVAJI MAHARAJ TERMINUS',
        'CUTTACK': 'CUTTACK',
        'DADAR': 'DADAR',
        'DARBHANGA': 'DARBHANGA JUNCTION',
        'DAVANGERE': 'DAVANGERE',
        'DEE': 'DELHI SARAI ROHILLA',
        'DEHRADUN': 'DEHRADUN',
        'DHANBAD': 'DHANBAD JUNCTION',
        'DIBRUGARH': 'DIBRUGARH',
        'DLI': 'OLD DELHI',
        'DR': 'DADAR',
        'DURG': 'DURG',
        'DURGAPUR': 'DURGAPUR',
        'DWARKA': 'DWARKA',
        'ERNAKULAM': 'ERNAKULAM JUNCTION',
        'ERODE': 'ERODE JUNCTION',
        'FARIDABAD': 'FARIDABAD',
        'FDB': 'FARIDABAD NTC',
        'GAYA': 'GAYA JUNCTION',
        'GCT': 'GHAZIPUR CITY',
        'GGN': 'GURGAON',
        'GHAZIABAD': 'GHAZIABAD',
        'GOA': 'MADGAON',  # Main station for Goa
        'GORAKHPUR': 'GORAKHPUR JUNCTION',
        'GULBARGA': 'KALABURAGI',  # Renamed from Gulbarga
        'GUNTUR': 'GUNTUR JUNCTION',
        'GURGAON': 'GURGAON',
        'GUWAHATI': 'GUWAHATI',
        'GWALIOR': 'GWALIOR JUNCTION',
        'GZB': 'GHAZIABAD',
        'HARIDWAR': 'HARIDWAR',
        'HOWRAH': 'HOWRAH JUNCTION',
        'HUBLI': 'HUBBALLI JUNCTION',  # Renamed from Hubli
        'HYDERABAD': 'HYDERABAD DECCAN',
        'INDORE': 'INDORE JUNCTION',
        'JABALPUR': 'JABALPUR',
        'JAIPUR': 'JAIPUR JUNCTION',
        'JALANDHAR': 'JALANDHAR CITY',
        'JAMNAGAR': 'JAMNAGAR',
        'JAMSHEDPUR': 'TATANAGAR JUNCTION',
        'JODHPUR': 'JODHPUR JUNCTION',
        'JORHAT': 'JORHAT TOWN',
        'KALKA': 'KALKA',
        'KALYAN': 'KALYAN JUNCTION',
        'KANNUR': 'KANNUR',
        'KHARAGPUR': 'KHARAGPUR JUNCTION',
        'KOCHI': 'ERNAKULAM JUNCTION',
        'KOLHAPUR': 'KOLHAPUR',
        'KOLKATA': 'HOWRAH JUNCTION',
        'KOTA': 'KOTA JUNCTION',
        'KOTTAYAM': 'KOTTAYAM',
        'KOZHIKODE': 'KOZHIKODE',
        'KURLA': 'KURLA',
        'KURUKSHETRA': 'KURUKSHETRA JUNCTION',
        'KYN': 'KALYAN JUNCTION',
        'LNL': 'KURLA',
        'LTT': 'LOKMANYA TILAK TERMINUS',
        'LUCKNOW': 'LUCKNOW',
        'LUDHIANA': 'LUDHIANA JUNCTION',
        'MADGAON': 'MADGAON',
        'MADURAI': 'MADURAI JUNCTION',
        'MATHURA': 'MATHURA JUNCTION',
        'MUZAFFARPUR': 'MUZAFFARPUR JUNCTION',
        'MYSORE': 'MYSURU JUNCTION',  # Renamed from Mysore
        'NAGPUR': 'NAGPUR',
        'NELLORE': 'NELLORE',
        'NZM': 'HAZRAT NIZAMUDDIN',
        'PALAKKAD': 'PALAKKAD JUNCTION',
        'PANVEL': 'PANVEL',
        'PATNA': 'PATNA JUNCTION',
        'PNVL': 'PANVEL',
        'PUNE': 'PUNE JUNCTION',
        'PURI': 'PURI',
        'RAIPUR': 'RAIPUR',
        'RAJAHMUNDRY': 'RAJAHMUNDRY',
        'RAJKOT': 'RAJKOT JUNCTION',
        'RANCHI': 'RANCHI',
        'RATLAM': 'RATLAM JUNCTION',
        'SALEM': 'SALEM JUNCTION',
        'SEALDAH': 'SEALDAH',
        'SECUNDERABAD': 'SECUNDERABAD JUNCTION',
        'SILIGURI': 'SILIGURI JUNCTION',
        'SOLAPUR': 'SOLAPUR',
        'SURAT': 'SURAT',
        'THANE': 'THANE',
        'THRISSUR': 'THRISSUR',
        'TINSUKIA': 'NEW TINSUKIA JUNCTION',
        'TIRUCHIRAPALLI': 'TIRUCHIRAPPALLI',
        'TIRUNELVELI': 'TIRUNELVELI JUNCTION',
        'TIRUPATI': 'TIRUPATI',
        'TNA': 'THANE',
        'UDHAMPUR': 'UDHAMPUR',
        'UJJAIN': 'UJJAIN JUNCTION',
        'VADODARA': 'VADODARA JUNCTION',
        'VARANASI': 'VARANASI JUNCTION',
        'VELLORE': 'VELLORE KATPADI JUNCTION',
        'VIJAYAWADA': 'VIJAYAWADA JUNCTION',
        'VISAKHAPATNAM': 'VISAKHAPATNAM',
        'WARANGAL': 'WARANGAL',
        'YESVANTPUR': 'YESVANTPUR JUNCTION',
        
        # Zone codes - these are railway zones, not stations
        'CR': 'CENTRAL RAILWAY ZONE',
        'ER': 'EASTERN RAILWAY ZONE', 
        'NR': 'NORTHERN RAILWAY ZONE',
        'NW': 'NORTH WESTERN RAILWAY ZONE',
        'SR': 'SOUTHERN RAILWAY ZONE',
        'SW': 'SOUTH WESTERN RAILWAY ZONE',
        'WR': 'WESTERN RAILWAY ZONE'
    }
    
    print(f"🔍 Adding {len(manual_results)} manually researched station names...")
    
    # Add the manual results
    finder.add_manual_research_results(manual_results)
    
    # Generate updated database
    combined_stations = finder.generate_updated_station_database()
    
    print(f"\n🎉 PROCESS COMPLETE!")
    print(f"📊 Total stations in database: {len(combined_stations)}")
    print(f"📁 Updated database saved to: updated_station_database.py")
    
    # Show sample of the combined database
    print(f"\n📋 SAMPLE OF UPDATED DATABASE:")
    sample_codes = ['PN', 'JP', 'SBC', 'NDLS', 'PUNE', 'AHMEDABAD', 'CSMT', 'GUWAHATI']
    for code in sample_codes:
        if code in combined_stations:
            print(f"  {code:8} -> {combined_stations[code]}")
    
    return finder, combined_stations

if __name__ == "__main__":
    finder, database = add_manual_research_results() 