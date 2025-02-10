# Use the official ROS 2 Humble base image
FROM ros:humble

# Install required dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3-colcon-common-extensions \
    build-essential \
    cmake \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workspace directory
WORKDIR /ros2_ws/build

# Clone the YDLidar SDK repository
RUN git clone https://github.com/YDLIDAR/YDLidar-SDK.git

# Build and install the YDLidar SDK
WORKDIR /ros2_ws/build/YDLidar-SDK
RUN mkdir build && cd build && \
    cmake .. && make -j$(nproc) && make install

# Clone the YDLidar ROS2 driver repository
WORKDIR /ros2_ws/src
RUN git clone -b humble --single-branch https://github.com/YDLIDAR/ydlidar_ros2_driver
# Go to the workspace root
WORKDIR /ros2_ws

# copy the /ros2_ws/params/TG.yaml to yplidar.yaml
RUN cp /ros2_ws/src/ydlidar_ros2_driver/params/TG.yaml /ros2_ws/src/ydlidar_ros2_driver/params/ydlidar.yaml

# Build the ROS2 workspace with optimized memory usage
RUN bash -c "source /opt/ros/humble/setup.bash && \
             colcon build --symlink-install"

# Set up the entrypoint
RUN echo "source /opt/ros/humble/setup.bash && source /ros2_ws/install/setup.bash" >> ~/.bashrc

# Environment variables
ENV ROS_DOMAIN_ID=12
ENV FASTRTPS_DISCOVERY_SERVER=192.168.8.104:11811

# Set up the entrypoint
# Keep the container open for interactive use
CMD ["/bin/bash"]
