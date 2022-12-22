class UserSyncErrorTemplate:

    @property
    def name(self):
        return "UserSyncError"

    @property
    def locked_account(self):
        error = "User account used by PPA is locked"
        return {
            "reason": "GroupsNotFound",
            "objects": [
                {"name": "Group 1", "error": error},
                {"name": "Group 2", "error": error}
            ]
        }

    @property
    def logon_failure(self):
        error = "Invalid username or password for user account used by PPA"
        return {
            "reason": "GroupsNotFound",
            "objects": [
                {"name": "Group 1", "error": error},
                {"name": "Group 2", "error": error}
            ]
        }

    @property
    def missing_groups(self):
        error = "No group found"
        return {
            "reason": "GroupsNotFound",
            "objects": [
                {"name": "Group 1", "error": error},
                {"name": "Group 2", "error": error}
            ]
        }


class UserSyncFailedTemplate:

    @property
    def name(self):
        return "UserSyncFailed"

    @property
    def no_groups_found(self):
        return {"reason": "NoGroupsFound", "objects": ["Group 1", "Group 2"]}

    @property
    def connection_error(self):
        return {"reason": "ConnErr", "objects": ["Group 1", "Group 2"]}

    @property
    def no_group_found(self):
        return {"reason": "NoGroupFound", "objects": ["Group 1", "Group 2"]}

    @property
    def multiple_groups_found(self):
        return {"reason": "MultipleGroupsFound", "objects": ["Group 1", "Group 2"]}


class LowDiskSpaceTemplate:

    @property
    def name(self):
        return "LowDiskSpace"

    @property
    def low(self):
        return {
            "total": 64424509440,
            "remaining": 21474836480,
            "used": 42949672960,
            "percent_remaining": 66.66,
            "percent_used": 33.34
        }

    @property
    def critical(self):
        return {
            "total": 64424509440,
            "remaining": 1073741824,
            "used": 63350767616,
            "percent_remaining": 1.67,
            "percent_used": 98.33
        }

    @property
    def critical_small_disk(self):
        return {
            "total": 21474836480,
            "remaining": 1073741824,
            "used": 20401094656,
            "percent_remaining": 5,
            "percent_used": 95
        }


UserSyncError = UserSyncErrorTemplate()
UserSyncFailed = UserSyncFailedTemplate()
LowDiskSpace = LowDiskSpaceTemplate()
