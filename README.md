# 🎮 BattleArena Kubernetes - Production-Ready Gaming Platform

A complete, production-ready multiplayer gaming platform deployed on Kubernetes with comprehensive scaling and high availability capabilities.

## 🗺️ Learning Roadmap

This project is structured as a progressive learning path for Kubernetes:

### **Step 1: Kubernetes Basics (`k8s-demo/`)**
Start here to learn fundamental Kubernetes concepts:
- Basic Pods and Deployments
- Services (ClusterIP, LoadBalancer)
- Container networking and service discovery
- Hands-on examples with simple applications

**Location:** `k8s-demo/` folder  
**See:** `k8s-demo/readme.md` for detailed instructions

### **Step 2: Local Kubernetes Deployment (`k8s/`)**
Deploy the full BattleArena application on a local Kubernetes cluster using Kind:
- Multi-replica Deployments
- Persistent Volumes (PVCs)
- ConfigMaps and Secrets
- Service discovery and load balancing
- Health checks and resource management

**Location:** `k8s/` folder  
**See:** `k8s/README.md` for detailed instructions  
**Cluster:** Local Kind cluster

### **Step 3: Cloud Deployment (`k8s_cloud/`)**
Deploy to Google Kubernetes Engine (GKE) for production:
- Cloud-native deployments
- Multi-platform container images
- LoadBalancer services
- Production-ready configurations

**Location:** `k8s_cloud/` folder  
**See:** `k8s_cloud/README.md` for GKE-specific instructions

---

## 🚀 Quick Start (10 minutes)

### **Option 1: Local Kubernetes (Kind)**
```bash
# 1. Create Kind cluster
kind create cluster --config kind-config.yaml

# 2. Deploy to Kubernetes
kubectl apply -f k8s/

# 3. Wait for deployment
kubectl wait --for=condition=available --timeout=300s deployment --all -n battlearena

# 4. Access the API
kubectl port-forward -n battlearena svc/battlearena-api-service 8000:8000
open http://localhost:8000/docs
```

### **Option 2: Cloud Deployment (GKE)**
```bash
# 1. Build and push images to Docker Hub
docker buildx build --platform linux/amd64,linux/arm64 -t your-username/battlearena-api:latest --push .

# 2. Deploy to GKE
kubectl apply -f k8s_cloud/

# 3. Get LoadBalancer IP
kubectl get svc battlearena-api-service -n battlearena
```

**That's it!** You now have a production-ready gaming platform running on Kubernetes! 🎉

---

## 📚 What You're Learning

This project teaches you:

### **Kubernetes Fundamentals**
- **Deployments**: Multi-replica application scaling
- **StatefulSets**: Stateful workloads with persistent storage
- **Services**: Service discovery and load balancing
- **ConfigMaps & Secrets**: Configuration and credential management
- **Persistent Volumes**: Data persistence across pod restarts

### **Production Operations**
- **High Availability**: Multi-replica deployments with health checks
- **Scaling**: Horizontal pod scaling and manual scaling
- **Service Discovery**: Internal networking with DNS-based service discovery
- **Load Balancing**: External and internal load balancing

### **DevOps Best Practices**
- **Infrastructure as Code**: Kubernetes manifests for reproducible deployments
- **Container Orchestration**: Managing containerized applications at scale
- **Configuration Management**: ConfigMaps and Secrets for application settings
- **Security**: Secrets management and resource limits

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                          │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   API Pods      │    │   PostgreSQL    │    │  Simulator  │ │
│  │   (3 replicas)  │◄──►│   Deployment    │    │    Pod      │ │
│  │                 │    │   + PVC         │    │             │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│           │                       │                   │        │
│           ▼                       ▼                   ▼        │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │   API Service   │    │   DB Service    │                    │
│  │  (LoadBalancer) │    │  (ClusterIP)    │                    │
│  └─────────────────┘    └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Components**

