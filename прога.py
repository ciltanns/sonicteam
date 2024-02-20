import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *  
from tkinter.ttk import Combobox 
from openpyxl import load_workbook

from flask import Flask, request, jsonify
import requests
import socket
import threading
import time

root = tk.Tk()
root.title("Защита от DDoS атак")
root.minsize(width=300, height=100)
root.configure(bg='lightblue')
root.geometry("300x300")

def active():
    def redirect():
        app = Flask(__name__)

        @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
        @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def proxy(path):
            url = url_entry.get() + path  
            if request.method == 'GET':
                response = requests.get(url, params=request.args)
            elif request.method == 'POST':
                response = requests.post(url, data=request.form)
            elif request.method == 'PUT':
                response = requests.put(url, data=request.form)
            elif request.method == 'DELETE':
                response = requests.delete(url)

            return response.content, response.status_code, response.headers.items()

        if __name__ == '__main__':
            app.run(debug=True)

    def detect_ddos(threshold):
        # Устанавливаем сокет для прослушивания сетевого трафика
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(("0.0.0.0", 9999))

        # Слушаем сетевой трафик и анализируем количество запросов
        while True:
            data, addr = server_socket.recvfrom(1024)
            
            # Проверяем количество запросов
            if len(data) > threshold:
                redirect()
                # Здесь можно добавить дополнительные действия

    if __name__ == '__main__':
        # Установка порога для обнаружения DDoS атаки
        threshold = 1000  # Это значение можно настроить в зависимости от ожидаемой нормы трафика
        detect_ddos(threshold)

    url_label = tk.Label(text="Введите URL стороннего хоста:")
    url_label.pack()
    url_entry = tk.Entry(root, width=75)
    url_entry.pack()


def analysis():
    # Configuration
    HOST = '127.0.0.1'  # Localhost
    PORT = 12345        # Port to listen on
    RATE_LIMIT = 100    # Maximum number of requests allowed per second

    # Global variables
    request_count = 0
    lock = threading.Lock()

    def handle_connection(client_socket, client_address):
        global request_count
        while True:
            # Increment request count
            with lock:
                request_count += 1

            # Check request rate
            if request_count > RATE_LIMIT:
                break

            # Simulate processing of request
            time.sleep(0.1)  # Simulate processing time

        # Decrement request count
        with lock:
            request_count -= 1

        # Close connection
        client_socket.close()

    def main():
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen()

        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()

            # Start a new thread to handle the connection
            threading.Thread(target=handle_connection, args=(client_socket, client_address)).start()

        # Close the server socket
        server_socket.close()

    if __name__ == "__main__":
        main()


active_button = tk.Button(text="Активировать редирект-защиту", command=active)
active_button.pack()

analysis_button = tk.Button(text="Активировать блок-защиту", command=analysis)
analysis_button.pack()

root.mainloop()
