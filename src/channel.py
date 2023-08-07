import json
from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""
    url = 'https://www.youtube.com/'
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.channel_data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.id = [x['id'] for x in self.channel_data['items']][0]
        self.title = [x['snippet']['title'] for x in self.channel_data['items']][0]
        self.description = [x['snippet']['description'] for x in self.channel_data['items']][0]
        self.url = self.url + [x['snippet']['customUrl'] for x in self.channel_data['items']][0]
        self.subscriberCount = [x['statistics']['subscriberCount'] for x in self.channel_data['items']][0]
        self.video_count = [x['statistics']['videoCount'] for x in self.channel_data['items']][0]
        self.view_count = [x['statistics']['viewCount'] for x in self.channel_data['items']][0]

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        return int(self.subscriberCount) == int(other.subscriberCount)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_data, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, name_file):
        with open(name_file, 'w', encoding='utf-8') as file:
            data = {
                'id канала': self.id,
                'название канала': self.title,
                'описание канала': self.description,
                'ссылка на канал': self.url,
                'количество подписчиков': self.subscriberCount,
                'количество видео': self.video_count,
                'общее количество просмотров': self.view_count,
            }
            json.dump(data, file, indent=2, ensure_ascii=False)
