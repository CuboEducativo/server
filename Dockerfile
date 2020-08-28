FROM python:3.7

RUN pip install poetry

RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib environs numpy pandas flask

ADD /app /app

# copy credentials
ADD credentials.json credentials.json

# copy env
ADD .env .env

# copy token
ADD token.pickle token.pickle

# cloud run environments
ENV PORT 8080
ENV HOST 0.0.0.0

ENTRYPOINT ["python"]
CMD ["app/quickstart.py"]

