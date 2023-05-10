FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# WORKDIR /app

# COPY ./requirements.txt requirements.txt
# COPY ./.env ./.env
COPY ./events_api .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "5000"]
