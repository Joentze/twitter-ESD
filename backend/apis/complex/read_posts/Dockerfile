FROM python:3-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./complex/read_posts/*.py ./

COPY ./complex/read_posts/read_posts.py ./complex/read_posts/invokes.py ./
CMD [ "python", "./read_posts.py" ]
