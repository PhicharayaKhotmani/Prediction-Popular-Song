from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# ขอ token จาก Spotify
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

# สร้าง header สำหรับการยืนยันตัวตน
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}




########################################################################################################################################################################################################################################
# ค้นหาศิลปินจากชื่อ 
def search_for_artist(token, artist_name, offset=0, limit=50):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit={limit}&offset={offset}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist found")
        return None

    return json_result


# ขอได้ครั้งละ 50 ศิลปิน โดยเริ่มจากตำแหน่งที่ 0
# แค่มี a ในชื่อ ก็จะได้ศิลปินที่มี a ในชื่อ
artists1 = search_for_artist(token, "a")
artists51 = search_for_artist(token, "a", offset=50)

artist_rank = []
# 0-49
if artists1:
    for idx, artist in enumerate(artists1):
        # ตรวจสอบความนิยมของศิลปิน 0 คือน้อยที่สุด 100 คือมากที่สุด
        if artist.get("popularity") >= 50:
            print(f"{idx + 1}: {artist['name']} {artist['popularity']}")
else:
    print("No artists found.")

# 50-99
if artists51:
    for idx, artist in enumerate(artists51, start=51):
        if artist.get("popularity") >= 50:
            print(f"{idx}: {artist['name']} {artist['popularity']}")
else:
    print("No artists found.")
########################################################################################################################################################################################################################################




########################################################################################################################################################################################################################################
# artist_id = result["id"]
# ดึงเพลงของศิลปิน โดยใช้ artist_id
def get_song_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result


# song = get_song_by_artist(token, artist_id)
# for song in song:
#     print(song["name"])
########################################################################################################################################################################################################################################