1. **BattleArena API** (Kubernetes Deployment)
   - 3 replicas for high availability
   - REST API with 10+ endpoints
   - Automatic health checks and restart policies
   - LoadBalancer service for external access

2. **PostgreSQL Database** (Kubernetes Deployment)
   - Persistent storage with PVC
   - Health checks and backup capabilities
   - Data persistence across pod restarts

3. **Traffic Simulator** (Deployment)
   - Generates realistic gaming traffic
   - Automatically seeds database with test players
   - Configurable simulation modes
   - Tests system under load

---

## 📊 Kubernetes Resources

### **Deployments**

| Resource | Type | Purpose | Replicas |
|----------|------|---------|----------|
| `battlearena-api` | Deployment | API server | 3 |
| `postgres` | Deployment | Database | 1 |
| `battlearena-simulator` | Deployment | Traffic generator | 1 |

### **Services & Networking**

| Service | Type | Purpose | Port |
|---------|------|---------|------|
| `battlearena-api-service` | NodePort/LoadBalancer | External API access | 80→8000 |
| `postgres-service` | ClusterIP | Database access | 5432 |

### **Storage & Configuration**

| Resource | Type | Purpose |
|----------|------|---------|
| `postgres-pvc` | PersistentVolumeClaim | Database storage |
| `battlearena-config` | ConfigMap | Application settings |
| `battlearena-secret` | Secret | Database credentials |

---

## 🔌 API Endpoints

### **Statistics & Analytics**
- `GET /api/stats/players` - Player engagement metrics
- `GET /api/stats/matches` - Match performance & crash rates  
- `GET /api/stats/revenue` - Revenue analytics
- `GET /api/leaderboard` - Top players ranking

### **Player Management**
- `POST /api/players/register` - Register new player
- `POST /api/players/login` - Record player login
- `GET /api/players/{id}` - Get player details

### **Match Management**
- `POST /api/matches/start` - Start new match
- `POST /api/matches/complete` - Complete match with results
- `POST /api/matches/crash` - Handle server crashes

### **Business Operations**
- `POST /api/transactions/create` - Process purchases
- `POST /api/system/event` - Log system events

### **System Health**
- `GET /health` - Health check with database connectivity

---

## 🎯 Key Features

### **Production-Ready Kubernetes**
- **High Availability**: 3-replica API deployment with health checks
- **Persistent Storage**: PVC for database durability
- **Service Discovery**: Internal networking with DNS-based service discovery
- **Load Balancing**: External LoadBalancer/NodePort for public access
- **Auto-Recovery**: Automatic pod restart on failures
- **Health Checks**: Kubernetes-native liveness and readiness probes

### **Scalability & Performance**
- **Horizontal Scaling**: Easy replica scaling with `kubectl scale`
- **Resource Management**: CPU and memory limits for optimal resource usage
- **Load Testing**: Built-in traffic simulator for performance testing
- **Multi-Platform**: Support for both local (Kind) and cloud (GKE) deployments

---

## 🛠️ Kubernetes Development Workflow

### **Local Kubernetes (Kind)**

```bash
# Create Kind cluster
kind create cluster --config kind-config.yaml

# Deploy application
kubectl apply -f k8s/

# View pod status
kubectl get pods -n battlearena

# View logs
kubectl logs -n battlearena -l app=battlearena-api

# Scale API replicas
kubectl scale deployment battlearena-api --replicas=5 -n battlearena
```

### **Cloud Deployment (GKE)**

```bash
# Build multi-platform images
docker buildx build --platform linux/amd64,linux/arm64 \
  -t your-username/battlearena-api:latest --push .

# Deploy to GKE
kubectl apply -f k8s_cloud/

# Get external IP
kubectl get svc battlearena-api-service -n battlearena
```

### **Testing the System**

