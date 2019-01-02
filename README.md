# Cloud Automation Services SDK for Python (Caspyr)
This is a set of Python (3.6 minimum version) bindings for VMware's Cloud Automation Services (Cloud Assembvly, Service Broker, Code Stream) meant to simplify programmtic consumption of it's API interfaces. 

The initial usecase was designed to automate the 1902-03 Hands On Labs for VMworld; but significant usecase exist to consume this SDK.

This kit was primarilly designed by VMware employees however is not a VMware project as of now. 

## Requirements for Usage 
* Python 3.6 
* This Repository 
* API Key with sufficient permissions to the Cloud Automation Services platform

## Getting Started 

Clone this repository and access a Python Shell. Import the appropriate modules/libraries in order to begin interacting with the platform. Example import statement is below

```
from caspyr import Session, User, Region
from caspyr import CloudAccountAws, CloudAccountAzure, CloudAccount
from caspyr import CloudZone, ImageMapping, FlavorMapping
from caspyr import NetworkProfile, StorageProfileAWS, StorageProfileAzure, StorageProfile
from caspyr import Project, Request, Deployment, Blueprint, Machine
```

From here, we will authenticate to the Cloud Services Platform by establishing an object for we can interact with. 

```
s = Session.login(api_token)
```

With this object instantiated, we can leverage other calls, passing the session object in to return data. Examples can be found in the examples directory. 

### Listing all Current Deployments

```
s = Session.login(api_token)
d = Deployment.list(s)
```

### Listing all Projects

```
s = Session.login(api_token)
p = Projects.list(s)
```

### Import Blueprint from Github Repository

```
s = Session.login(api_token)
p = Projects.list(s)
projID = p[0]['id']
b = Blueprint.create(s,projID,'Sample BP','Sample Blueprint Name','1','codyde/cas-blueprints','samplebp.yaml')
```

Documentation is forthcoming (PR's welcome!)

## Maintainers

Grant Orchard (@grantorchard)
Cody De Arkland (@codydearkland)