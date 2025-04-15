# python runtime
FROM python:3.11

WORKDIR /app/src

COPY ./requirements.txt /app/requirements.txt

# install requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy all docs in /src into /app/src  
COPY ./src /app/src

# setting entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/app/src

ENTRYPOINT ["/entrypoint.sh"]
