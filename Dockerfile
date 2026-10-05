FROM python:3.12-slim as build
WORKDIR /myapp
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim
WORKDIR /myapp
RUN useradd appuser
COPY app.py .
COPY --from=build /install /usr/local
USER appuser
CMD ["python", "app.py"]
