FROM python:3.6.5

ENV APP_DIR /usr/src/poi_setup/

# Copy the the db files and the pipfile to the working directory
COPY Pipfile $APP_DIR
COPY Pipfile.lock $APP_DIR
COPY db/setup $APP_DIR

WORKDIR $APP_DIR

# TODO: This shouldn't have to use pipenv since it is already running inside a container.
#		At the moment pipenv is used just to make sure it uses the version of psycopg2
#		as the other parts of the system
RUN pip install pipenv
RUN pipenv install psycopg2

CMD ["pipenv", "run", "python3", "runSetupFiles.py"]
