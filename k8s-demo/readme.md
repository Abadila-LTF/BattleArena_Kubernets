# 🎓 Step 1: Kubernetes Basics Demo

This is the first step in learning Kubernetes. Start here before moving to local deployment (`k8s/`) and cloud deployment (`k8s_cloud/`).

---

## 📚 References

- [Kubernetes Docs](https://kubernetes.io/docs/home/)
- [Kind Docs](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kind Installation](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [Kind Alternatives](https://kubernetes.io/docs/tasks/tools/)

---

## 🏗️ Local Kubernetes Cluster using KIND

### Create Using CLI

#### Create a simple cluster (only one master node)

```bash
kind create cluster --name kind-cluster
```

*This will create a Kubernetes cluster on your machine, where nodes are Docker containers*

#### Switching the kubectl context to point to the cluster

```bash
kubectl cluster-info --context kind-kind-cluster
```

#### Interacting with the cluster

```bash
kubectl get node -o wide   # Get the cluster nodes
kubectl get pods -o wide   # Get the cluster pods
kubectl get svc -o wide    # Get the cluster services
```

#### Delete the cluster

```bash
kind delete cluster --name kind-cluster
```

### Create Using Config File

In this folder we have a `kind_cluster_config.yaml` file that creates a cluster with one master node and 3 worker nodes.

#### Create the cluster

```bash
kind create cluster --config kind_cluster_config.yaml --name battlearena
```

#### Switch kubectl context

```bash
kubectl cluster-info --context kind-battlearena
```

#### Interact with the cluster

```bash
kubectl get node -o wide   # Get the cluster nodes
kubectl get pods -o wide   # Get the cluster pods
kubectl get svc -o wide    # Get the cluster services
```

---

## 🎮 Playing with Kubernetes

### Part 1: Pods and Deployments

In the `src/` folder we have a simple Flask backend with one endpoint `/heath` that returns "Up".

#### Build & Tag & Push the Docker image

```bash
docker build -t basic_api .                           # build 
docker run -p 5000:5000 basic_api                     # run locally to test
docker tag basic_api <registry-name>/basic_api:0.0.1  # tag
docker push <registry-name>/basic_api:0.0.1           # push
```

#### Deploy the API with a Deployment

📖 Reference: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

We have a `k8s_deployment.yaml` file that contains a Deployment object:

```bash
kubectl apply -f k8s_deployment.yaml
```

Get pods:

```bash
kubectl get pods
```

---

### Part 2: Testing with a Curl Pod

We have a `curl-pod.yaml` file that creates a pod with curl utility to test our API.

#### Deploy the curl pod

```bash
kubectl apply -f curl-pod.yaml
```

#### Test the API from inside the cluster

```bash
# Get the API pod IP address
kubectl get pods -o wide

# Send request from curl pod to API pod
kubectl exec -it curl-pod -- curl <api-server-pod-ip>:9090

# Or enter the pod shell
kubectl exec -it curl-pod -- sh
curl <api-server-pod-ip>:9090  # from inside the pod
```

**⚠️ Problem:** Pod IP addresses change when pods restart! We need Services to fix this.

---

### Part 3: ClusterIP Service

📖 Reference: [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)

Services provide a **fixed IP address** and **DNS name** for pods.

#### Deploy the ClusterIP Service

```bash
kubectl apply -f ClusterIP.yaml
```

#### Get the service IP

```bash
kubectl get svc
```

#### Test using the service IP (from curl pod)

```bash
kubectl exec -it curl-pod -- curl flask-clusterip-service:9090
```

Now you can use the service name instead of pod IP! 🎉

---

### Part 4: Scaling and Load Balancing Demo

This is where it gets interesting! Let's see how Kubernetes distributes traffic across multiple pods.

#### Step 1: Update the Flask App to Show Pod Info

First, update `src/app.py` to show which pod is responding:

```python
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/heath')
def index():
    pod_name = os.getenv("HOSTNAME")  
    pod_ip = request.remote_addr 
    return f'Hello! This is pod: {pod_name} with IP: {pod_ip}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
```

#### Step 2: Rebuild and Push the Image

```bash
docker build -t <registry-name>/basic_api:0.0.2 .
docker push <registry-name>/basic_api:0.0.2
```

#### Step 3: Update the Deployment Image

```bash
# Update the deployment to use the new image
kubectl set image deployment/flask-app flask-app=<registry-name>/basic_api:0.0.2

# Or edit the deployment directly
kubectl edit deployment flask-app
```

#### Step 4: Scale Up the Deployment

```bash
# Scale to 3 replicas
kubectl scale deployment flask-app --replicas=3

# Watch pods come up
kubectl get pods -w

# Verify all pods are running
kubectl get pods -o wide
```

**Expected output:**
```
NAME                         READY   STATUS    RESTARTS   AGE   IP
flask-app-xxxxx-abc12        1/1     Running   0          10s   10.244.1.5
flask-app-xxxxx-def34        1/1     Running   0          10s   10.244.2.3
flask-app-xxxxx-ghi56        1/1     Running   0          10s   10.244.1.6
```

#### Step 5: Watch Load Balancing in Action! 🔄

Now let's see Kubernetes distribute requests across all pods:

```bash
# From the curl pod, run a loop to see different pods responding
kubectl exec -it curl-pod -- sh

# Inside the pod, run:
while true; do curl -w "\n" flask-clusterip-service:9090/heath; sleep 1; done
```

**Expected output (different pods responding!):**
```
Hello! This is pod: flask-app-xxxxx-abc12 with IP: 10.244.1.5
Hello! This is pod: flask-app-xxxxx-def34 with IP: 10.244.2.3
Hello! This is pod: flask-app-xxxxx-ghi56 with IP: 10.244.1.6
Hello! This is pod: flask-app-xxxxx-abc12 with IP: 10.244.1.5
Hello! This is pod: flask-app-xxxxx-def34 with IP: 10.244.2.3
...
```

**🎉 This demonstrates Kubernetes load balancing!** Each request goes to a different pod.

#### Step 6: Scale Down and Observe

```bash
# Scale down to 1 replica
kubectl scale deployment flask-app --replicas=1

# Now all requests go to the same pod
kubectl exec -it curl-pod -- sh -c "while true; do curl -w '\n' flask-clusterip-service:9090/heath; sleep 1; done"
```

---

### Part 5: LoadBalancer Service (External Access)

ClusterIP only works **inside** the cluster. To access from outside, use LoadBalancer.

📖 Reference: [LoadBalancer Service](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)

#### Deploy the LoadBalancer Service

```bash
kubectl apply -f LoadBalancer.yaml
```

#### Check the service

```bash
kubectl get svc flask-lb-service
```

**Output:**
```
NAME               TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
flask-lb-service   LoadBalancer   10.96.xxx.xx   <pending>     80:31234/TCP   10s
```

**Note:** In Kind, `EXTERNAL-IP` stays `<pending>` because Kind doesn't have a cloud load balancer. In real cloud environments (GKE, EKS, AKS), you get an actual external IP.

#### Access via NodePort (Kind workaround)

In Kind, you can access via the NodePort:

```bash
# Get the NodePort
kubectl get svc flask-lb-service -o jsonpath='{.spec.ports[0].nodePort}'

# Access from your machine (if port mapping is configured in kind config)
curl localhost:<nodeport>/heath
```

---

## 🔄 Service Types Summary

| Service Type | Access From | Use Case |
|--------------|-------------|----------|
| **ClusterIP** | Inside cluster only | Internal communication between pods |
| **NodePort** | Node IP + Port | Development, testing |
| **LoadBalancer** | External IP | Production, cloud environments |

---

## 🧹 Cleanup

```bash
# Delete all resources
kubectl delete -f k8s_deployment.yaml
kubectl delete -f curl-pod.yaml
kubectl delete -f ClusterIP.yaml
kubectl delete -f LoadBalancer.yaml

# Delete the cluster
kind delete cluster --name battlearena
```

---

## ➡️ Next Step

Now that you understand the basics, proceed to **Step 2: Local Deployment** in `../k8s/README.md` to deploy the full BattleArena application!

---

## 📝 Key Concepts Learned

- ✅ Creating Kubernetes clusters with Kind
- ✅ Pods and Deployments
- ✅ Services (ClusterIP, LoadBalancer)
- ✅ Scaling deployments
- ✅ Load balancing across pods
- ✅ kubectl commands for managing resources
