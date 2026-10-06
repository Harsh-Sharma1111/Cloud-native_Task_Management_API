# Cloud-Native Task Management API

![CI/CD Status](https://img.shields.io/badge/CI%2FCD-Passing-brightgreen) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue) ![AWS](https://img.shields.io/badge/AWS-Deployed-orange)

A modern, cloud-native full-stack web application designed to demonstrate robust DevOps practices, containerization, and automated CI/CD deployment pipelines on Amazon Web Services (AWS).

## 🚀 Tech Stack

* **Frontend:** React.js, Vite, TailwindCSS (Served via Nginx)
* **Backend:** Python, Flask, SQLAlchemy, Gunicorn
* **Database:** MySQL 8.0
* **Containerization:** Docker, Docker Compose
* **CI/CD:** GitHub Actions, Docker Hub
* **Cloud Provider:** Amazon Web Services (AWS)

---

## ☁️ AWS Cloud Infrastructure

This project was deployed entirely on AWS using the Free Tier, heavily focusing on infrastructure-as-code and system administration principles to overcome hardware constraints.

### 1. Amazon EC2 (Elastic Compute Cloud)
* **Usage:** Provisioned a `t3.micro` instance (2 vCPUs, 1 GB RAM) to act as the primary production host.
* **Challenge Overcome:** The limited 1 GB of physical RAM caused Out-Of-Memory (OOM) crashes when attempting to build and run multiple Docker containers simultaneously. 
* **Resolution:** Implemented **2 GB of Virtual RAM (Swap Space)** by allocating space on the root drive and mounting it persistently via `/etc/fstab`.

### 2. Amazon EBS (Elastic Block Store)
* **Usage:** Provided the persistent root block storage for the EC2 instance.
* **Challenge Overcome:** The default 8 GB allocation quickly filled up (`No space left on device`) due to heavy Docker image caching and layering.
* **Resolution:** Performed a live disk expansion, resizing the EBS volume from 8 GB to 20 GB. Utilized Linux system tools (`growpart` and `resize2fs`) to seamlessly expand the filesystem without data loss or extended downtime.

### 3. AWS Security Groups (Virtual Firewall)
* **Usage:** Managed inbound and outbound network traffic to the production server.
* **Configuration:** Carefully configured Custom TCP rules to securely expose only necessary services to the public internet:
  * **Port 22:** Open for secure SSH deployments via GitHub Actions.
  * **Port 3000:** Open to serve the Nginx-hosted React frontend to users.
  * **Port 5000:** Open to allow the frontend UI to communicate with the Python API.

### 4. EC2 User Data & Cloud-Init
* **Usage:** Utilized EC2 instance initialization scripts to recover from "Docker Death Loops".
* **Challenge Overcome:** Docker's `restart: unless-stopped` policy caused the database container to crash the system before the SSH daemon could start, locking out administrative access.
* **Resolution:** Injected a `#cloud-boothook` script via the AWS Console to intercept the boot sequence, force-stopping the Docker daemon early in the boot process to regain SSH control and repair the volume corruption.

---

## ⚙️ Continuous Integration & Deployment (CI/CD)

A robust deployment pipeline was built using **GitHub Actions** to enforce code quality and automate cloud deployments.

### Phase 1: Continuous Integration (CI)
* Triggers automatically on every push to the `main` branch.
* Sets up an isolated Python environment and runs automated unit testing via `pytest`.
* **Sign-off Rule:** Acts as a strict gatekeeper. If any code breaks a test, the CI pipeline fails (turns red) and explicitly blocks the Continuous Deployment pipeline from running, thereby protecting the production server from bad code.

### Phase 2: Continuous Deployment (CD)
* **Build & Publish:** Automatically compiles the React frontend and Flask backend into optimized Docker images, pushing them securely to **Docker Hub**.
* **Remote Deployment:** Uses the `appleboy/ssh-action` to securely SSH into the AWS EC2 production server, pull the latest Docker images, and execute a zero-downtime rolling restart via `docker compose up -d`.
* **Health Verification:** Implements a custom bash loop that continuously pings the backend `/health` endpoint for up to 90 seconds. The deployment is only marked as a success once the server responds with a `200 OK`.

---

## 💻 Local Development Setup

To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Cloud-native-Task-Management-API.git
   cd Cloud-native-Task-Management-API
   ```

2. **Start the containers:**
   ```bash
   docker compose up --build
   ```

3. **Seed the database (First run only):**
   ```bash
   docker exec task_backend python seed.py
   ```

4. **Access the application:**
   * Frontend UI: `http://localhost:3000`
   * Backend API: `http://localhost:5000`

---
*This project was built to demonstrate modern DevOps theory, agile methodologies, and cloud-native architecture patterns.*
