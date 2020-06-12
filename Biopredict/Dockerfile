FROM python:3.7

WORKDIR /bioprodict
COPY ./requirements.txt ./apiapp.py ./
RUN pip install -r requirements.txt
COPY ./app ./app

EXPOSE 5050

CMD ["gunicorn", "-b", ":5050", "--access-logfile", "-", "--error-logfile", "-", "--workers=5", "--threads=2", "apiapp:app"]
