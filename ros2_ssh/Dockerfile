# Dockerfile
FROM ros:humble-ros-base

# Install OpenSSH server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:ros2password' | chpasswd && \
    sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 2222

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]
