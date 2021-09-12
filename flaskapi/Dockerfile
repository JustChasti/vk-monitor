FROM python:3
WORKDIR /flaskapi
COPY /flaskapi/requirements.txt /flaskapi
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY /flaskapi /flaskapi
CMD ["flask", "run"]