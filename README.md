q# PRODUCTION DEPLOYMENT PRACTISE: 

## PART 1: DEV STAGE
For this stage w'll be adding a dockerfile and a YAML compose file to declare to docker what to build. Furthermore, we will need a requirements file to make sure the project has installed all necessary dependencies:

<img width="1132" height="729" alt="cpose 1" src="https://github.com/user-attachments/assets/668fe944-fba2-4033-a6ec-e430253a435b" />

<img width="1132" height="729" alt="cpose 1" src="https://github.com/user-attachments/assets/b25760d3-0b5c-46da-8c8e-c4105163db5b" />

<img width="1132" height="729" alt="cpose 1" src="https://github.com/user-attachments/assets/10a6e9ae-e222-4e60-ae4b-5d878a63a7a2" />

## PART 2: FIRST PRODUCTION STAGE
Now, we'll add Gunicorn as intermediate between our application and the world of internet as WSGI. Why do we need to do this? First, exposing the app to internet by default is insecure and it's not scalable. So
we need a web server, like nginx in this practise. Secondly, a web server like nginx cannot execute directly python or other codes. We need an app that can intermediate between theese two. Then, we need to make
a scalable and secured project , so we need a server, but servers do not execute code easily so we need something to intermediate.

To get Gunicorn we define it in the requirements and we modify the command of the compose and the dockerfile (only showing dockerfile)
Later we must make a little fix. In the project there's installed the reload middleware, and it's a bad ppractise to use it in a production deployment because of the frequent petitions to reload.
So, we must eliminate the app, the middleware and the specification in the requirements.txt

<img width="1131" height="395" alt="dfile 2" src="https://github.com/user-attachments/assets/6d60b710-518f-49c3-adb0-d6abb090a6f2" />

<img width="1131" height="395" alt="dfile 2" src="https://github.com/user-attachments/assets/d4137769-ee4f-49d8-9eb4-6a678bc25be9" />

## PART 3: FINAL PRODUCTION STAGE
Now we will be adding the web server nginx, by adding a folder 'nginx' with another folder, 'conf.d' and inside it a file called 'default.conf'. This file will have de basic configuration for the server

<img width="1157" height="676" alt="default" src="https://github.com/user-attachments/assets/b8e7ee9a-e1c0-4dd1-b667-7f2717df77ee" />

Then we'll be moddifying the compose.yaml so it includes the server and let it the exit of the information, so the web sercvice only exposses it's port. Also built the volumes, and chnaged the default command

<img width="1140" height="856" alt="cpose2" src="https://github.com/user-attachments/assets/178415c4-f351-49c1-83ca-88ba5df9f5cd" />

Finally, a quick specification in the settings of the project for the mdia and static files served directly by nginx

<img width="1268" height="973" alt="seting" src="https://github.com/user-attachments/assets/1acd209b-30fc-439f-b27f-289da82d7a93" />



