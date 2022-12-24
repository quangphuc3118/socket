import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []

def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"Tin nhắn gửi từ {username} trống")
def send_message_to_client(client, message):
    client.sendall(message.encode())
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)
def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} đã thêm vào đoạn chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Tên người dùng máy khách trống")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"chạy máy chủ trên {HOST} {PORT}")
    except:
        print(f"không thể kết nối tới {HOST} {PORT}")
    server.listen(LISTENER_LIMIT)
    while 1:

        client, address = server.accept()
        print(f"kết nối thành công với{address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()