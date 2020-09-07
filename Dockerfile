FROM python:3.7

# copy requirements
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

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

