FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# WORKDIR /app

# COPY ./requirements.txt requirements.txt
# COPY ./.env ./.env
COPY . .
RUN pip install -r requirements.txt

EXPOSE 7000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "7000"]
