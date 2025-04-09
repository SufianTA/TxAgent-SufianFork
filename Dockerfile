# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements.txt first (this will be cached unless requirements.txt changes)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your project files into the container
COPY . /app/

# Expose the port for Streamlit
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "txagent_ui.py"]
