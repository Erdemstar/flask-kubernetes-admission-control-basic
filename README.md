# Flask - Kubernetes Admission Control
Hello, in this project, I made a simple development with Python Flask using Mutate and Validate Webhooks in Kubernetes Admission Control. My aim of developing the project is to provide convenience and basis for those who want to develop a project by using this feature in the future.

**Validate**
In this section, it checks whether there is ***latest*** at the end of the tag by looking at the tag part of the image that comes in the Deployment to be created.

**Mutate**
In this section, it adds the word ***dummy-prefix*** to the beginning of the name information in the Deployment to be created.

## Project Folders
In order to create an order in the project, folders have been made. Details are as follows.

 - **Certs**
	 - ***Generate*** : It contains the things that will be needed to produce the certificate.
	 - ***Keys***: It is the part where the produced certificates are kept.
- **iac**
	- ***Docker*** : It is the folder where Dockerfile is kept.
	- ***Kubernetes***: It is the folder where the files for creating the application in kubernetes and other needs are kept.
- **Certs**
	 - ***app.py*** : Contains application codes.

## Project Integration

### Image Creation
The image version of the project is kept on Docker hub as follows. If you wish, you can run it using the following path or you can create your own image by changing Project > iac > Docker > Dockerfile.

**Dockerhub**

```
erdemstar/flask-admission-control:1.0.0
```

### Running in Kubernetes
After the image process is finished, we need to perform the final checks in iac > Kubernetes > deployment.yaml and run the following commands in order if there is no problem.

The following command is used to install the application in kubernetes.
```
kubectl apply -f deployment.yaml
```

The following command is used to register the installed application we created in Kubernetes into Admission Control.
```
kubectl apply -f admission.yaml
```

The final state should be as follows.

![enter image description here](https://user-images.githubusercontent.com/26081033/201528861-b5e97117-0c07-44f9-8f7d-458aff40b736.png)


### Controlling Webhooks
At this stage, you can understand whether the application is working properly by running the commands below and checking whether the output is the same as in the pictures.

The image in iac > Kubernetes > Validating.yaml is specified as ***nginx:test***. Since this definition is undesirable by the validation we have added, Deployment will not have a foot in the kubernetes environment and will produce a message as in the picture.
```
kubectl apply -f validating.yaml
```
![enter image description here](https://user-images.githubusercontent.com/26081033/201529140-bfd49780-ef6b-48ae-8331-3db5bec5580b.png)

In iac > Kubernetes > Mutating.yaml, the name given to Deployment is defined as ***myapp2***. When the following command is run, the result will be ***dummy-prefix-myapp2***.

```
kubectl apply -f mutating.yaml
```

![enter image description here](https://user-images.githubusercontent.com/26081033/201529292-5fa13ebb-8799-4a7e-82f5-3e46bcf1cfb6.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)