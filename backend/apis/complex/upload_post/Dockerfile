FROM python:3-slim


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./complex/upload_post/*.py ./

COPY ./complex/upload_post/upload_post.py ./
CMD [ "python", "./upload_post.py" ]
