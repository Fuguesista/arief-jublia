from model.scheduller_mailler.scheduller_mailler import *
from flask import Flask, render_template
from config.read_config import read_config

app = Flask(__name__)

data_config = read_config("config/base_config.ini")
