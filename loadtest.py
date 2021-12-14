import htpasswd
import argparse
from os.path import exists
from pathlib import Path
import openshift as oc
import time

parser = argparse.ArgumentParser(description="Program to loadtest dbaas operator")
parser.add_argument("--createprojects", help="Create projects", default=False, action="store_true")
parser.add_argument("--from", help="Where to start from", required=True)
parser.add_argument("--to", help="Where to end", required=True)
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


def _get_role_binding_dict(user_name, project_name):
    return {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
        "metadata": {
            "name": "admin-0",
            "namespace": project_name
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
                "name": user_name
            }
        ]
    }


def _get_dbaas_tenant(user_name, project_name):
    return {
        "apiVersion": "dbaas.redhat.com/v1alpha1",
        "kind": "DBaaSTenant",
        "metadata": {
            "name": user_name
        },
        "spec": {
            "inventoryNamespace": project_name
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


def _process_batch(start_user_index, end_user_index):
    for user_index in range(start_user_index, end_user_index + 1, 1):
        user_name = "user-" + str(user_index)
        for project_index in range(1, 3, 1):
            if args["createprojects"]:
                continue
                # oc.new_project("user-" + str(user_index) + "-project-" + str(project_index))
            if args["deleteprojects"]:
                oc.delete_project("user-" + str(user_index) + "-project-" + str(project_index))
            if args["giveadminrights"]:
                project_name = "user-" + str(user_index) + "-project-" + str(project_index)
                role_binding = _get_role_binding_dict(user_name, project_name)
                oc.apply(role_binding)
            if args["removeadminrights"]:
                project_name = "user-" + str(user_index) + "-project-" + str(project_index)
                role_binding = _get_role_binding_dict(user_name, project_name)
                oc.delete(role_binding)
            if args["createdbaastenant"]:
                project_name = "user-" + str(user_index) + "-project-1"
                dbaas_tenant = _get_dbaas_tenant(user_name, project_name)
                oc.apply(dbaas_tenant)

    print("Processed batch {} to {}".format(start_user_index, end_user_index))


to_project = int(args["to"])
from_project = int(args["from"])
print("Projects from {} to {} will be processed".format(from_project, to_project))

if to_project - from_project > 100:
    batch_size = 100
    for end_user_index_range in range(from_project + batch_size, to_project + 1, batch_size):
        _process_batch(from_project, end_user_index_range)
        from_project = end_user_index_range + 1
        time.sleep(1)
else:
    _process_batch(from_project, to_project)

# if args["test"]:
#     prg = oc.new_project("test")
#     print(prg.)
