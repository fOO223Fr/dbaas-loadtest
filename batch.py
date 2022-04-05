from templates import get_template
import random
import openshift as oc


def _process_batch(task, start_user_index, end_user_index):
    print("Launched batch {} to {} for task {}".format(start_user_index, end_user_index, task))
    
    for user_index in range(start_user_index, end_user_index + 1, 1):
        
        user_name = "user-" + str(user_index)

        for project_index in range(1, 3, 1):
            
            project_name = "user-" + str(user_index) + "-project-" + str(project_index)
            
            match task:
                case "createprojects":
                    oc.new_project("user-" + str(user_index) + "-project-" + str(project_index))
                case "deleteprojects":
                    oc.delete_project("user-" + str(user_index) + "-project-" + str(project_index))
                case "giveadminrights":
                    role_binding = get_template("rolebinding", user_name, project_name)
                    oc.apply(role_binding)
                case "removeadminrights":
                    role_binding = get_template("rolebinding", user_name, project_name)
                    oc.delete(role_binding, ignore_not_found=True)
                case "createdbaastenants":
                    dbaas_tenant = get_template("dbaastenant", project_name)
                    oc.apply(dbaas_tenant)
                case "removedbaastenants":
                    dbaas_tenant = get_template("dbaastenant", project_name)
                    oc.delete(dbaas_tenant, ignore_not_found=True)
                case "createrandomobjects":
                    deploy_template = get_template("deployment", project_name)
                    secret_template = get_template("secret", user_name, project_name)
                    configmap_template = get_template("configmap", user_name, project_name)
                    options = ["deploy", "secret", "configmap"]
                    random_choose_object = random.choice(options)+"_template"
                    oc.apply(locals()[random_choose_object])
                    # oc.apply(deploy_template)
                case "createdbaasinventory":
                    dbaas_inventory_template = get_template("dbaasinventory", project_name)
                    oc.apply(dbaas_inventory_template)
                case "createdbaasconn":
                    dbaas_connection_template = get_template("dbaasconnection", project_name)
                    oc.apply(dbaas_connection_template)
                case "createondemand":
                    ondemand_template = get_template("ondemand", project_name)
                    oc.apply(ondemand_template)

    print("Processed batch {} to {} for task {}".format(start_user_index, end_user_index, task))