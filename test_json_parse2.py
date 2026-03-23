import json

# Test parsing the JSON response
response_data = '{"faults":[{"branch_id":34,"branch_name":"12500 - KFC Wataneya El Koronfel","camera_name":"KFC-Breading-12500","date_reported":"2026-02-12T14:39:44.970127","description":"gjghj","fault_type":"\\u0643\\u0627\\u0628\\u0644","id":1,"repair_notes":null,"reported_by":"admin","resolved_at":null,"technician_id":2}]}'

try:
    json_data = json.loads(response_data)
    print('SUCCESS: JSON parsed successfully')
    
    # Check the fault data
    if 'faults' in json_data and len(json_data['faults']) > 0:
        fault = json_data['faults'][0]
        print('Fault data:')
        for key, value in fault.items():
            print(f'  {key}: {value}')
            
except Exception as e:
    print('ERROR parsing JSON:', e)
    import traceback
    traceback.print_exc()
