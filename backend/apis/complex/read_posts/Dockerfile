FROM python:3-slim


WORKDIR /usr/src/app

COPY ./read_posts/requirements.txt ./

COPY read_posts/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./read_posts/*.py ./

COPY ./read_posts/read_posts.py ./invokes.py ./
CMD [ "python", "./read_posts.py" ]
