from ftplib import FTP
import cv2
import time

ftp_server = 'ftp.example.com'
ftp_username = 'USERNAME'
ftp_password = 'PASSWORD'
image_type = '.jpg'

def connect_to_camera(rtsp_url, remote_image_path):
    ftp_connection = FTP(ftp_server) 
    ftp_connection.login(ftp_username, ftp_password)
    ftp_connection.connect()

    if not ftp_connection:
        print("Error: Could not connect to FTP")
        return

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        ftp_connection.quit()
        return

    try:
        while True:
            try:
                if not ftp_connection:
                    print(f"{time.ctime()} Reconnecting to FTP")    
                    ftp_connection.connect()

                ret, frame = cap.read()
    
                if ret:
                    image = cv2.imencode(image_type, frame)[1].tobytes()
                    ftp_connection.storbinary(f"STOR {remote_image_path}", image)
                else:
                    print(f"{time.ctime()} Error: Could not read image from RTSP stream.")    
            except Exception as e:
                print(f"{time.ctime()} Error: {e}")
            
            time.sleep(60)
    except KeyboardInterrupt:
        cap.release()

    ftp_connection.quit()

if __name__ == "__main__":
    connect_to_camera('rtsp://STREAM_URL', 'PATH')
