Welcome to caspyr, a python project for VMware Cloud Automation Services. 

This has been born out of a need to provide some automation for the VMware Hands-On Labs, and will be built out over time to support further use cases. 

While the owner of this repository is an employee of VMware, this is not an official VMware project.

To get started, login with your API token:
s = Session.login(api_token)

Subsequent calls need the Session class object passed to it:
d = Deployment.list(s)

Code comments need some work, but if you have any problems, just create an issue, or ping me on twitter @grantorchard.
