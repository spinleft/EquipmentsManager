# -*- coding : utf-8 -*-
# coding: utf-8

from flask import *
from flask_wtf import FlaskForm
from wtforms import *
import pymysql

app = Flask(__name__)
app.config.from_object('config')

db = pymysql.connect(
    host="192.168.1.138",
    user="root",
    password = "fermi123456",
    database="equipments",
    charset="utf8")

from app import views