import csv
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Load environment variables
load_dotenv()

# Spotify credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Function to get a token from Spotify
def get_token():
    auth_str = client_id + ":" + client_secret
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()

# Generate token
token = get_token()

# Function to generate authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function to search for a track by URI or name
def search_for_track_by_uri(token, track_uri, limit=1):
    url = f"https://api.spotify.com/v1/tracks/{track_uri.split(':')[-1]}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    if "id" in json_result:
        return json_result
    else:
        print(f"No track found for URI: {track_uri}")
        return None

# Function to get audio features for a track
def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    
    # Debugging output to check response status and content
    print(f"Response Status: {result.status_code}")
    print(f"Response Content: {result.content}")

    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    elif result.status_code == 403:
        print("Forbidden: Access to the audio features is restricted.")
    else:
        print(f"Failed to retrieve audio features. Status Code: {result.status_code}")
    
    return None

# Function to process tracks from the CSV file
def process_csv(input_file, output_file):
    with open(input_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        results = []

        for row in reader:
            print(row)
            track_uri = row["uri"]  # URI from the CSV
            track_name = row["track_name"]
            artist_names = row["artist_names"]
            print(f"Processing: {track_name} by {artist_names}")

            # Search for the track using the URI
            track = search_for_track_by_uri(token, track_uri)

            if track:
                track_id = track["id"]
                track_artist = ", ".join(artist["name"] for artist in track["artists"])

                # Get audio features for the track
                audio_features = get_audio_features(token, track_id)
                print(audio_features)

                if audio_features:
                    # Append the track and audio features to results
                    results.append(
                        {
                            "Rank": row["\ufeffrank"],
                            "Track URI": track_uri,
                            "Artist Names": artist_names,
                            "Track Name": track_name,
                            "Source": row["source"],
                            "Peak Rank": row["peak_rank"],
                            "Previous Rank": row["previous_rank"],
                            "Weeks on Chart": row["weeks_on_chart"],
                            "Streams": row["streams"],
                            "Tempo (BPM)": audio_features["tempo"],
                            "Danceability": audio_features["danceability"],
                            "Energy": audio_features["energy"],
                            "Loudness": audio_features["loudness"],
                            "Key": audio_features["key"],
                        }
                    )

        # Write results to a new CSV file
        with open(output_file, "w", newline="") as out_file:
            fieldnames = [
                "Rank", "Track URI", "Artist Names", "Track Name", "Source", 
                "Peak Rank", "Previous Rank", "Weeks on Chart", "Streams", 
                "Tempo (BPM)", "Danceability", "Energy", "Loudness", "Key"
            ]
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"Results saved to {output_file}.")

# Example usage
input_file = "./charts/regional-th-weekly-2019-01-03.csv"  # Replace with your input CSV file
output_file = "output_audio_features.csv"  # Replace with your desired output CSV file
process_csv(input_file, output_file)
