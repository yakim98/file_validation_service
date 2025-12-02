FROM python:3.13
WORKDIR /file_validation_service
COPY /build/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
CMD ["python", "src/validation_service/raw_validator.py"]