import pytest
from bootprocess import views_helper
from Access import models
import threading
from EnigmaAutomation.settings import DEFAULT_ACCESS_GROUP


class MockAuthUser:
    def __init__(self, username="", user=""):
        self.user = user
        self.username = username


class MockRequest:
    def __init__(self, username=""):
        self.user = MockAuthUser(username)


@pytest.mark.parametrize(
    (
        "testName, userIsInDefaultAccessGroup,"
        " groupCount"
    ),
    [
        # user is not part of default group and has respective count of git repo,
        # dashboard, ssh machines and group accesses
        ("UserInDefaultGroup", True, 40),
        ("UserInDefaultGroup", False, 40),
    ],
)
def test_getDashboardData(
    monkeypatch,
    testName,
    userIsInDefaultAccessGroup,
    groupCount,
):
    class MockUserModelobj:
        def __init__(self, user="", gitusername="", name=""):
            self.user = user
            self.gitusername = gitusername
            self.name = name

        def get(self, user__username=""):
            self.user = user__username
            return MockUserModelobj(user="username", gitusername="username")

    class MockGitAccessModelobj:
        def __init__(self, requestInfo={"": ""}):
            self.user = ""
            self.requestInfo = requestInfo

        def filter(self, requester="", status=""):
            if status == "Approved":
                return [MockGitAccessModelobj()]
            return MockGitAccessModelobj()

    class MockGroupV2:
        def filter(self, name="", status=""):
            if status == "Approved":
                return [MockGroupV2()]
            return MockGitAccessModelobj()

    class MockUserAccessMapping:
        def filter(self, user="", status="", access__access_tag=""):
            if access__access_tag == "other":
                return []
            elif access__access_tag == "github_access":
                return []
            elif access__access_tag == "ssh":
                return []
            else:
                group = []
                for i in range(groupCount):
                    group.append(i)
                return group

    class Group:
        def __init__(self):
            self.name = ""

    class MockMembershipV2:
        def __init__(self, is_owner=False, approver="", status="", user=""):
            self.is_owner = is_owner
            self.approver = approver
            self.status = status
            self.user = user
            self.group = Group()

        def filter(self, user="", status="", group="", is_owner=False):
            if is_owner:
                return [MockMembershipV2()]
            return MockMembershipV2()

        def only(self, filter):
            return MockMembershipV2()

        def create(*args, **kwargs):
            return MockMembershipV2()

        def save(self):
            return ""

        def __str__(self):
            if userIsInDefaultAccessGroup:
                return DEFAULT_ACCESS_GROUP
            else:
                return ""

        def __len__(self):
            return groupCount

    class MockThread:
        def start(self):
            return True

    def mockgenerateUserMappings(*args, **kwargs):
        return []

    views_helper.generate_user_mappings = mockgenerateUserMappings

    def mock_Thread(*args, **kwargs):
        return MockThread()

    monkeypatch.setattr(threading, "Thread", mock_Thread)

    models.MembershipV2.objects = MockMembershipV2()
    models.User.objects = MockUserModelobj()
    models.UserAccessMapping.objects = MockUserAccessMapping()
    models.GroupV2.objects = MockGroupV2()
    request = MockRequest(username="username1")
    context = views_helper.getDashboardData(request)
    assert context["regions"] == ["eu-central-1"]
    assert context["groupCount"] == groupCount
