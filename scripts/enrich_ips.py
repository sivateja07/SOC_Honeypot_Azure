import pandas as pd
import requests
import time

TOKEN = "23safr232$9q" #Not real token, replace this with your Own.

df = pd.read_csv("query_data.csv")

results = []

for ip in df["IpAddress"].dropna().unique():

    try:
        url = f"https://ipinfo.io/{ip}/json?token={TOKEN}"

        response = requests.get(url)
        data = response.json()

        loc = data.get("loc", "")

        latitude = ""
        longitude = ""

        if "," in loc:
            latitude, longitude = loc.split(",")

        results.append({
            "IpAddress": ip,
            "Network": data.get("org", ""),
            "City": data.get("city", ""),
            "Country": data.get("country", ""),
            "Latitude": latitude,
            "Longitude": longitude
        })

        print(f"Processed {ip}")

        time.sleep(0.5)

    except Exception as e:
        print(f"Error with {ip}: {e}")

geo_df = pd.DataFrame(results)

final_df = df.merge(geo_df, on="IpAddress", how="left")

final_df.to_csv("enriched_attackers.csv", index=False)

print("Finished!")
