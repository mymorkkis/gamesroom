FROM python:3.6-alpine
LABEL maintainer="Max Veasey <mveasey87@gmail.com>"
COPY . /src
WORKDIR /src
RUN pip install pipenv
COPY Pipfile.lock /src/
RUN pipenv install deploy --ignore-pipfile
EXPOSE 5000
CMD ["pipenv", "run", "flask", "run"]
