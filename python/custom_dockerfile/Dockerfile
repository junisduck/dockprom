FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install requests pymysql 

ENTRYPOINT /bin/bash -c

COPY . .

CMD [ "python", "./url_status_check.py" ]
