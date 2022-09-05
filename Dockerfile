FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /test_task
COPY . /test_task

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py" ]
CMD ["runserver", "0.0.0.0:8000"]