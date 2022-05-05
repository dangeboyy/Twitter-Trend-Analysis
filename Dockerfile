FROM python:3.9

WORKDIR /thesis

COPY requirements.txt STN.xlsx stop_words.txt ./

RUN pip install -r requirements.txt

COPY . /tez

CMD ["python","/tez/tez.py"]