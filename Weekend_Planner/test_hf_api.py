import requests
import os

# IMPORTANT: Ensure this token is the *exact* one you copied from Hugging Face
# It's currently hardcoded as in your main.py.
HF_TOKEN = "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" # Your actual token
HF_MODEL = "google/flan-t5-large"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def test_huggingface_api():
    prompt = "Explain the concept of photosynthesis in one sentence."
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 50},
    }

    print(f"--- Starting Hugging Face API Test ---")
    print(f"Target URL: {API_URL}")
    print(f"Headers: {HEADERS}")
    print(f"Payload: {payload}")
    print("-" * 30)

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status() # This will raise an HTTPError for 4xx/5xx responses

        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Raw Text: {response.text}")

        result = response.json()
        if isinstance(result, list) and result and 'generated_text' in result[0]:
            print(f"\n✅ Generated Text: {result[0]['generated_text'].strip()}")
        else:
            print("\n⚠️ Unexpected response format from Hugging Face API.")
            print(f"Full response JSON: {result}")

    except requests.exceptions.HTTPError as http_err:
        print(f"\n❌ HTTP Error occurred: {http_err}")
        print(f"Response Content: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"\n❌ Connection Error: {conn_err}. Check your internet connection or firewall.")
    except requests.exceptions.Timeout as timeout_err:
        print(f"\n❌ Timeout Error: {timeout_err}. The request took too long.")
    except requests.exceptions.RequestException as req_err:
        print(f"\n❌ An unexpected Request Error occurred: {req_err}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

    print("\n--- Test Finished ---")

if __name__ == "__main__":
    test_huggingface_api()