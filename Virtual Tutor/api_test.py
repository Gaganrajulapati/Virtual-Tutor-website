import requests

BASE_URL = "http://localhost:5000"

def test_get_videos():
    url = f"{BASE_URL}/api/videos"
    response = requests.get(url)
    print("GET /api/videos status:", response.status_code)
    print("Response JSON:", response.json())

def test_rate_video():
    url = f"{BASE_URL}/api/rate"
    payload = {
        "video_id": "dQw4w9WgXcQ",
        "rating": 5
    }
    response = requests.post(url, json=payload)
    print("POST /api/rate status:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    print("Testing GET /api/videos")
    test_get_videos()
    print("\nTesting POST /api/rate")
    test_rate_video()