```bash
# Health check
curl http://localhost:8000/health

# Player statistics
curl http://localhost:8000/api/stats/players | jq

# Register a new player
curl -X POST http://localhost:8000/api/players/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","level":1}'

# View API documentation
open http://localhost:8000/docs
```

---

## 🔧 Deployment Operations

### **Scaling Operations**

```bash
# Scale API replicas
kubectl scale deployment battlearena-api --replicas=5 -n battlearena

# Update application
kubectl set image deployment/battlearena-api \
  api=your-username/battlearena-api:v2.0 -n battlearena

# Rolling restart
kubectl rollout restart deployment/battlearena-api -n battlearena
```

### **Operations & Debugging**

```bash
# View logs
kubectl logs -f deployment/battlearena-api -n battlearena

# Check resource usage
kubectl top pods -n battlearena

# View events
kubectl get events -n battlearena

# Port-forward for local access
kubectl port-forward -n battlearena svc/battlearena-api-service 8000:8000
```

---

## 🎮 Understanding the Simulator

The simulator creates realistic gaming traffic:

### **Traffic Patterns**
- **Auto-Seeding**: Automatically creates 1000+ test players on startup
- **Player Logins**: Simulates user sessions with realistic patterns
- **Match Events**: Creates and completes matches with various outcomes
- **Transactions**: Generates in-game purchases with failure simulation
- **System Events**: Logs errors and activities for debugging

### **Simulation Modes**
- **Normal**: Balanced traffic (default)
- **Slow**: Reduced load for debugging
- **Stress**: 5x traffic for load testing
- **Tournament**: 10x traffic for stress testing

### **Realistic Behavior**
- **Time-based Patterns**: Peak hours (6PM-11PM) with higher traffic
- **Failure Simulation**: 1% transaction failures, 2% match crashes
- **Player Progression**: Level advancement and point accumulation

---

## 🔧 Customization Guide

### **Adding New Endpoints**

Edit `app/api.py`:
```python
@app.get("/api/your-endpoint")
def your_endpoint(db: Session = Depends(get_db)):
    # Your logic here
    return {"message": "Hello from Kubernetes!"}
```

### **Modifying Kubernetes Resources**

Edit deployment files in `k8s/` or `k8s_cloud/`:
```yaml
# Scale replicas
spec:
  replicas: 5

# Add environment variables
env:
- name: NEW_VAR
  value: "new_value"
```

### **Customizing Resource Limits**

Edit deployment files to adjust resource requests and limits:
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "200m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

---

## 🐛 Troubleshooting

### **Common Issues**

**Pods not starting:**
```bash
# Check pod status
kubectl get pods -n battlearena

# Describe pod issues
kubectl describe pod <pod-name> -n battlearena

# Check logs
kubectl logs <pod-name> -n battlearena
```

**Services not accessible:**
```bash
# Check service status
kubectl get svc -n battlearena

# Test service connectivity
kubectl exec -it <pod-name> -n battlearena -- curl http://battlearena-api-service:8000/health
```

**Database connection issues:**
```bash
# Check database pod
kubectl get pods -n battlearena -l app=postgres

# Check database logs
kubectl logs -n battlearena -l app=postgres

# Test database connectivity
kubectl exec -it <api-pod> -n battlearena -- psql -h postgres-service -U admin -d battlearena
```

**LoadBalancer not getting IP:**
```bash
# Check service status
kubectl get svc battlearena-api-service -n battlearena

# Check events
kubectl get events -n battlearena --sort-by=.metadata.creationTimestamp
```

---

## 📚 Learning Resources

