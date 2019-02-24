FROM python:3.6.5

ENV APP_DIR /usr/src/poi/


COPY server $APP_DIR/server
COPY db $APP_DIR/db/
COPY Pipfile Pipfile.lock $APP_DIR

EXPOSE 5000

WORKDIR $APP_DIR
# Install pipenv and dependencies
RUN pip install pipenv
RUN pipenv install

# Start the server
CMD ["pipenv", "run", "python3", "server/run.py"]
