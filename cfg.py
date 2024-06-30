import streamlit as st
from PIL import Image
from cores import get_yolo
import os
import shutil
import glob

DATA_PATH = r"data/358131089_1598284357678845_8367029803511623159_n.jpg"
FOLDER_PATH = "data/"

CONF_THRESHOLD = 0.5
IMG_SIZE = 640

SAVE_FOLDER = "save/"
