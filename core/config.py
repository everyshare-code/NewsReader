import os
from dotenv import load_dotenv
import yaml


class ProjectSettings:
    def __init__(self):
        load_dotenv()

        # 환경 변수 로드
        self.ENVIRONMENT = os.getenv("ENVIRONMENT")
        self.PROJECT_NAME = os.getenv("PROJECT_NAME")
        self.ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS").split(',')

        # 환경별 설정 로드
        self.load_environment_settings()

        # 기본 설정
        self.DEFAULT_CONFIG = {
            "urls": {
                "base": "https://news.naver.com",
                "categories": {
                    "flash": {
                        "url": "/main/list.naver",
                        "params": {
                            "mode": "LSD",
                            "mid": "sec",
                            "sid1": "001"
                        }
                    },
                    "politics": {
                        "url": "/section/100"
                    },
                    "economy": {
                        "url": "/section/101"
                    },
                    "social": {
                        "url": "/section/102"
                    },
                    "life": {
                        "url": "/section/103"
                    },
                    "it": {
                        "url": "/section/105"
                    },
                    "world": {
                        "url": "/section/104"
                    }
                }
            }
        }

    def load_environment_settings(self):
        # 환경별로 설정 값을 로드
        self.HOST = os.getenv(f"{self.ENVIRONMENT.upper()}_SERVER_HOST")
        self.PORT = int(os.getenv(f"{self.ENVIRONMENT.upper()}_SERVER_PORT"))
        self.SERVER_NAME = os.getenv(f"{self.ENVIRONMENT.upper()}_SERVER_NAME")


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.project_settings = ProjectSettings()
        # 노출할 속성들
        self._expose_attributes()

    def _expose_attributes(self):
        for settings in (self.project_settings,):
            for attr, value in settings.__dict__.items():
                setattr(self, attr, value)


settings = Settings()
