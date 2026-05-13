# Face Mask Detection System (Microservices Architecture)

A robust, enterprise-grade **Face Mask Detection System** built with a highly decoupled microservices architecture. This project integrates Deep Learning with modern DevOps practices, featuring an **Angular** frontend and a **Python-based** backend orchestrated by **Docker** and **RabbitMQ**.

---

## 🏗️ System Architecture

The system is designed using a **Microservices Architecture** to ensure scalability and independent deployment.

### 🧩 Services Breakdown:
- **API Gateway (Port 8000):** The central entry point for all client requests.
- **Prediction Service (Port 8001):** The AI core. It utilizes a pre-trained **PyTorch** model (`mask_detector_cpu.pth`) to perform real-time mask detection.
- **Image Service (Port 8002):** Manages image processing, uploads, and data handling.
- **Logging Service (Port 8003):** Asynchronously records system activities and detection results via RabbitMQ.
- **Notification Service (Port 8004):** Handles alerts and notifications based on AI findings.
- **RabbitMQ:** The message broker facilitating asynchronous communication between services to ensure non-blocking performance.

---

## 🚀 Tech Stack

- **Artificial Intelligence:** Python, PyTorch, OpenCV, NumPy.
- **Frontend:** Angular, TypeScript, Bootstrap/Tailwind.
- **Containerization:** Docker, Docker Compose.
- **Messaging:** RabbitMQ (Message Broker).
- **Architecture:** Microservices, API Gateway.

---

## 📁 Project Structure

```text
FaceMask_System/
├── AI_Backend/                 # Backend & AI Development
│   ├── face-mask-microservices/ # Containerized Services (Docker Compose)
│   ├── mask_detector_cpu.pth    # Trained PyTorch Model Weights
│   ├── project.ipynb           # Model Training Notebook
│   └── app.py                  # Standalone Testing Module
└── Angular_Frontend/           # UI Application
    ├── src/                    # Angular Source Code
    └── Dockerfile              # Frontend Containerization
```

---

## ⚙️ Setup & Execution

### 1. Run Backend Services (Microservices)
Navigate to the microservices directory and launch the stack:
```bash
cd AI_Backend/face-mask-microservices
docker-compose up --build
```

### 2. Run Frontend (Angular)
In a separate terminal, build and run the frontend container:
```bash
cd Angular_Frontend
docker build -t mask-frontend .
docker run -p 8080:4200 mask-frontend
```

---

## 🧠 Model Details
The AI engine is powered by a MobileNet Deep Learning architecture, trained on a custom
face mask dataset. MobileNet was specifically chosen for its lightweight nature and efficiency,
making it highly optimized for CPU inference within Docker containers. This ensures fast, real-
time detection and high performance without the need for dedicated GPU hardware.
