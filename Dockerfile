FROM tensorflow/tensorflow:1.13.1-py3


COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT bash start.sh