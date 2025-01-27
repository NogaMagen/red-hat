FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PYTHONPATH=/src
WORKDIR /src
COPY ../requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./src /src
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
