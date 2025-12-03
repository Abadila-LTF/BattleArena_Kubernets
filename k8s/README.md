# 🏠 BattleArena - Local Kubernetes Deployment (Kind)

This guide walks you through deploying BattleArena on a local Kubernetes cluster using Kind (Kubernetes in Docker).

## 📋 Prerequisites

Before starting, make sure you have completed **Step 1: Kubernetes Basics** (`k8s-demo/`).

### Required Tools
- **Docker**: Running and configured
- **Kind**: Kubernetes in Docker ([Installation Guide](https://kind.sigs.k8s.io/docs/user/quick-start/#installation))
- **kubectl**: Kubernetes CLI ([Installation Guide](https://kubernetes.io/docs/tasks/tools/))

### Verify Installation
```bash
docker --version
kind --version
kubectl version --client
```

---

## 🚀 Deployment Steps

### Step 1: Create the Kind Cluster

From the project root directory (`BattleArena_Kubernets/`):

```bash
# Create cluster with our configuration (1 control-plane + 2 workers)
kind create cluster --config kind-config.yaml

# Verify the cluster is running
kubectl cluster-info --context kind-battlearena
kubectl get nodes
```

**Expected output:**
```
NAME                        STATUS   ROLES           AGE   VERSION
battlearena-control-plane   Ready    control-plane   1m    v1.27.x
battlearena-worker          Ready    <none>          1m    v1.27.x
battlearena-worker2         Ready    <none>          1m    v1.27.x
```

### Step 2: Build and Load Docker Images

Kind uses local Docker images, so we need to build and load them into the cluster:

```bash
# Build the API image
docker build -t battlearena-api:latest -f Dockerfile .

# Build the Simulator image
docker build -t battlearena-simulator:latest -f Dockerfile.simulator .

# Load images into Kind cluster
kind load docker-image battlearena-api:latest --name battlearena
kind load docker-image battlearena-simulator:latest --name battlearena
```

### Step 3: Deploy to Kubernetes

Apply all manifests in order:

```bash
# Option 1: Apply all at once
kubectl apply -f k8s/

# Option 2: Apply step by step (recommended for learning)
kubectl apply -f k8s/00-namespace.yaml      # Create namespace
kubectl apply -f k8s/01-configmap.yaml      # Application config
kubectl apply -f k8s/02-secret.yaml         # Database credentials
kubectl apply -f k8s/03-postgres-pvc.yaml   # Storage for database
kubectl apply -f k8s/04-postgres-deployment.yaml  # PostgreSQL
kubectl apply -f k8s/05-api-deployment.yaml       # API (3 replicas)
kubectl apply -f k8s/06-simulator-deployment.yaml # Traffic simulator
```

### Step 4: Wait for Pods to be Ready

```bash
# Watch pods come up
kubectl get pods -n battlearena -w

# Or wait for all deployments
kubectl wait --for=condition=available --timeout=300s deployment --all -n battlearena
```

**Expected output:**
```
NAME                                    READY   STATUS    RESTARTS   AGE
battlearena-api-xxxxx-xxxxx             1/1     Running   0          1m
battlearena-api-xxxxx-xxxxx             1/1     Running   0          1m
battlearena-api-xxxxx-xxxxx             1/1     Running   0          1m
battlearena-simulator-xxxxx-xxxxx       1/1     Running   0          1m
postgres-0                              1/1     Running   0          2m
```

### Step 5: Access the Application

The Kind cluster is configured to expose port 8000 on your localhost:

```bash
# Test the health endpoint
curl http://localhost:8000/health

# Test the API
curl http://localhost:8000/api/stats/players | jq

# Open API documentation in browser
open http://localhost:8000/docs
```

**Alternative: Port Forward**
```bash
kubectl port-forward -n battlearena svc/battlearena-api-service 8000:80
```

---

## 📁 Manifest Files Explained

| File | Resource | Purpose |
|------|----------|---------|
| `00-namespace.yaml` | Namespace | Isolates all BattleArena resources |
| `01-configmap.yaml` | ConfigMap | Non-sensitive configuration (log level, simulation mode) |
| `02-secret.yaml` | Secret | Sensitive data (database credentials) |
| `03-postgres-pvc.yaml` | PVC | Persistent storage claim for database |
| `04-postgres-deployment.yaml` | StatefulSet + Service | PostgreSQL database with persistent storage |
| `05-api-deployment.yaml` | Deployment + Service | API server (3 replicas) with NodePort |
| `06-simulator-deployment.yaml` | Deployment | Traffic simulator for testing |

---

## 🔍 Useful Commands

### View Resources
```bash
# All resources in namespace
kubectl get all -n battlearena

# Pods with more details
kubectl get pods -n battlearena -o wide

# Services
kubectl get svc -n battlearena

# Persistent volumes
kubectl get pvc -n battlearena
```

### View Logs
```bash
# API logs
kubectl logs -n battlearena -l app=battlearena-api --tail=50

# Follow logs in real-time
kubectl logs -n battlearena -l app=battlearena-api -f

# Simulator logs
kubectl logs -n battlearena -l app=battlearena-simulator -f

# Database logs
kubectl logs -n battlearena -l app=postgres
```

### Scaling
```bash
# Scale API to 5 replicas
kubectl scale deployment battlearena-api --replicas=5 -n battlearena

# Verify scaling
kubectl get pods -n battlearena -l app=battlearena-api
```

### Debugging
```bash
# Describe a pod (shows events and errors)
kubectl describe pod <pod-name> -n battlearena

# Execute command in pod
kubectl exec -it <pod-name> -n battlearena -- /bin/sh

# Check events
kubectl get events -n battlearena --sort-by=.metadata.creationTimestamp
```

---

## 🐛 Troubleshooting

### Pods stuck in `ImagePullBackOff`
Images weren't loaded into Kind:
```bash
kind load docker-image battlearena-api:latest --name battlearena
kind load docker-image battlearena-simulator:latest --name battlearena
```

### Pods stuck in `Pending`
Check if PVC is bound:
```bash
kubectl get pvc -n battlearena
```

### Database connection errors
Wait for PostgreSQL to be ready:
```bash
kubectl wait --for=condition=ready pod -l app=postgres -n battlearena --timeout=120s
```

### API not responding on localhost:8000
Verify NodePort is working:
```bash
kubectl get svc -n battlearena battlearena-api-service
# Should show NodePort 30000
```

---

## 🧹 Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Delete the Kind cluster
kind delete cluster --name battlearena
```

---

## ➡️ Next Step

Once you're comfortable with local deployment, proceed to **Step 3: Cloud Deployment** in `k8s_cloud/README.md` to deploy on Google Kubernetes Engine (GKE).

---

## 📚 Key Concepts Learned

After completing this step, you understand:

- ✅ Creating a local Kubernetes cluster with Kind
- ✅ Building and loading Docker images into Kind
- ✅ Namespaces for resource isolation
- ✅ ConfigMaps for application configuration
- ✅ Secrets for sensitive data
- ✅ PersistentVolumeClaims for data persistence
- ✅ StatefulSets for stateful applications (PostgreSQL)
- ✅ Deployments for stateless applications (API, Simulator)
- ✅ Services for networking (ClusterIP, NodePort)
- ✅ Health checks (liveness and readiness probes)
- ✅ Resource requests and limits

