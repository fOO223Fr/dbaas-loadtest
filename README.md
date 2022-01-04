## command
`cd $WORK_DIR`
`$./loadtest -h`

# usage
```
usage: loadtest [-h]
                [--task [
                    {
                        createprojects,
                        deleteprojects,
                        giveadminrights,
                        removeadminrights,
                        createdbaastenants,
                        removedbaastenants
                    }
                ]
                ]
                --from FROM --to TO [--file FILE]

Program to loadtest dbaas operator

options:
  -h, --help            show this help message and exit
  --task [{createprojects,deleteprojects,giveadminrights,removeadminrights,createdbaastenants,removedbaastenants}]
                        Select what to task perform
  --from FROM           Where to start from. example: --from 1 (represents user 1)
  --to TO               Where to end. example: --to 2000 (represents user 2000)
  --file FILE           Enter htpasswd file path
```