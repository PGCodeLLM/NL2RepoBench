FROM --platform=linux/amd64 ghcr.io/multimodal-art-projection/nl2repobench/fastapi-users:1.0

WORKDIR /workspace

# Ensure PYTHONPATH includes workspace
ENV PYTHONPATH=/workspace:/workspace/src:$PYTHONPATH

# Keep container running for agent/test execution
CMD ["tail", "-f", "/dev/null"]
