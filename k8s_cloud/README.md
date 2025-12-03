# 🎮 BattleArena - GKE (Google Kubernetes Engine) Deployment

Production-ready deployment of BattleArena on Google Kubernetes Engine (GKE).

## 📋 Overview

This directory contains Kubernetes manifests optimized for deployment on Google Kubernetes Engine (GKE). The configuration uses Docker Hub for container images and includes production-ready settings.

## 🏗️ Architecture

- **Multi-replica API deployment** (3 replicas for high availability)
- **StatefulSet for PostgreSQL** with persistent storage
- **Service discovery** and load balancing
- **Persistent volumes** for database data

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
kubectl wait --for=condition=available --timeout=300s deployment/postgres -n battlearena

# Deploy API
kubectl apply -f 05-api-deployment.yaml

# Deploy simulator
kubectl apply -f 06-simulator-deployment.yaml
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
2. **Backup Strategy**: Implement database backups
3. **Security**: Add network policies and RBAC
4. **Scaling**: Configure horizontal pod autoscaling

---

## 📝 Exercises for Students

Practice what you've learned with these hands-on exercises:

### Exercise 1: Create Three Environments 🌍

Create three separate environments (dev, staging, prod) running the same application:

**Tasks:**
1. Create three namespaces: `battlearena-dev`, `battlearena-staging`, `battlearena-prod`
2. Deploy the application to each namespace
3. Use different ConfigMaps for each environment (e.g., different `LOG_LEVEL`)
4. Verify all three environments are running independently

**Hints:**
```bash
# Create namespaces
kubectl create namespace battlearena-dev
kubectl create namespace battlearena-staging
kubectl create namespace battlearena-prod

# Deploy to each (modify the namespace in manifests or use -n flag)
kubectl apply -f . -n battlearena-dev
```

**Verification:**
```bash
kubectl get pods -n battlearena-dev
kubectl get pods -n battlearena-staging
kubectl get pods -n battlearena-prod
```

---

### Exercise 2: Implement Resource Limits 📊

Configure proper resource requests and limits for production:

**Tasks:**
1. Set memory requests to `256Mi` and limits to `512Mi` for the API
2. Set CPU requests to `200m` and limits to `500m` for the API
3. Apply changes and verify pods are running with new limits
4. Use `kubectl top pods` to monitor actual usage

**Expected outcome:** Pods should run with defined resource boundaries.

---

### Exercise 3: Rolling Update with Zero Downtime 🔄

Practice deploying a new version without downtime:

**Tasks:**
1. Build a new version of the API image (tag it as `v2`)
2. Push to Docker Hub
3. Perform a rolling update
4. Monitor the rollout progress
5. If something goes wrong, rollback to the previous version

**Commands to use:**
```bash
# Update image
kubectl set image deployment/battlearena-api api=<your-image>:v2 -n battlearena

# Watch rollout
kubectl rollout status deployment/battlearena-api -n battlearena

# Rollback if needed
kubectl rollout undo deployment/battlearena-api -n battlearena
```

---

### Exercise 4: Horizontal Pod Autoscaling (HPA) ⚡

Configure automatic scaling based on CPU usage:

**Tasks:**
1. Create an HPA for the API deployment
2. Set min replicas to 2, max to 10
3. Target CPU utilization at 50%
4. Generate load and observe scaling

**Create HPA:**
```bash
kubectl autoscale deployment battlearena-api \
  --cpu=50% \
  --min=2 \
  --max=10 \
  -n battlearena
```

**Monitor:**
```bash
kubectl get hpa -n battlearena -w
```


---

**🎉 Congratulations on completing the Kubernetes learning path!**

You've progressed from basic concepts (`k8s-demo/`) → local deployment (`k8s/`) → cloud production (`k8s_cloud/`). Keep practicing and exploring! 🚀
