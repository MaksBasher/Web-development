FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/VIRTUAL_ENV
RUN python - m venv $VIRTUAL_ENV
ENV PATH="/$VIRTUAL_ENV/bin:$PATH"

ENV APP-HOME=/app 

RUN mkdir $APP-HOME

RUN mkdir $APP-HOME/static

WORKDIR $APP-HOME

EXPOSE 8000

COPY requirements.txt $APP-HOME/requirements.txt

RUN pip install -r requirements.txt

COPY . $APP-HOME/