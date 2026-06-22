import urllib.request
import urllib.error

url = "http://localhost:3000"
try:
    with urllib.request.urlopen(url) as response:
        print("Status:", response.status)
        print("Headers:")
        for key, value in response.getheaders():
            print(f"  {key}: {value}")
        print("Body:", response.read().decode('utf-8')[:500])
except urllib.error.HTTPError as e:
    print("HTTPError Status:", e.code)
    print("HTTPError Headers:")
    for key, value in e.headers.items():
        print(f"  {key}: {value}")
    try:
        print("HTTPError Body:", e.read().decode('utf-8')[:500])
    except Exception:
        pass
except Exception as e:
    print("Error:", e)
