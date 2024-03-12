FROM python:slim-bullseye

WORKDIR /app

RUN apt-get update && apt install -y libgl1-mesa-glx libglib2.0-0
RUN pip3 install opencv-python

COPY . .

CMD ["python", "cctv_to_ftp.py"]
