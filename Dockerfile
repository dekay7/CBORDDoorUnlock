FROM python:3.12

COPY requirements.txt .
COPY openDoor.py .
COPY openDoorServer.py .

RUN pip install -r requirements.txt
RUN playwright install-deps
RUN playwright install

EXPOSE 5000

CMD [ "python" , "openDoorServer.py"]