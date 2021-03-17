AUTH_FAILED = {"text": "Forbidden", "status_code": 403}

INVALID_NON_JSON = {"text": "I am an unhandled non-JSON response"}

PERMISSION_DENIED = {"json": {}, "status_code": 403}  # No real JSON response is required here.

REQUEST_ERROR = {
    "json": {"message": "This is a request error message", "hint": "Check the request data"},
    "status_code": 400,
}

MUST_BE_DEPLOYED = {
    "json": {
        "message": "This is a request error message",
        "hint": "Check the request data",
        "details": "Image must be deployed.",
    },
    "status_code": 400,
}

CREDITS_ERROR = {"status_code": 402, "json": {}}

SERVER_ERROR = {
    "json": {
        "message": "This is a server error message",
        "details": "Something went wrong server-side",
        "hint": "Check the PPA logs",
    },
    "status_code": 500,
}

UNHANDLED = {"json": "Something really weird happened", "status_code": 410}

EMPTY_LIST = {"json": [], "status_code": 200}

EMPTY_DICT = {"json": [], "status_code": 200}

EMPTY_STRING = {"json": "", "status_code": 200}

NO_DATA = {"status_code": 204}

NOT_FOUND_JSON = {"status_code": 404, "json": ""}

NOT_FOUND_TEXT = {"status_code": 404, "json": None}

USERS = {
    "status_code": 200,
    "json": [
        {
            "id": 6,
            "username": "2012-domain\\system.auditor",
            "name": "system auditor",
            "email": "",
            "authenticated_at": "2021-02-11T14:45:15.934458+00:00",
            "active": False,
            "deleted_at": None,
        },
        {
            "id": 13,
            "username": "2012-domain\\cloud.engineer",
            "name": "cloud engineer",
            "email": "",
            "authenticated_at": "2021-02-11T14:28:33.535783+00:00",
            "active": False,
            "deleted_at": "2021-02-16T15:10:31.531594+00:00",
        },
        {
            "id": 3,
            "username": "2012-domain\\service.operator",
            "name": "service operator",
            "email": "",
            "authenticated_at": "2021-02-11T14:43:55.358433+00:00",
            "active": False,
            "deleted_at": None,
        },
    ],
}

IMAGES = {
    "status_code": 200,
    "json": [
        {
            "uuid": "031cd412-416f-47f3-8194-666d5897a617",
            "id": 2,
            "name": "Joiner Process",
            "description": "Test.",
            "hash": "sha256:79bd110a3bfa362f978ec609b4f0aebcd4bf21172501158e569343af6f86ba3a",
            "author": "Test",
            "tag": "demo",
            "tags": ["office", "joiner", "hr"],
            "updated_at": "2021-02-08T08:51:25.911919+00:00",
            "icon": None,
            "has_yaml": False,
            "deployed": True,
            "latest": {"id": 2, "tag": "demo"},
            "total_revisions": 1,
            "is_owner": True,
            "is_delegate": False,
            "os": "linux",
            "agent": "PPA Appliance",
            "available": True,
            "groups": 0,
            "owner": "test",
            "use_kerberos": False,
        },
        {
            "uuid": "031cd412-416f-47f3-8194-666d5897a617",
            "id": 2,
            "name": "Leaver Process",
            "description": "Test.",
            "hash": "sha256:79bd110a3bfa362f978ec609b4f0aebcd4bf21172501158e569343af6f86ba3a",
            "author": "Test",
            "tag": "demo",
            "tags": ["office", "leaver", "hr"],
            "updated_at": "2021-02-08T08:51:25.911919+00:00",
            "icon": None,
            "has_yaml": False,
            "deployed": True,
            "latest": {"id": 2, "tag": "demo"},
            "total_revisions": 1,
            "is_owner": True,
            "is_delegate": False,
            "os": "linux",
            "agent": "PPA Appliance",
            "available": True,
            "groups": 0,
            "owner": "test",
            "use_kerberos": False,
        },
    ],
}

