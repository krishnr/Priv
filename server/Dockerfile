# base python
FROM python:3

# add requirements and install in root
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

# expose server port for other containers
EXPOSE 5000