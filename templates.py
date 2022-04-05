
def get_template(obj_name, user_name, project_name):
    if obj_name == "rolebinding":
        return globals()["_get_"+obj_name+"_template"](user_name, project_name)
    else:
        return globals()["_get_"+obj_name+"_template"](project_name)

# Rolebinding template to give admin access to user to its projects.
def _get_rolebinding_template(user_name, project_name):
    return {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
        "metadata": {
            "name": "admin-0",
            "namespace": project_name,
            "labels": {
                "auto": "true"
            }
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

# DBaaS tenants for given namespace/project.
def _get_dbaastenant_template(project_name):
    return {
        "apiVersion": "dbaas.redhat.com/v1alpha1",
        "kind": "DBaaSTenant",
        "metadata": {
            "name": project_name
        },
        "spec": {
            "inventoryNamespace": project_name
        }
    }

# Deployment template which runs busybox.
def _get_deployment_template(project_name):
    return {
        "kind": "Deployment",
        "apiVersion": "apps/v1",
        "metadata": {
            "name": "fake-nginx-" + project_name,
            "namespace": project_name,
            "labels": {
                "auto": "true",
                "app": "nginx-"+project_name
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": "nginx-"+project_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "nginx-"+project_name,
                        "auto": "true"
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": "deployed-pod",
                            "imagePullPolicy": "IfNotPresent",
                            "image": "docker.io/library/busybox:latest",
                            "command": [
                                "sleep",
                                "3600"
                            ],
                            "resources": {}
                        }
                    ]
                }
            },
            "strategy": {}
        },
        "status": {}
    }

# Secret template 
def _get_secret_template(project_name):
    return {
        "kind": "Secret",
        "apiVersion": "v1",
        "metadata": {
            "name": "secret-" + project_name,
            "namespace": project_name,
            "labels": {
                "auto": "true",
            }
        },
        "data": {
            "rubbish": "c2VjcmV0"
        }
    }

# CM template
def _get_configmap_template(project_name):
    return {
        "kind": "ConfigMap",
        "apiVersion": "v1",
        "metadata": {
            "name": "cm-" + project_name,
            "namespace": project_name,
            "labels": {
                "auto": "true",
            }
        },
        "data": {
            "key1": "config1"
        }
    }

# DBaaSInventory template
def _get_dbaasinventory_template(project_name):
    return {
        "apiVersion": "dbaas.redhat.com/v1alpha1",
        "kind": "DBaaSInventory",
        "metadata": {
            "name": project_name,
            "labels": {
                "auto": "true"
            }
        },
        "spec": {
            "credentialsRef": {
                "name": "dbaas-vendor-credentials-1648576236501",
                "namespace": "openshift-dbaas-operator"
            },
            "providerRef": {
                "name": "crunchy-bridge-registration"
            }
        }
    }

# DBaaSConnection Template
def _get_dbaasconnection_template(project_name):
    return {
        "apiVersion": "dbaas.redhat.com/v1alpha1",
        "kind": "DBaaSConnection",
        "metadata": {
            "name": "conn-"+project_name,
            "labels": {
                "auto": "true"
            }
        },
        "spec": {
            "instanceID": "6jlbpbvlyrahlcxouew3vkhiuu",
            "inventoryRef": {
                "name": project_name,
            }
        }
    }

# Use the below to define a template on-demand.
def _get_ondemand_template(project_name):
    return {
        "apiVersion": "dbaas.redhat.com/v1alpha1",
        "kind": "CrdbDBaaSInventory",
        "metadata": {
            "name": project_name,
            "namespace": "openshift-dbaas-operator",
            "labels": {
                "auto": "true"
            }
        },
        "spec": {
            "credentialsRef": {
                "name": "dbaas-vendor-credentials-1648825772443",
                "namespace": "openshift-dbaas-operator"
            }
        }
    }