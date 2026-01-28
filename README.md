# PRODUCTION DEPLOYMENT PRACTISE: 

## PART 1: DEV STAGE
For this stage w'll be adding a dockerfile and a YAML compose file to declare to docker what to build. Furthermore, we will need a requirements file to make sure the project has installed all necessary dependencies:

<img width="1132" height="729" alt="cpose 1" src="https://github.com/user-attachments/assets/668fe944-fba2-4033-a6ec-e430253a435b" />

<img width="1132" height="729" alt="cpose 1" src="https://github.com/user-attachments/assets/b25760d3-0b5c-46da-8c8e-c4105163db5b" />

<img width="1132" height="729" alt="cpose 1" src="https://github.com/user-attachments/assets/10a6e9ae-e222-4e60-ae4b-5d878a63a7a2" />

## PART 2: FIRST PRODUCTION STAGE
Now, we'll add Gunicorn as intermediate between our application and the world of internet as WSGI. Why do we need to do this? First, exposing the app to internet by default is insecure and it's not scalable. So
we need a web server, like nginx in this practise. Secondly, a web server like nginx cannot execute directly python or other codes. We need an app that can intermediate between theese two. Then, we need to make
a scalable and secured project , so we need a server, but servers do not execute code easily so we need something to intermediate.


