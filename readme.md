# Blender AWS Rendering Pipeline

This project consists of a series of Python scripts designed to run on an AWS EC2 GPU instance. The scripts automate the process of importing a 3D model into Blender, applying textures and backgrounds, capturing screenshots from different angles, and rendering a 90-degree animation of the model. The final outputs, including images and video, are uploaded to an S3 bucket.

## Prerequisites

- **AWS EC2 GPU Instance**: Ensure you have an AWS EC2 instance with GPU capabilities set up.
- **Blender**: Installed on the EC2 instance. You can download it from the [Blender website](https://www.blender.org/download/).
- **AWS CLI**: Installed and configured on the EC2 instance for S3 operations.
- **NVIDIA Drivers**: Ensure that the NVIDIA drivers are installed and configured for GPU rendering.

## Setup Instructions

1. **Install Required Software**:
   - Install Blender on your EC2 instance.
   - Install and configure the AWS CLI for S3 access.
   - Ensure NVIDIA drivers are installed for GPU rendering.

2. **Prepare the Environment**:
   - Place the Python scripts in a directory on your EC2 instance.
   - Ensure the S3 bucket is set up to store the input STL files and output images/videos.

3. **Run the Scripts**:
   - **`main.py`**: This script is executed by Blender to import the 3D model, apply textures, set up the scene, and perform the rendering.
   - **`post_process.py`**: Manages the download of STL files from S3, initiates the Blender rendering process, and uploads the results back to S3.

4. **Interact with the Scripts**:
   - The scripts automatically handle the download and upload of files to and from S3.
   - Monitor the console output for progress and any potential errors.

5. **Video Demonstration**: For a visual demonstration of the rendering process, you can watch the video [here](https://youtu.be/uWBjDkOsUuI).

## Script Descriptions

- **`main.py`**: 
  - Configures Blender to use GPU for rendering.
  - Imports the STL file and applies textures and materials.
  - Sets up multiple cameras to capture images from different angles.
  - Renders a 90-degree animation of the model and saves the output.

- **`post_process.py`**:
  - Manages the lifecycle of STL files, including downloading from S3, processing in Blender, and uploading results back to S3.
  - Cleans up local files after processing to maintain a clean environment.

## Additional Information

- The scripts are designed to handle multiple STL files in sequence, processing each one and uploading the results to a specified S3 bucket.
- Ensure that your AWS credentials and permissions are correctly configured to allow access to the necessary S3 buckets.
- The rendering process is optimized for GPU usage, so ensure that your EC2 instance is properly configured to utilize the GPU.

By following these instructions, you should be able to set up and run the Blender rendering pipeline on an AWS EC2 GPU instance successfully. Enjoy creating high-quality renders of your 3D models!
