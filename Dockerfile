FROM python:3.9.0

COPY * .

RUN pip install requests flask

CMD ["python", "-u", "main.py"]