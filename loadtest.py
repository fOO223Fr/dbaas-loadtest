import htpasswd
import argparse
from os.path import exists
from pathlib import Path
import openshift as oc
import time

parser = argparse.ArgumentParser(description="Program to loadtest dbaas operator")
parser.add_argument("--createprojects", help="Create projects", default=False, action="store_true")
parser.add_argument("--deleteprojects", help="Delete projects", default=False, action="store_true")
parser.add_argument("--giveadminrights", help="Give rights of projects to users", default=False, action="store_true")
parser.add_argument("--removeadminrights", help="Remove rights of projects from users", default=False,
                    action="store_true")
parser.add_argument("--createdbaastenant", help="Create dbaas tenant", default=False, action="store_true")
parser.add_argument("--test", help="Testing", default=False, action="store_true")
parser.add_argument("--file", help="Enter htpasswd file path")
args = vars(parser.parse_args())

# Global vars
TOTAL_USERS = 2000


def _get_role_binding_dict(username, projectname):
    return {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
        "metadata": {
            "name": "admin-0",
            "namespace": projectname
        },
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "admin"
        },
        "subjects": [
            {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "User",
                "name": username
            }
        ]
    }


def _get_dbaas_tenant(username, projectname):
    return {
        "apiVersion": "dbaas.redhat.com/v1alpha1",
        "kind": "DBaaSTenant",
        "metadata": {
            "name": username
        },
        "spec": {
            "inventoryNamespace": projectname
        }
    }


if args["file"]:
    filename = args["file"]
    # if htpasswd file doesn't exist in local dir then create one.
    if not exists(filename):
        Path(filename).touch()
    with htpasswd.Basic(filename, mode="md5") as userdb:
        for index in range(1, TOTAL_USERS + 1, 1):
            try:
                userdb.add("user-" + str(index), "user" + str(index))
            except htpasswd.basic.UserExists as error:
                print(error)

if args["createprojects"]:
    batchSize = 100
    startUserIndexRange = 1
    for endUserIndexRange in range(batchSize, TOTAL_USERS + 1, batchSize):
        for userIndex in range(startUserIndexRange, endUserIndexRange + 1, 1):
            for projectIndex in range(1, 3, 1):
                oc.new_project("user-" + str(userIndex) + "-project-" + str(projectIndex))
        print("Processed batch {} to {}".format(startUserIndexRange, endUserIndexRange))
        startUserIndexRange = endUserIndexRange + 1
        time.sleep(2)

if args["deleteprojects"]:
    for userIndex in range(1, TOTAL_USERS + 1, 1):
        for projectIndex in range(1, 3, 1):
            oc.delete_project("user-" + str(userIndex) + "-project-" + str(projectIndex))

if args["giveadminrights"]:
    batchSize = 100
    startUserIndexRange = 1
    for endUserIndexRange in range(batchSize, TOTAL_USERS + 1, batchSize):
        for userIndex in range(startUserIndexRange, endUserIndexRange + 1, 1):
            username = "user-" + str(userIndex)
            for projectIndex in range(1, 3, 1):
                projectname = "user-" + str(userIndex) + "-project-" + str(projectIndex)
                rolebinding = _get_role_binding_dict(username, projectname)
                oc.apply(rolebinding)
        print("Processed batch {} to {}".format(startUserIndexRange, endUserIndexRange))
        startUserIndexRange = endUserIndexRange + 1
        time.sleep(1)

if args["removeadminrights"]:
    for userIndex in range(1, TOTAL_USERS + 1, 1):
        username = "User-" + str(userIndex)
        for projectIndex in range(1, 3, 1):
            projectname = "user-" + str(userIndex) + "-project-" + str(projectIndex)
            rolebinding = _get_role_binding_dict(username, projectname)
            oc.delete(rolebinding)

if args["createdbaastenant"]:
    batchSize = 100
    startUserIndexRange = 1
    for endUserIndexRange in range(batchSize, TOTAL_USERS + 1, batchSize):
        for userIndex in range(startUserIndexRange, endUserIndexRange + 1, 1):
            username = "user-" + str(userIndex)
            projectname = "user-" + str(userIndex) + "-project-1"
            dbaastenant = _get_dbaas_tenant(username, projectname)
            oc.apply(dbaastenant)
        print("Processed batch {} to {}".format(startUserIndexRange, endUserIndexRange))
        startUserIndexRange = endUserIndexRange + 1
        time.sleep(1)

# if args["test"]:
#     prg = oc.new_project("test")
#     print(prg.)
