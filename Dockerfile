FROM python:3.9.0

COPY * .

RUN pip install requests flask

EXPOSE 3000

CMD ["python", "-u", "main.py"]