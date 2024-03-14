FROM python:3-slim


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./complex/upload_comment/*.py ./

COPY ./complex/upload_comment/upload_comment.py ./
CMD [ "python", "./upload_comment.py" ]
