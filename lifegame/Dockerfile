FROM python:3.12-slim

WORKDIR /app

# Copy the entire package directory
COPY . /app/

# Install poetry
RUN pip install --no-cache-dir poetry

# Install the package
RUN cd /app && \
    poetry build && \
    pip install dist/*.whl

# Create patterns directory with a sample pattern
RUN mkdir -p /app/patterns
RUN echo "000\n010\n001\n111" > /app/patterns/glider.txt

# Set environment variables
ENV TERM=xterm-256color

# Set the entrypoint to the lifegame-run command
ENTRYPOINT ["lifegame-run"]
CMD ["--input", "/app/patterns/glider.txt", "--iterations", "50", "--no-clear"] 