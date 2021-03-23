[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Build Status](https://www.travis-ci.com/tomguyatt/osirium-ppa-api.svg?token=axSwR2eiyQ8S1NRkBAps&branch=main)](https://www.travis-ci.com/tomguyatt/osirium-ppa-api) [![codecov](https://codecov.io/gh/tomguyatt/osirium-ppa-api/branch/main/graph/badge.svg?token=F5OEWBU3RV)](https://codecov.io/gh/tomguyatt/osirium-ppa-api)

# Osirium PPA API

A Python package for integrating with Osirium PPA's public API.

### Getting Started

- [Installation](#installation)
- [Version Requirements](#version-requirements)
- [Auth & Permissions](#authentication--permissions)
- [Certificates & Proxies](#certificates-and-proxies)

### Example Scripts

The [examples](examples) folder contains scripts demonstrating the following operations.

#### Users

- [All Users CSV](examples/users_report.py)
- [Licensed Users CSV](examples/licensed_users_report.py)

#### Tasks

- [Run Task](examples/run_task.py)
- [Run Task (async)](examples/run_task_async.py)
- [My Task History CSV](examples/my_task_history_report.py)

#### Images

- [Deployed Images CSV](examples/deployed_images.py)

### Code Snippets:

#### Client

- [Create Client Instance](#create-client-instance)

#### Users

- [List All Users](#list-all-users)
- [List Licensed Users](#list-licensed-users)
- [List Deleted Users](#list-deleted-users)
- [Get Specific User](#get-specific-user)

#### Tasks

- [Auditing Task History](#auditing-task-history)
    - [All Tasks](#listing-all-tasks)
    - [Tasks Started By Me](#listing-tasks-started-by-me)
- [Starting Tasks](#starting-tasks)
    - [Synchronous](#synchronous)
    - [Asynchronous](#asynchronous)
    - [Undeployed Tasks](#undeployed-tasks)
- [Supplying Payloads](#supplying-payloads)
- [Checking Task State](#checking-task-state)

#### Images

- [Getting Images](#getting-images)
    - [Latest Images](#listing-latest-images)
    - [All Images](#listing-all-images)

#### Other

- [Return Types](#return-types)
- [Return Fields](#return-fields)
- [Exceptions](#exceptions)

# Getting Started

## Installation

The package is on pypi and can be installed via pip:

`pip install ppa-api`

## Version Requirements

- PPA Appliance 2.7.1 or later
- Python 3.8 or later

## Authentication & Permissions

You'll need to generate an API key in PPA to use this package.

The API key will have the same permissions as the PPA user it was generated by.

The following snippet requires permission to view users in PPA.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.users()
```

If the code run without the relevant PPA permissions, it will raise [PermissionDenied](#permissiondenied).

```
PermissionDenied: Forbidden (403). The user associated with this API key does not have the required users permissions in PPA.
```

## Certificates & Proxies

You can supply a proxy address to the PPA client instance using the `proxy` keyword argument.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key, proxy="my-https-proxy.net")
```

To use a custom certificate, use the `verify` keyword argument to supply a path to a CA bundle.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key, verify="/path/to/ca-bundle")
```

By default no proxy or custom certificate will be used, & the server's TLS certificate will be verified. 

# Code Examples

## Client

### Create Client Instance

Creating a PPA client instance requires an `address`  & `api_key`.

If there is no trusted certificate on PPA, you'll need to set the `verify` keyword argument to `False`.

#### Trusted Certificate

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
```

#### Untrusted Certificate

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key, verify=False)
```

Skipping verification may generate the following log lines whenever a request is made:

```
InsecureRequestWarning: Unverified HTTPS request is being made to host '1.2.3.4'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
```

You can silence these by importing `urllib3` & disabling the warning.

```python
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Users

### List All Users

This snippet will list all _current_ users in the PPA appliance.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.users()
```

A list of [Users](#user) will be returned.

```python
[
    User(
        active=False,
        authenticated_at='2021-02-11T14:28:33.535783+00:00',
        deleted_at=None,
        email='cloud.engineer@domain.com',
        id=3,
        name='cloud engineer',
        username='domain\\cloud.engineer'
    )
]
```

### List Licensed Users

This snippet will list all _current_ users who can **start tasks**.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.licensed_users()
```

A list of [Users](#user) will be returned.

```python
[
    User(
        active=True,
        authenticated_at='2021-02-12T12:03:17.515093+00:00',
        deleted_at=None,
        email='service.operator@domain.com',
        id=3,
        name='service operator',
        username='domain\\service.operator'
    )
]
```

### List Deleted Users

Use the following method to list all deleted users.
 
```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.deleted_users()
```

A list of [Users](#user) will be returned

### Get Specific User

This snippet finds the user with the supplied username.

The search is case insensitive & the domain name is not required.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.user_by_username("service.operator")
``` 

A single [User](#user) is returned if the user is found.

If the user was not found, the method will return `None`.

## Tasks

### Auditing Task History

#### Listing All Tasks

You can view the history of all tasks visible to the API key's associated user.

The following snippet gets all visible tasks.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.tasks()
```

#### Listing Tasks Started By Me

The following snippet get all visible tasks _started by_ the API key's associated user.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.tasks_started_by_me()
```

Both methods return a list of [tasks](#task).

```python
[
    Task(
        author='John Doe',
        cancelled_at=None,
        cancelled_by=None,
        duration='00:01:33.945833',
        exit_code=0,
        exit_message=None,
        id=3,
        image='Add User to Groups',
        image_id=7,
        image_uuid='59787351-16ac-4a85-a812-007b1dcde027',
        is_owner=True,
        is_running=False,
        started_at='2021-02-08T10:12:25.404705+00:00',
        state='success',
        stopped_at='2021-02-08T10:13:59.350538+00:00',
        timed_out=False,
        timeout=15,
        username='domain\\john.doe',
        uuid='b007905b-6c6a-4037-b4cd-b2d4a7fd3c0d'
    )
]
```

### Starting Tasks

This package allows you to start the **latest deployed** revision of a task.

Tasks can be started either synchronously or asynchronously.
 
#### Synchronous

The snippet below starts the _latest deployed revision_ of a task, & waits up to 10 minutes for it to complete.

A [Task](#task) is returned if it completes within the time limit, otherwise [WaitTimeout](#waittimeout) is raised.

You can supply a custom timeout in seconds using the `timeout` keyword argument. 

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
task = ppa.start_task("Domain Admins Audit")
```

See the asynchronous section below for a non-blocking approach.

#### Asynchronous

This snippet starts the _latest deployed revision_ of a task & immediately returns a [Task](#task).

The state is checked periodically using the [Task](#task) `uuid` attribute.

```python
import time

from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
task = ppa.start_task_async("Domain Admins Audit")

for i in range(0, 10):
    if ppa.task_running(task.uuid):
        print("The task is still running.")
        time.sleep(30)
        continue
    break
else:
    raise Exception("The task has not completed after 5 minutes.")

print(ppa.get_task_result(task.uuid))
```

#### Undeployed Tasks

Starting an **undeployed** task will raise [ImageNotDeployed](#imagenotdeployed).

```
ImageNotDeployed: The task cannot be started as image 'example task' is not deployed.
```

### Checking Task State

The state of a task can be checked a few different ways.

#### Did a task succeed?

```python
ppa.task_succeeded(task.uuid)
```

The easiest way to whether a task succeeded.

Returns a bool or raises [TaskStillRunning](#taskstillrunning).

#### Is a task running?

```python
ppa.task_running(task.uuid)
```

The recommended method to use while waiting for a task that was started asynchronously.

Returns a bool.

#### Get a Task using its UUID

```python
ppa.task_by_uuid(task.uuid)
```

Returns a [Task](#task) reflecting its current state.

```python
Task(
    author='John Doe',
    cancelled_at=None,
    cancelled_by=None,
    duration='00:01:33.945833',
    exit_code=0,
    exit_message=None,
    id=3,
    image='Add User to Groups',
    image_id=7,
    image_uuid='59787351-16ac-4a85-a812-007b1dcde027',
    is_owner=True,
    is_running=False,
    started_at='2021-02-08T10:12:25.404705+00:00',
    state='success',
    stopped_at='2021-02-08T10:13:59.350538+00:00',
    timed_out=False,
    timeout=15,
    username='domain\\john.doe',
    uuid='b007905b-6c6a-4037-b4cd-b2d4a7fd3c0d'
)
```

#### Get Task Result

This is the only method that returns both the task state & its JSON result.

```python
ppa.get_task_result(task.uuid)
```

Returns a [TaskResult](#taskresult) if the task saved a JSON result.

```python
TaskResult(
    exit_code=0,
    exit_message=None,
    result_json={"user_created": True, "group_memberships": None},  # This is saved by the task when it runs.
    state='success'
)
``` 

If the task didn't save a JSON result, [NoData](#nodata) will be raised.

```
NoData: No result data was saved by task with UUID '2f35cbe5-75af-4a68-af1b-b3b61c231588'.
```

### Supplying Payloads

You can supply a JSON payload to a task with the `payload` keyword argument.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
task = ppa.start_task(
    "Audit Untagged EC2 Instances",
    payload={
        "environment": "development",
        "team": "infrastructure"
    }
)
```

If the supplied payload cannot be converted to JSON, [ParameterError](#parametererror) will be raised.

```
ParameterError: The supplied payload cannot be converted to JSON.
```

## Images

The images API endpoint represents the **Inventory** page in PPA.

You can use the API to list images visible to the API key's associated user.

For an image to be visible to a user, one of the following must be true:

- The user has permission to see all tasks
- The image is owned by the user
- The image has been delegated to a group the user is in

You can check the _deployed_ attribute to determine if an image is deployed or not. 

### Listing Latest Images

This snippet will list the latest version of each visible image.

In this context __latest__ means one of the following:

- The current deployed revision (if the image has been deployed)
- The latest built revision (if the image has _not_ been deployed)

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.images(latest=True)
```

A list of [Images](#image) will be returned.

```python
[
    Image(
        author='John Doe',
        description='Recertify members of your Active Directory groups.',
        deployed=True,
        groups=0,
        id=6,
        name='Group Recertification',
        owner='domain\\john.doe',
        tags=['active directory', 'group', 'recertification'],
        updated_at='2021-01-21T15:28:41.463558+00:00',
        uuid='b2d8d266-03da-49ce-8a4a-836fe2fed6e9'
    )
]
```

### Listing All Images

This snippet will list _all revisions_ of each image visible to the API key's associated user.

```python
from ppa_api.client import PPAClient

ppa = PPAClient(address, api_key=api_key)
ppa.images()
```

A list of [Images](#image) will be returned.

## Return Types

You can use this package to interact with PPA __images__, __tasks__, & __users__.

Methods that _only_ fetch a single record will return a named tuple.

Methods that _can_ fetch multiple records will return a list of named tuples, even if only 1 item is received.  

Named tuples are immutable & their values can be accessed using dot notation.

See [Return Fields](#return-fields) for the fields available in each named tuple.

## Return Fields

The fields available for each type of named tuple are listed below.

### User

- active
- authenticated_at
- deleted_at
- email
- id
- name
- username

### Task

- author
- cancelled_at
- cancelled_by
- duration
- exit_code
- exit_message
- id
- image
- image_id
- image_uuid
- is_owner
- is_running
- result_json
- started_at
- state
- stopped_at
- timed_out
- timeout
- username
- uuid

### TaskResult

- exit_code
- exit_message
- result_json
- state

### Image

- author
- deployed
- description
- groups
- id
- name
- owner
- tags
- updated_at
- uuid

## Exceptions

The following custom exceptions can be raised by this package.

#### CreditsRequired

One of the [start task](#starting-tasks) methods was called with no licensed credits remaining.

#### AuthenticationFailed

Authentication to the PPA Appliance failed using the supplied API key.

#### VersionError

The target PPA Appliance is older than v2.7.1.

#### TaskStillRunning

The task_succeeded method was called on a task that is still running.

#### WaitTimeout

A task is started synchronously & does not finish within the time limit.

#### ImageNotDeployed

One of the [start task](#starting-tasks) methods was called with the name of an undeployed image.

#### NoData

The get_task_result method was called on a task that has not saved a JSON result.

#### NotFound

A non-existent endpoint was called or a supplied `uuid` does not exist.

Usually re-raised as a more meaningful exception.

#### NoImageFound

An invalid `uuid` was supplied to an image method.

#### NoTaskFound

An invalid `uuid` was supplied to a task method.

#### PermissionDenied

The API key does not have permission in the PPA Appliance to perform the operation.  

#### ParameterError

Either a `uuid` or `payload` was supplied in an invalid format.

#### ServerError

The PPA appliance responded with status code 500.

#### RequestError

The PPA appliance responded with status code 400.

#### UnhandledRequestError

The PPA Appliance responded with an unhandled status code (unlikely).

#### InvalidResponse

The PPA Appliance responded with invalid JSON (very unlikely).
