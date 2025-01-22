FROM python:3.11-slim

# Install bash along with other dependencies
RUN apt update && apt install -y \
    bash \
    gcc \
    ghostscript \
    libxml2-dev libxslt1-dev antiword \
    unrtf poppler-utils tesseract-ocr

# Set the working directory
WORKDIR /usr/src/app

# Copy dependencies and install Python requirements
COPY requirements.txt /usr/src/app/
RUN pip install -U pip && \
    pip install -r requirements.txt --no-cache-dir --no-deps --root-user-action=ignore

RUN echo "Using password: $OPENAI_API_KEY"

# Copy the rest of the application code
COPY . /usr/src/app/

# Expose port and set entrypoint
EXPOSE 8000
# ENTRYPOINT ["python", "app.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
