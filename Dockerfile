FROM python:3.12-slim AS build

WORKDIR /myapp

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /myapp

RUN useradd --create-home appuser

COPY . .

COPY --from=build /install /usr/local

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
