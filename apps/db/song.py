import csv
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()

# YouTube API 키
API_KEY = os.getenv('YOUTUBE_KEY')

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_playlist_videos(plyylink):
    video_link = []
    # plyylist에서 ID추출
    plyy_id = plyylink.split('list=')[1].split('&')[0]

    # playlistItems 메서드를 호출해 재생목록에 있는 비디오 ID 추출
    playlist_items = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=plyy_id,
        maxResults=50  # 재생목록의 최대 비디오 개수 (기본 50, 최대 50)
    ).execute()
    
    # videoid를 통해 video 링크 생성
    for item in playlist_items['items']:
        video_id = item['contentDetails']['videoId']
        video_link.append(f'https://www.youtube.com/watch?v={video_id}')

    return video_link

def song(plyy_link,csv_file):
    song_info = []
    song_vids = get_playlist_videos(plyy_link)
    print(song_vids)
    return 0
    count = 0

    if not os.path.isfile(csv_file):
        for row in reader:
            song_info.append({
                'song_cmt':row[0],
                'song_vid':song_vids[count],
                'song_index':count,
                'p_id':row[1],
                'tk_id':row[2]
            })

            count += 1

    # 파일이 존재하지 않는 경우 헤더 추가
    if not os.path.isfile(csv_file):
        with open(csv_file, 'w', encoding='utf-8', newline='') as file:
            fwriter = csv.writer(file)
            header = [
                'cmt',
                'vid',
                'index',
                'p_id',
                'tk_id']
            fwriter.writerow(header)

    with open(csv_file, 'a', encoding='utf-8', newline='') as file:
        fwriter = csv.writer(file)
        for song in song_info:
            fwriter.writerow([song['song_cmt'],song['song_vid'],song['song_index'],song['p_id'],song['tk_id']])

    return song_info


# 플리 순서: Chill, 나그녀랑친구하재, 스@근한 그루브, 💔
# 플리 순서: Bronze, Gold, Silver
# 플리 순서: "Last Summer Swing Vol. 3 / LL YOON J MIX #12", "24.7.22. Soul, Slowjam", 디개맨래퀴엠
# 플리 순서: 🧪새벽감성💉, 🧇 my_collection.zip 🥐
# ['https://youtube.com/playlist?list=PLi5p5mTdWhrinSaqUeFRUDplqej5WW2m9&feature=shared',
#                 'https://youtube.com/playlist?list=PLi5p5mTdWhrhhFOazWoga6WKAlbMJ4RHi&feature=shared',]
playlist_link = [
                'https://youtube.com/playlist?list=PLi5p5mTdWhrg_E3eusRjTpUP8cbbJnWd9&feature=shared'
                ]

# file_names = ['mh_song.csv','sm-SONG.csv','HL_SONG.csv','gn_song.csv']
song_info = []

for i in range(len(playlist_link)) :
    song(playlist_link[i],'song.csv')