### **Kubernetes Fundamentals**
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [Kubernetes Tutorials](https://kubernetes.io/docs/tutorials/)

### **Production Operations**
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)
- [Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

---

## 🎓 What You've Built

This Kubernetes deployment demonstrates:

✅ **Production-Ready Infrastructure**: Multi-replica deployments with health checks  
✅ **High Availability**: Automatic failover and recovery  
✅ **Scalability**: Horizontal scaling and load balancing  
✅ **Configuration Management**: ConfigMaps and Secrets for application settings  
✅ **Security**: Secrets management and resource limits  
✅ **DevOps Practices**: Infrastructure as code and automated deployments  

---

## 🚀 Next Steps

### **Immediate Actions**
1. **Start with Basics**: Explore `k8s-demo/` to understand fundamental concepts
2. **Deploy Locally**: Use Kind to deploy the full application
3. **Test Scaling**: Scale replicas and observe behavior
4. **Deploy to Cloud**: Try GKE deployment with LoadBalancer

### **Learning Extensions**
1. **Add CI/CD**: Implement GitLab CI/CD for automated deployments
2. **Implement Security**: Add network policies and RBAC
3. **Add Caching**: Implement Redis for performance optimization
4. **Add StatefulSets**: Convert PostgreSQL to StatefulSet for better state management

### **Advanced Topics**
1. **Service Mesh**: Implement Istio for advanced networking
2. **GitOps**: Use ArgoCD for Git-based deployments
3. **Multi-Cluster**: Deploy across multiple regions
4. **Machine Learning**: Add ML workloads to the cluster

---

## 📄 Project Structure

```
BattleArena_Kubernets/
├── app/                    # FastAPI application
│   ├── api.py             # Main API with all endpoints
│   ├── models.py          # Database models (5 tables)
│   ├── schemas.py         # Request/response validation
│   ├── database.py        # Database connection
│   └── config.py          # Configuration management
├── simulator/             # Traffic simulation
│   └── simulator.py       # Main simulator logic (includes auto-seeding)
├── k8s-demo/              # Step 1: Kubernetes learning examples
│   ├── k8s_deployment.yaml # Basic deployment example
│   ├── ClusterIP.yaml     # Service example
│   ├── LoadBalancer.yaml  # LoadBalancer example
│   ├── curl-pod.yaml      # Testing pod
│   └── readme.md          # Learning guide
├── k8s/                   # Step 2: Local Kubernetes manifests (Kind)
│   ├── 00-namespace.yaml  # Namespace creation
│   ├── 01-configmap.yaml  # Application configuration
│   ├── 02-secret.yaml     # Database credentials
│   ├── 03-postgres-pvc.yaml # Persistent volume claim
│   ├── 04-postgres-deployment.yaml # PostgreSQL Deployment
│   ├── 05-api-deployment.yaml # API Deployment (3 replicas)
│   └── 06-simulator-deployment.yaml # Simulator Deployment
├── k8s_cloud/             # Step 3: Cloud Kubernetes manifests (GKE)
│   ├── 00-namespace.yaml  # Namespace creation
│   ├── 01-configmap.yaml  # Application configuration
│   ├── 02-secret.yaml     # Database credentials
│   ├── 03-postgres-pvc.yaml # Persistent volume claim
│   ├── 04-postgres-deployment.yaml # PostgreSQL Deployment
│   ├── 05-api-deployment.yaml # API Deployment (Docker Hub images)
│   ├── 06-simulator-deployment.yaml # Simulator Deployment
│   └── README.md          # GKE deployment guide
├── kind-config.yaml       # Kind cluster configuration
└── requirements.txt       # Python dependencies
```

---

## 🎯 Success Criteria

After working with this project, you should understand:

- ✅ How to deploy applications on Kubernetes
- ✅ Kubernetes resource types (Deployments, Services, PVCs)
- ✅ Service discovery and load balancing
- ✅ Persistent storage with PVCs
- ✅ Configuration and secrets management
- ✅ Health checks and resource management
- ✅ Scaling and high availability concepts
- ✅ Production-ready deployment patterns

---

**🎉 Congratulations! You now have a solid foundation in Kubernetes and production operations!**

For questions or issues, check the troubleshooting section or explore the Kubernetes manifests - they're designed to be educational and well-documented.