FROM python:3
WORKDIR /vkapi
COPY /vkapi/requirements.txt /vkapi
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY /vkapi /vkapi
CMD ["python3", "api.py"]
