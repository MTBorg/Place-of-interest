FROM python:3.6.5

ENV APP_DIR /usr/src/poi

WORKDIR $APP_DIR

COPY . $APP_DIR

EXPOSE 5000

# Install pipenv and dependencies
RUN pip install pipenv
RUN pipenv install

# Start the server
CMD ["pipenv", "run", "python3", "server/run.py"]