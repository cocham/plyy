import csv
import pprint
import os.path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()

# SRC TABLE 전용 모듈
cid = os.getenv('SPOTIFY_KEY')
secret = os.getenv('SPOTIFY_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ko')


# 1. 스포티파이 플레이리스트 링크를 통한 곡 정보 추출
def song_from_plyy(plyy_list):
    #곡 정보 리스트
    playlist_info = []

    #플리 ID 추출
    for plyy_link in plyy_list:
        plyyid = plyy_link.split('playlist/')[1].split('?')[0]
        plyy = sp.playlist_tracks(playlist_id=plyyid)

        for item in plyy['items']:
            t_id = item['track']['id']
            t_name = item['track']['name']
            t_run = item['track']['duration_ms']
            artist = ', '.join([artist['name'] for artist in item['track']['artists']])
            album = item['track']['album']['name']
            img = next((image['url'] for image in item['track']['album']['images'] if image['height'] == 300), None)
            playlist_info.append(
                {
                'track_id':t_id,
                'track': t_name,
                'artist': artist,
                'album': album,
                't_run':t_run,
                'img': f"src: {img}"
            })

    return playlist_info
    
# 트랙 아이디 & 플리 아이디
def song_from_plyy(plyy_list):
    #곡 정보 리스트
    playlist_info = []

    #플리 ID 추출
    for plyy_link in plyy_list:
        plyyid = plyy_link.split('playlist/')[1].split('?')[0]
        plyy = sp.playlist_tracks(playlist_id=plyyid)

        for item in plyy['items']:
            t_id = item['track']['id']
            t_name = item['track']['name']
            playlist_info.append(
                {
                'track_id':f"src_{t_id}",
                'track': t_name,
            })

    return playlist_info
    
# 1-1. 플레이리스트 곡을 csv에 옮기기
# 1-1-1. 겹치는 곡은 csv에 안 넣기 위한 체크 함수
def read_existing_tracks_from_csv(csv_file):
    existing_tracks = set()
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                track_id = row[0]
                existing_tracks.add(track_id)
    return existing_tracks

# 1-1-2. 
def track_to_csv(plyy_list, csv_file):
    
    existing_tracks = read_existing_tracks_from_csv(csv_file)
    
    for plyy_link in plyy_list:
        track_info = []
        
        # 플리 ID 추출
        plyyid = plyy_link.split('playlist/')[1].split('?')[0]
        plyy = sp.playlist_tracks(playlist_id=plyyid)

        for item in plyy['items']:
            t_id = item['track']['id']
            t_name = item['track']['name']
            artist = ', '.join([artist['name'] for artist in item['track']['artists']])
            album = item['track']['album']['name']
            img = next((image['url'] for image in item['track']['album']['images'] if image['height'] == 300), None)
            t_run = item['track']['duration_ms']

            if (t_id) not in existing_tracks:
                track_info.append([t_id,t_name, artist,album,img,t_run])
                existing_tracks.add(t_id)

        if not os.path.isfile(csv_file):
            with open(csv_file, 'w', encoding='utf-8', newline='') as file:
                fwriter = csv.writer(file)
                header = ['id','title', 'artist', 'album', 'img', 'rtime']
                fwriter.writerow(header)

        with open(csv_file, 'a', encoding='utf-8', newline='') as file:
            fwriter = csv.writer(file)
            for x in track_info:
                fwriter.writerow(x)


# 2. csv 파일에서 받아온 곡 정보로 sp.search 후 곡 정보 추출
def song_from_csv(csv_file):
    track_info = []
    src_info = []
    with open(csv_file, 'r', encoding='utf-8', newline='') as file:
        freader = csv.reader(file)
        for row in freader:
                #쿼리로 변환해서 넣기
                track_info.append(row[0] + ' ' + row[1])

    for track in track_info:
        search = sp.search(track,type='track',limit=1,market='KR')
        for item in search['tracks']['items']:
            if 'linked_from' in item:
                t_id = item['linked_from']['id']
            else:
                t_id = item['id']
            t_name = item['name']
            artist = ', '.join([artist['name'] for artist in item['artists']])
            album = item['album']['name']
            t_run = item['duration_ms']
            img = next((image['url'] for image in item['album']['images'] if image['height'] == 640), None)
            src_info.append(
                {
                'src_track_id':t_id,
                'src_title': t_name,
                'src_artist': artist,
                'src_album': album,
                'src_rtime':t_run,
                'src_album_img': f"{img}"
            })
    
    return src_info

# print(sp.playlist(playlist_id='3axAvtVlnfhenoPSfOel70'))
# pprint.pprint(song_from_plyy(['https://open.spotify.com/playlist/3axAvtVlnfhenoPSfOel70?si=66d640cb443b437c']))
# pprint.pprint(song_from_csv('track.csv'))

# 플리 순서: Chill, 나그녀랑친구하재, 스@근한 그루브, 💔
# 플리 순서: Bronze, Gold, Silver
# 플리 순서: "Last Summer Swing Vol. 3 / LL YOON J MIX #12", "24.7.22. Soul, Slowjam", 디개맨래퀴엠
# 플리 순서: 🧪새벽감성💉, 🧇 my_collection.zip 🥐
plyy = ['https://open.spotify.com/playlist/3axAvtVlnfhenoPSfOel70?si=2ef3a33d65b9480c',
        'https://open.spotify.com/playlist/1DqSOvkgRp5jmG7iecz1bG?si=be9fe137abd6417e'
        'https://open.spotify.com/playlist/5yNnbPiURS70jJY7I33Nyv?si=151f2f795e5d4a30',
        'https://open.spotify.com/playlist/7qdPvkneIFxPMAYKYto5xk?si=f7b6474baa264b7f',
        'https://open.spotify.com/playlist/1kFHbWm0DXgc8aU7GQOZs8?si=1cf80547ce4848e3',
        'https://open.spotify.com/playlist/5JBzg4TQLQWDCvgct0hjhe?si=425917b1982d4b33',
        'https://open.spotify.com/playlist/6AhVuKi3LCJxAxO8HjnQ7L?si=a3c7b84e692448c8',
        'https://open.spotify.com/playlist/2AnToV6KbRdWN7B8h7HZMT?si=85fcf5e9f43f41b9',
        'https://open.spotify.com/playlist/0WYoqbLFpR1imUmVxXIysQ?si=982d40c5da404e0f',
        'https://open.spotify.com/playlist/14Mj4hfpnHKieUvU13rTlJ?si=44f6e7d0bd5e45f4',
        'https://open.spotify.com/playlist/5JIwGSpqO8p9xTu2UXNfnu?si=a156f55ee1644338',
        ]

track_to_csv(plyy,'track.csv')

def genre():
    genre = sp.recommendation_genre_seeds()['genres']
    return genre

# print(genre())
# print(sp.search('피 땀 눈물 BTS',type='track',limit=1,market='KR'))

#장르 태그 추출
# print(sp.recommendation_genre_seeds())
