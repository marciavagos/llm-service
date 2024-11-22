import docker
import os

def build_and_run_docker(image_name="llm_inference_image", container_name="llm_inference_container"):
    # Initialize Docker client
    client = docker.from_env()

    # Build the Docker image
    print(f"Building Docker image: {image_name}...")
    try:
        client.images.build(path=".", tag=image_name, rm=True)
        print(f"Image '{image_name}' built successfully.")
    except docker.errors.BuildError as e:
        print("Error building the Docker image:", e)
        return
    except docker.errors.APIError as e:
        print("Docker API error:", e)
        return

    # Stop and remove any existing container with the same name
    try:
        existing_container = client.containers.get(container_name)
        print(f"Stopping and removing existing container: {container_name}...")
        existing_container.stop()
        existing_container.remove()
    except docker.errors.NotFound:
        print(f"No existing container with name '{container_name}' found. Proceeding...")
    except docker.errors.APIError as e:
        print("Docker API error while handling existing container:", e)
        return

    # Run the Docker container
    print(f"Running Docker container: {container_name}...")
    try:
        client.containers.run(
            image_name,
            name=container_name,
            runtime="nvidia",  # Use NVIDIA runtime for GPU support
            detach=True,
            ports={"5000/tcp": 5000},  # Map port 5000 on the host to port 5000 in the container
            environment={"SERVER_URL": "http://localhost:5000"},  # Pass environment variables
        )
        print(f"Container '{container_name}' is now running.")
    except docker.errors.ContainerError as e:
        print("Error running the Docker container:", e)
    except docker.errors.APIError as e:
        print("Docker API error while running the container:", e)

if __name__ == "__main__":
    build_and_run_docker()
