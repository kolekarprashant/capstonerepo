# FastAPI + Flask Deployment on AWS EC2 (Dockerized)

This project demonstrates deploying a FastAPI backend and Flask frontend on an AWS EC2 Ubuntu instance using Docker.

---

## Project Structure
```
GENAICAPSTONEPROJECT/
│
├── API/                      # FastAPI backend
│   ├── savepdf/              
│   ├── services/             
│   ├── tools/                
│   ├── __init__.py           
│   ├── app.log               
│   ├── cohere_embedding.py   
│   ├── logging_config.py     
│   ├── main.py               
│   ├── Readme.md             
│   └── sqldatabase.py        
│
├── Deployment/               # Deployment documentation & scripts
│   └── README.md             
│
├── Images/                   # Image assets
│
├── pdfiles/                  # PDF storage
│
├── UI/                       # Flask frontend
│   ├── static/               
│   ├── templates/            
│   ├── app.py                
│   └── Readme.md             
│
├── .env                      # Environment variables
├── .gitignore                
├── Dockerfile                
```


## Deployment Setup

### 1. Create Dockerfile for FastAPI and Flask UI
Example **FastAPI Dockerfile**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Example **Flask UI Dockerfile**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

### 2. Create a Repository on GitHub
- Push your local project to GitHub.

---

### 3. Pull Repository on AWS EC2 Ubuntu
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
git clone https://github.com/username/repo.git
cd your-repo
```

---

### 4. Run Docker Containers on AWS EC2
Using individual `docker build` and `docker run`:
```bash
# Build FastAPI container
cd backend
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app

# Build Flask container
cd ../frontend
docker build -t flask-ui .
docker run -d -p 5000:5000 flask-ui
```

Or using `docker-compose`:
```bash
docker-compose up -d --build
```

---

### 5. Access the Applications
- Flask UI: `http://<ec2-public-ip>:5000`
- FastAPI: `http://<ec2-public-ip>:8000`

---

## Notes
- If your EC2 IP changes on restart, associate an **Elastic IP** in AWS.
- Open ports 5000 and 8000 in your EC2 **Security Group**.
- Use a domain name by mapping Elastic IP to your domain's DNS records.
