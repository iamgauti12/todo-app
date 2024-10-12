# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@34.148.187.129/myappdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
