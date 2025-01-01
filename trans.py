import requests

def get_ip_and_country():
    # Get public IP and country from ipinfo.io
    response = requests.get('https://ipinfo.io')
    data = response.json()
    
    ip_address = data.get('ip')
    country = data.get('country')

    print(f"IP Address: {ip_address}")
    print(f"Country: {country}")

if __name__ == "__main__":
    get_ip_and_country()
