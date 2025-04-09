# python runtime
FROM python:3.11

WORKDIR /app/src

COPY ./requirements.txt /app/requirements.txt

# install requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy all docs in /src into /app/src  
COPY ./src /app/src

ENV PYTHONPATH=/app/src

# start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
