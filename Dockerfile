# Base image for the MQTT subscriber
FROM python

RUN apt-get update

COPY requirements/requirements.txt /mqtt/
RUN pip3 install -r /mqtt/requirements.txt

RUN pip install --upgrade pip

RUN pip install paho-mqtt requests  

COPY mqtt.py /mqtt/

WORKDIR /mqtt

# Define the entry point for the MQTT subscriber
CMD ["python3", "mqtt.py"]

