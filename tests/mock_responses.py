AUTH_FAILED = {"text": "Forbidden", "status_code": 403}

INVALID_NON_JSON = {"text": "I am an unhandled non-JSON response"}

PERMISSION_DENIED = {"json": {}, "status_code": 403}  # No real JSON response is required here.

REQUEST_ERROR = {
    "json": {"message": "This is a request error message", "hint": "Check the request data"},
    "status_code": 400,
}

TASK_MUST_BE_DEPLOYED = {
    "json": {
        "message": "This is a request error message",
        "hint": "Check the request data",
        "details": "Image must be deployed.",
    },
    "status_code": 400,
}

DELAY_MUST_BE_DEPLOYED = {
    "json": {
        "message": "This is a request error message",
        "hint": "Check the request data",
        "details": "No deployed version found.",
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
            "username": "domain\\system.auditor",
            "name": "system auditor",
            "email": "",
            "authenticated_at": "2021-02-11T14:45:15.934458+00:00",
            "active": False,
            "deleted_at": None,
            "groups": [
                "ad:domain.net:PPA Admins",
            ],
        },
        {
            "id": 13,
            "username": "domain\\cloud.engineer",
            "name": "cloud engineer",
            "email": "",
            "authenticated_at": "2021-02-11T14:28:33.535783+00:00",
            "active": False,
            "deleted_at": "2021-02-16T15:10:31.531594+00:00",
            "groups": ["ad:domain.net:PPA Admins", "ad:domain.net:PPA Auditors"],
        },
        {
            "id": 3,
            "username": "domain\\service.operator",
            "name": "service operator",
            "email": "",
            "authenticated_at": "2021-02-11T14:43:55.358433+00:00",
            "active": False,
            "deleted_at": None,
            "groups": [
                "ad:domain.net:PPA Task Operators",
                "ad:domain.net:PPA Admins",
                "ad:domain.net:PPA Auditors",
            ],
        },
    ],
}

ROLES = {
    "status_code": 200,
    "json": [
        {
            "id": 3,
            "name": "Users",
            "groups": [],
            "groups_count": None,
            "users_count": 0,
            "permissions": [
                "images.read",
                "tasks.output.read",
                "tasks.events.read",
                "tasks.events.write",
                "tasks.cancel",
            ],
        },
        {
            "id": 4,
            "name": "Task Operators",
            "groups": ["ad:domain.net:PPA Task Operators"],
            "groups_count": 1,
            "users_count": 5,
            "permissions": [
                "images.read",
                "tasks.events.read",
                "tasks.output.read",
                "tasks.events.write",
                "tasks.cancel",
            ],
        },
        {
            "id": 5,
            "name": "Auditors",
            "groups": ["ad:domain.net:PPA Auditors"],
            "groups_count": 1,
            "users_count": 3,
            "permissions": [
                "images.read",
                "images.read+",
                "images.groups.read",
                "images.source.owner.read",
                "images.source.read+",
                "images.source.maintainer.read",
                "images.maintainers.read",
                "editor.plugins.read",
                "tasks.read+",
                "tasks.events.read",
                "tasks.events.read+",
                "tasks.output.read",
                "tasks.output.read+",
                "jobs.read",
                "jobs.read+",
                "reporting.read",
                "config.read",
                "users.read",
                "roles.read",
                "active-directory.read",
                "kerberos.read",
                "apis.read",
                "license.read",
                "smtp.read",
                "syslog.read",
                "sso.read",
            ],
        },
        {
            "id": 2,
            "name": "Admins",
            "groups": [
                "ad:domain.net:PPA Admins",
                "ad:domain.net:PPA Auditors",
                "ad:domain.net:PPA Task operators",
            ],
            "groups_count": 3,
            "users_count": 7,
            "permissions": [
                "images.read",
                "images.read+",
                "images.upload",
                "images.archive",
                "images.groups.read",
                "images.groups.write",
                "tasks.read+",
                "tasks.output.read",
                "tasks.output.read+",
                "tasks.events.read",
                "tasks.events.read+",
                "tasks.events.write",
                "tasks.events.write+",
                "hooks.wait",
                "tasks.cancel",
                "tasks.cancel+",
                "active-directory.read",
                "active-directory.write",
                "agents.read",
                "agents.sync",
                "agents.write",
                "roles.read",
                "roles.write",
                "users.read",
                "users.write",
                "apis.read",
                "apis.write",
                "reporting.read",
                "config.read",
                "license.read",
                "license.write",
                "system.techout",
                "users.api_key",
                "jobs.read",
                "jobs.read+",
                "jobs.write",
                "jobs.write+",
                "syslog.read",
                "syslog.write",
                "smtp.read",
                "smtp.write",
                "sso.read",
                "sso.write",
                "images.metadata",
                "images.ownership",
                "images.maintainers.read",
                "images.maintainers.write",
                "images.source.owner.read",
                "images.source.maintainer.read",
                "images.source.read+",
                "images.source.owner.write",
                "images.source.maintainer.write",
                "images.source.write",
                "images.source.write+",
                "editor.plugins.write",
                "editor.plugins.delete",
                "images.download",
                "editor.plugins.read",
                "images.deploy",
                "editor.plugins.build",
                "users.delete",
                "users.restore",
                "kerberos.read",
                "kerberos.write",
                "tasks.delayed.write",
                "tasks.delayed.write+",
                "system.events.dismiss",
                "insights.read",
            ],
        },
    ],
}

