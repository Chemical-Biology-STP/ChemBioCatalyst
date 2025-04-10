# Use the official Miniconda base image
FROM continuumio/miniconda3

# Set working directory in the container
WORKDIR /app

# Copy dependency files first to leverage Docker caching
COPY environment.yml requirements.txt ./

# Create the Conda environment as defined in environment.yml.
# This environment file handles the pip installation via the "-r requirements.txt" directive.
RUN conda env create -f environment.yml

# Update PATH to use the Conda environment's binaries; note the environment name below
ENV PATH /opt/conda/envs/interface/bin:$PATH

# Copy the rest of the application code into the container
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
