import socket
import os
import time
from flask import Flask, request, jsonify, render_template
import sqlite3
import threading
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, storage, db

# cred = credentials.Certificate("credentials.json")
# firebase_admin.initialize_app(cred, {"storageBucket": "pbl4-09092003.appspot.com"})

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "pbl4-09092003.appspot.com",
    "databaseURL": "https://pbl4-09092003-default-rtdb.firebaseio.com"
})

def get_link_from_database():
    db_ref = db.reference('web_blocks')
    data = db_ref.get()
    return data

def save_links_to_file(links, file_path):
    with open(file_path, 'a') as file:
        for entry_key, entry_value in links.items():
            link = entry_value.get('link', '')
            link_without_https = link.replace('https://', '')
            file.write(f"127.0.0.1 {link_without_https}\n")

links_data = get_link_from_database()
# save_links_to_file(links_data, 'C:/Windows/System32/drivers/etc/host')
save_links_to_file(links_data, 'D:/Semeter 5/PBL4/PBL/test.txt')