GROUPS = {
    "status_code": 200,
    "json": [
        {
            "id": 3,
            "name": "ad:domain.net:PPA Auditors",
            "source": "active-directory",
            "user_sync": True,
            "start_tasks": False,
            "roles_count": 1,
            "images_count": 1,
            "members_count": 1,
        },
        {
            "id": 2,
            "name": "ad:domain.net:PPA Admins",
            "source": "active-directory",
            "user_sync": True,
            "start_tasks": True,
            "roles_count": 1,
            "images_count": 0,
            "members_count": 5,
        },
        {
            "id": 1,
            "name": "ad:domain.net:PPA Task Operators",
            "source": "active-directory",
            "user_sync": True,
            "start_tasks": True,
            "roles_count": 1,
            "images_count": 26,
            "members_count": 4,
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

DELAYED_TASKS = {
    "status_code": 200,
    "json": [
        {
            "id": 1,
            "image": "Add User To Group",
            "image_id": 1,
            "description": "Adding John Smith to Remote Desktop Users",
            "username": "test",
            "task_uuid": "5069b766-0a8b-4721-8819-87d007c38db1",
            "is_pending": False,
            "is_owner": True,
            "start_time": "2021-03-24T16:14:16.775347",
            "timezone": "Etc/UTC",
            "payload": None,
            "has_payload": False,
            "source": "api",
            "parent_task_id": None,
        },
        {
            "id": 2,
            "image": "Remove User From Group",
            "image_id": 1,
            "description": "Removing John Smith from Remote Desktop Users",
            "username": "admin",
            "task_uuid": "9990056a-17b5-494a-8ae5-d3c84ca62d3b",
            "is_pending": False,
            "is_owner": True,
            "start_time": "2021-03-24T20:14:16.942373",
            "timezone": "Etc/UTC",
            "payload": None,
            "has_payload": False,
            "source": "api",
            "parent_task_id": None,
        },
    ],
}

TASK_STARTED = {"status_code": 200, "json": "fba5cc61-caf3-4620-a539-fcd7f4426abc"}

TASK_DELAYED = {"status_code": 200, "json": 1}

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
    f"2.{minor_version}.{patch_version}": {
        "status_code": 200,
        "json": {"appliance": f"2.{minor_version}.{patch_version}"},
    }
    for minor_version in {"7", "8", "9", "10", "11"}
    for patch_version in {"0", "1"}
}
