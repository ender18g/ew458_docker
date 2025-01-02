
# Use official ROS 2 Iron base image
FROM ros:humble

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install rosbridge_suite and all related packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-rosbridge-server \
    ros-${ROS_DISTRO}-rosbridge-library \
    ros-${ROS_DISTRO}-rosbridge-msgs \
    && rm -rf /var/lib/apt/lists/*

# Install ROS 2 talker and listener example packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-demo-nodes-cpp \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-teleop-twist-keyboard

RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-irobot-create-msgs


RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Keep the container open for interactive use
CMD ["/bin/bash"]
