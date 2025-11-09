# References

_Kubernets Docs_

https://kubernetes.io/docs/home/

_Kind Docs_

https://kind.sigs.k8s.io/docs/user/quick-start/

https://kind.sigs.k8s.io/docs/user/quick-start/#installation

_Kind alternatives_

https://kubernetes.io/docs/tasks/tools/

# local kubernets cluster using KIND

## Create Using CLI

- ### _Cretae a simple cluster (only one master node)_

```bash
    kind create cluster --name kind-cluster
```

_This will create a kubernets cluster on our machine, and the nodes are a docker containers_

- ### _Switching the kubectl context to point to the cluster we just created_

```bash
    kubectl cluster-info --context kind-cluster
```

- ### _Interacting with the cluster_

```bash
    kubectl get node -o wide # Get the cluster nodes
    kubectl get pods -o wide # Get the cluster pods
    kubectl get svc -o wide # Get the cluster services
```

- ### _Delete the cluster_

```bash
    kind delete cluster --name kind-cluster
```

## Create Using Config file

- in the root folder we have a kind_cluster_config.yaml file contains configs for kind to create a k8s cluster with one master node and 3 worker nodes \*

* ### _Cretae the cluster_

```bash
    kind create cluster --config kind_cluster_config.yaml --name spaceland_cluster
```

- ### _Switching the kubectl context to point to the cluster we just created_

```bash
    kubectl cluster-info --context spaceland_cluster
```

- ### _Interacting with the cluster_

```bash
    kubectl get node -o wide # Get the cluster nodes
    kubectl get pods -o wide # Get the cluster pods
    kubectl get svc -o wide # Get the cluster services
```


# Playing with k8s

## Playing with pods

- *in the src folder we have a python script that represents a simple backend with one endpoint /heath that returns Up*

- *this backend will be hosted as a server on a pod in k8s*

### build & tag & push the docker image

```bash
    docker build -t basic_api . # build 
    docker run -p 5000:5000 basic_api # run 
    docker tag basic_api `registry-name`/basic_api:0.0.1 # tag
    docker push `registry-name`/basic_api:0.0.1 # push
```

### deploy the api with deployment

*k8s deployments*

https://kubernetes.io/docs/concepts/workloads/controllers/deployment/


- *in the root folder we have a k8s_deployment.yaml file the contains a deployment object for k8s*
- *deploying with kubectl*

```bash
    kubectl apply -f k8s_deployment.yaml
```


- *get pods*

```bash
    kubectl get pods
```


### deploy the curl pod

- *in the root folder we have a curl-pod.yaml file contains kubernets pod object*
- *the curl pod runs a container with image curlimages/curl:latest, this pod have the curl utulity that we can use it to make http request to the api server we just deployd*

```bash
    kubectl apply -f curl-pod.yaml
```
- *enter the pod cli to use teh curl tool & use the curl command to sent GET request to <api-server-pod-ip-adress>:5000*

```bash
    kubectl get pods -o wide # to get the api-server-pod-ip-adress
    kubectl exec -it curl-pod -- curl <api-server-pod-ip-adress>:5000 # request the api-server
```

### deploy the ClusterIP Service

- *References : https://kubernetes.io/docs/concepts/services-networking/service/*

- *To fix the changing ip addres of the pods we will use services*
- *The service is k8s object that have a fixed ip adress and a local dns*

- *Deploy the service* in the root folder we have a ClusterIP.yaml file contains the service object*

```bash
    kubectl apply -f ClusterIP.yaml
```

- *Get the services ip*

```bash
    kubectl get svc
```

$ while true; do curl -w "\n" 10.96.57.225:9090; sleep 1; done
