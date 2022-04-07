# Description
This python script was designed to help loadtest dbaas-operator
in a sandbox like environment by creating objects specify to it 
but it can be used for other projects too. Just add your 
Custom Resouce (CR) template in templates.py _get_ondemand_template().

For example if you have a k8s CR named: `SillyCustomResource`

you can define it _get_ondemand_template() and can run using 
`./loadtest.py --task createondemand --from 20 --to 100`

The above command will then create two `SillyCustomResource` in two
respective namespaces of user 20 all the way to user 100.

## command
`cd $WORK_DIR`
`$./loadtest -h`

# usage
```
usage: loadtest [-h]
                [--task [
                    {
                      createprojects,deleteprojects,
                      giveadminrights,removeadminrights,
                      createdbaastenants,removedbaastenants,
                      createrandomobjects,
                      createdbaasinventory,
                      createdbaasconn,
                      createondemand
                    }
                  ]
                ]
                --from FROM --to TO [--file FILE]

Program to loadtest dbaas operator

options:
  -h, --help            show this help message and exit
  --task [{createprojects,deleteprojects,giveadminrights,removeadminrights,createdbaastenants,removedbaastenants,createrandomobjects,createdbaasinventory,createdbaasconn,createondemand}]
                        Select what to task perform
  --from FROM           Where to start from. example: --from 1 (represents user 1)
  --to TO               Where to end. example: --to 2000 (represents user 2000)
  --file FILE           Enter htpasswd file path
```