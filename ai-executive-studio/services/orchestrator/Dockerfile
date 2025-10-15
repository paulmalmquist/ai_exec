FROM python:3.12-slim
WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=false
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry==1.7.1 && poetry install --no-root --only main
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
