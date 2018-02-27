# base python
FROM tiangolo/uwsgi-nginx-flask:python3.6

# add requirements and install in root
COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /server

COPY . /server

# expose server port for other containers
EXPOSE 5000