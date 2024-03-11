FROM python:3-slim


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./complex/read_posts/*.py ./

COPY ./complex/read_posts/read_posts.py ./complex/invokes.py ./
CMD [ "python", "./read_posts.py" ]
