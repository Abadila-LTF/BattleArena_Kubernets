# 🎮 BattleArena - GKE (Google Kubernetes Engine) Deployment

Production-ready deployment of BattleArena on Google Kubernetes Engine with comprehensive observability stack.

## 📋 Overview

This directory contains Kubernetes manifests optimized for deployment on Google Kubernetes Engine (GKE). The configuration uses Docker Hub for container images and includes production-ready settings.

## 🏗️ Architecture

- **Multi-replica API deployment** (3 replicas for high availability)
- **StatefulSet for PostgreSQL** with persistent storage
- **Service discovery** and load balancing
- **Persistent volumes** for database data
- **Observability stack** (Prometheus, Grafana, Alertmanager)

## 🚀 Quick Start - GKE Deployment

### Prerequisites
- Google Cloud Platform account with GKE enabled
- `gcloud` CLI configured
- Docker Hub account for image storage

### 1. Build and Push Multi-Platform Images to Docker Hub

**IMPORTANT:** GKE nodes run on AMD64 (x86_64) architecture. If you're building on an M1/M2 Mac (ARM64), you MUST build multi-platform images.

```bash
# Build and push multi-platform images
cd /Users/abadila/Desktop/LP2/2-battlearena_k8s
export DOCKERHUB_USERNAME=your-dockerhub-username

# Manual multi-platform build
# First, ensure buildx is set up
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap

# Build and push multi-platform API image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f Dockerfile \
  -t your-dockerhub-username/battlearena-api:latest \
  --push \
  .

# Build and push multi-platform Simulator image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f Dockerfile.simulator \
  -t your-dockerhub-username/battlearena-simulator:latest \
  --push \
  .
```

**⚠️ Common Error:** If you see "no match for platform in manifest", it means you built for the wrong architecture. Always use `--platform linux/amd64,linux/arm64` when building for GKE.

### 2. Create GKE Cluster

```bash
# Create a GKE cluster (adjust as needed)
gcloud container clusters create battlearena-cluster \
  --num-nodes=3 \
  --machine-type=e2-medium \
  --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials battlearena-cluster --zone=us-central1-a
```

### 3. Deploy to GKE

```bash
# Create namespace
kubectl apply -f 00-namespace.yaml

# Create persistent volume claim (adjust storage class for your region)
kubectl apply -f 03-postgres-pvc.yaml

# Apply configurations
kubectl apply -f 01-configmap.yaml
kubectl apply -f 02-secret.yaml

# Deploy PostgreSQL
kubectl apply -f 04-postgres-deployment.yaml

# Wait for database to be ready
kubectl wait --for=condition=available --timeout=300s deployment/postgres-deployment -n battlearena

# Deploy API
kubectl apply -f 05-api-deployment.yaml

# Deploy simulator
kubectl apply -f 06-simulator-deployment.yaml
```

### 4. Set Up Observability

```bash
# Deploy monitoring stack
kubectl apply -f ../../../monitoring/

# Wait for all deployments
kubectl wait --for=condition=available --timeout=300s deployment --all -n battlearena
```

### 5. Access the Application

```bash
# Get the LoadBalancer external IP (may take 1-2 minutes to provision)
kubectl get svc battlearena-api-service -n battlearena -w

# Once you have the external IP, test the API:
EXTERNAL_IP=$(kubectl get svc battlearena-api-service -n battlearena -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "API accessible at: http://$EXTERNAL_IP"

# Test endpoints
curl http://$EXTERNAL_IP/health
curl http://$EXTERNAL_IP/api/stats/players

# Alternative: Port-forward for testing (bypasses LoadBalancer)
kubectl port-forward -n battlearena svc/battlearena-api-service 8000:8000
```

**Note:** The LoadBalancer service type provides a public IP that makes your API accessible from the internet. This is ideal for production deployments.

## 🔧 Configuration

### Update Image Names
Replace `your-dockerhub-username` in the deployment files with your actual Docker Hub username:

```bash
# In 05-api-deployment.yaml and 06-simulator-deployment.yaml
image: your-dockerhub-username/battlearena-api:latest
image: your-dockerhub-username/battlearena-simulator:latest
```

### Database Credentials
Update the secret in `02-secret.yaml` with your database credentials.

### Storage Class
Update `03-postgres-pvc.yaml` to use the appropriate storage class for your GKE zone.

## 📊 Monitoring & Observability

The deployment includes:
- **Prometheus** for metrics collection
- **Grafana** for dashboards and visualization
- **Alertmanager** for alerting

Access points:
- **API**: LoadBalancer IP or port-forward to 8000
- **Grafana**: LoadBalancer IP or port-forward to 3000 (admin/admin123)
- **Prometheus**: LoadBalancer IP or port-forward to 9090

## 🛠️ Operations

### Scaling
```bash
# Scale API replicas
kubectl scale deployment battlearena-api --replicas=5 -n battlearena

# Scale PostgreSQL (StatefulSet)
kubectl scale statefulset postgres-statefulset --replicas=2 -n battlearena
```

### Updates
```bash
# Update images
kubectl set image deployment/battlearena-api api=your-dockerhub-username/battlearena-api:v2.0 -n battlearena

# Rolling restart
kubectl rollout restart deployment/battlearena-api -n battlearena
```

### Monitoring
```bash
# View logs
kubectl logs -f deployment/battlearena-api -n battlearena

# Check resource usage
kubectl top pods -n battlearena

# View events
kubectl get events -n battlearena
```

## 🔒 Security Considerations

1. **Database credentials** should be stored in Google Secret Manager
2. **TLS certificates** should be configured for production
3. **Network policies** should be implemented
4. **RBAC** should be configured for different user roles

## 📈 Production Features

- **High Availability**: Multi-replica deployments
- **Persistent Storage**: StatefulSet with PVC
- **Load Balancing**: Kubernetes services with LoadBalancer
- **Monitoring**: Comprehensive observability stack
- **Scalability**: Horizontal pod autoscaling ready

## 🆘 Troubleshooting

### Common Issues

1. **Images not pulling**: Ensure Docker Hub credentials are configured
2. **PVC not binding**: Check storage class availability in your zone
3. **Services not accessible**: Check LoadBalancer provisioning and firewall rules
4. **Database connection**: Verify secret credentials and service discovery

### Debug Commands
```bash
# Check pod status
kubectl get pods -n battlearena

# Describe deployment issues
kubectl describe deployment battlearena-api -n battlearena

# Check logs
kubectl logs -n battlearena deployment/battlearena-api

# Check events
kubectl get events -n battlearena --sort-by=.metadata.creationTimestamp
```

## 🎯 Next Steps

1. **CI/CD Pipeline**: Set up automated deployment from GitHub/GitLab
2. **Monitoring Alerts**: Configure alerting rules for production
3. **Backup Strategy**: Implement database backups
4. **Security**: Add network policies and RBAC
5. **Scaling**: Configure horizontal pod autoscaling

---

**This GKE deployment provides a production-ready foundation for the BattleArena gaming platform with comprehensive monitoring and observability!** 🚀
