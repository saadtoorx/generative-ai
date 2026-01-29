import requests
import json

def test_extraction():
    url = "http://localhost:8000/extract/"
    note = "Patient presents with severe headache and sensitivity to light. Diagnosis: Migraine. Prescribed Ibuprofen. Follow up in 2 weeks."
    
    print(f"Sending note: {note}")
    
    try:
        response = requests.post(url, data={"note": note})
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            raw_structured = data.get("structured", "")
            print(f"\nRaw 'structured' field from backend:\n{raw_structured!r}")
            
            try:
                parsed = json.loads(raw_structured)
                print(f"\nSuccessfully parsed JSON: {parsed}")
            except json.JSONDecodeError as e:
                print(f"\nFAILED to parse JSON: {e}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_extraction()
