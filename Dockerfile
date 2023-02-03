FROM python:3.10

WORKDIR /myapp

RUN pip install -r requirements.txt
RUN pip install -e .


COPY . .
CMD ["sh", "-c", "uvicorn main:app --host=$HOST --port=$PORT"]
