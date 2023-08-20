import isodate
from googleapiclient.discovery import build
import os
from datetime import timedelta

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        # id плейлиста ↓
        self.__playlist_id = playlist_id
        self.channel_of_pl = youtube.playlistItems().list(
            playlistId=self.__playlist_id,
            part='snippet',
            maxResults=1, ).execute()

        # Создаем переменную с индификатором канала ↓
        self.channel_id = self.channel_of_pl['items'][0]['snippet']['videoOwnerChannelId']
        # Создаем переменную с названиями и данными всех плейлистов канала ↓
        self.playlists = youtube.playlists().list(
            channelId=self.channel_id,
            part='contentDetails,snippet',
            maxResults=50, ).execute()

        self.title = [x for x in self.playlists['items'] if x['id'] == playlist_id][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

        # Создаем переменную со списком данных видео из плейлиста
        self.playlist_videos = youtube.playlistItems().list(
            playlistId=self.__playlist_id,
            part='contentDetails',
            maxResults=50, ).execute()
        # Получаем все id видео из плейлиста
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # По Id получаем - кол-во лайков, просмотров, просмотров, комментариев ...
        self.video_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self) -> timedelta:
        """
            Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        time_video = timedelta()

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_video += duration
        return time_video

    def show_best_video(self) -> str:
        """
            Возвращает ссылку на самое популярное
            видео из плейлиста (по количеству лайков)
        """
        sorted_videos = sorted(self.video_response['items'],
                               key=lambda x: int(x['statistics']['likeCount']), reverse=True)

        return f"https://youtu.be/{sorted_videos[0]['id']}"