TASKS = {
    "status_code": 200,
    "json": [
        {
            "id": 1,
            "image": "Successful - Owned By Me",
            "image_id": 1,
            "uuid": "fba5cc61-caf3-4620-a539-fcd7f4426abc",
            "hash": "sha256:509e853decea3cc651b07d2178721d4b483aed07ef5316fc59a3728395598f1e",
            "author": "Test",
            "image_uuid": "c2f44b57-e038-4d1c-bccb-65a58869f4f8",
            "username": "test",
            "is_owner": True,
            "exit_code": 0,
            "defunct": False,
            "started_at": "2021-02-11T11:17:56.141925+00:00",
            "stopped_at": None,
            "cancelled_at": None,
            "is_running": False,
            "cancelled_by": None,
            "duration": "00:00:43.860108",
            "timed_out": False,
            "state": "success",
            "agent_id": 1,
            "agent": "PPA Appliance",
            "timeout": 15,
            "source": "ui",
            "exit_message": None,
            "deployed": True,
        },
        {
            "id": 2,
            "image": "Failed - Not Owned By Me",
            "image_id": 2,
            "uuid": "fba5cc61-caf3-4620-a539-fcd7f4426abc",
            "hash": "sha256:509e853decea3cc651b07d2178721d4b483aed07ef5316fc59a3728395598f1e",
            "author": "Test",
            "image_uuid": "c2f44b57-e038-4d1c-bccb-65a58869f4f8",
            "username": "test",
            "is_owner": False,
            "exit_code": 1,
            "defunct": False,
            "started_at": "2021-02-11T11:17:56.141925+00:00",
            "stopped_at": "2021-02-11T11:18:56.141925+00:00",
            "cancelled_at": None,
            "is_running": False,
            "cancelled_by": None,
            "duration": "00:00:43.860108",
            "timed_out": False,
            "state": "success",
            "agent_id": 1,
            "agent": "PPA Appliance",
            "timeout": 15,
            "source": "ui",
            "exit_message": None,
            "deployed": True,
        },
        {
            "id": 3,
            "image": "Running - Not Owned By Me",
            "image_id": 3,
            "uuid": "fba5cc61-caf3-4620-a539-fcd7f4426abc",
            "hash": "sha256:509e853decea3cc651b07d2178721d4b483aed07ef5316fc59a3728395598f1e",
            "author": "Test",
            "image_uuid": "c2f44b57-e038-4d1c-bccb-65a58869f4f8",
            "username": "test",
            "is_owner": False,
            "exit_code": None,
            "defunct": False,
            "started_at": "2021-02-11T11:17:56.141925+00:00",
            "stopped_at": None,
            "cancelled_at": None,
            "is_running": True,
            "cancelled_by": None,
            "duration": "00:00:43.860108",
            "timed_out": False,
            "state": "success",
            "agent_id": 1,
            "agent": "PPA Appliance",
            "timeout": 15,
            "source": "ui",
            "exit_message": None,
            "deployed": True,
        },
    ],
}

TASK_STARTED = {"status_code": 200, "json": "fba5cc61-caf3-4620-a539-fcd7f4426abc"}

SUCCESSFUL_TASK = {"status_code": 200, "json": [TASKS["json"][0]]}

FAILED_TASK = {"status_code": 200, "json": [TASKS["json"][1]]}

RUNNING_TASK = {"status_code": 200, "json": [TASKS["json"][2]]}

TASK_RESULT = {
    "status_code": 200,
    "json": {
        "state": "success",
        "exit_code": 0,
        "exit_message": None,
        "result_json": {"message": "Hello I am a message!"},
    },
}

VERSIONS = {
    "2.7.0": {"status_code": 200, "json": {"appliance": "2.7.0"}},
    "2.7.1": {"status_code": 200, "json": {"appliance": "2.7.1"}},
}
