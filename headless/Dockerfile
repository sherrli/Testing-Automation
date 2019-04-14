FROM python:3

WORKDIR /usr/src/app

COPY testscript.py requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8081

CMD ["python3", "./testscript.py"]
