# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:&jCP1_nseKFEm2Q`@34.130.250.127/todo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
