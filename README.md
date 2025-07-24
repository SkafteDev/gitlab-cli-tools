# Description
This repo contains some scripting for interacting with the GitLab REST API programatically.
The main purpose is to include features that are not supported out of the box by GitLab.'

## Reporting feature
The reporting feature enables the creation of unicode trees with subgroups and projects.

### Full permission tree
Reports the whole project/subgroup structure with members and their permission level - starting from a given root group id.

Example:
```sh
python main.py --gitlab_access_token "xyz" --gitlab_host gitlab.example.com --gitlab_root_group_id 0000 --report full_permission_tree

----------------- Group and Project membership for all users for root group id 0000 -----------------
https://gitlab.example.com/groups/group-0
├── https://gitlab.example.com/groups/group-0/subgroup-1
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/subgroup-2
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/subgroup-3
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/subgroup-3/project-a
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/subgroup-4
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/subgroup-4/project-b
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/subgroup-4/project-c
│   ├── User A, user_a, AccessLevel.OWNER
│   ├── User B, user_b, AccessLevel.OWNER
│   └── User C, user_c, AccessLevel.OWNER
├── https://gitlab.example.com/groups/group-0/public-projects
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/archived/project-1
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/subgroup-3/project-a/experiment-1
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/subgroup-3/project-a/project-unreal
│   ├── User A, user_a, AccessLevel.OWNER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/subgroup-4/project-b/module-1
│   ├── User A, user_a, AccessLevel.OWNER
│   ├── User D, user_d, AccessLevel.DEVELOPER
│   └── User B, user_b, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/subgroup-4/project-c/code-repo
│   ├── User A, user_a, AccessLevel.OWNER
│   ├── User B, user_b, AccessLevel.OWNER
│   ├── Bot A, bot_a, AccessLevel.GUEST
│   ├── User E, user_e, AccessLevel.MAINTAINER
│   ├── User F, user_f, AccessLevel.MAINTAINER
│   ├── User G, user_g, AccessLevel.MAINTAINER
│   ├── Bot B, bot_b, AccessLevel.GUEST
│   └── User C, user_c, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/subgroup-4/project-c/data-repo
│   ├── User A, user_a, AccessLevel.OWNER
│   ├── User B, user_b, AccessLevel.OWNER
│   ├── User E, user_e, AccessLevel.MAINTAINER
│   ├── User F, user_f, AccessLevel.MAINTAINER
│   ├── User G, user_g, AccessLevel.MAINTAINER
│   ├── User H, user_h, AccessLevel.MAINTAINER
│   ├── User I, user_i, AccessLevel.MAINTAINER
│   └── User C, user_c, AccessLevel.OWNER
├── https://gitlab.example.com/group-0/subgroup-4/project-c/model-repo
│   ├── User A, user_a, AccessLevel.OWNER
│   ├── User B, user_b, AccessLevel.OWNER
│   ├── User E, user_e, AccessLevel.MAINTAINER
│   ├── User F, user_f, AccessLevel.MAINTAINER
│   ├── User G, user_g, AccessLevel.MAINTAINER
│   ├── User H, user_h, AccessLevel.MAINTAINER
│   ├── User I, user_i, AccessLevel.MAINTAINER
│   └── User C, user_c, AccessLevel.OWNER
└── https://gitlab.example.com/group-0/public-projects/opensource-1
    ├── User A, user_a, AccessLevel.OWNER
    └── User B, user_b, AccessLevel.OWNER

```

### Member permission tree
Reports the subset of the project/subgroup structure that contains permissions for a given username - starting from a given root group id.

Example:

```sh
python main.py --gitlab_access_token "xyz" --gitlab_host gitlab.example.com --gitlab_root_group_id 0000 --report member_permission_tree --for_username user_i

----------------- Group and Project membership for user user_i starting at root group id 0000 -----------------
https://gitlab.example.com/groups/group-0
├── https://gitlab.example.com/group-0/subgroup-1/project-a
│   ├── User A, user_a, AccessLevel.OWNER
│   ├── User B, user_b, AccessLevel.OWNER
│   ├── User E, user_e, AccessLevel.MAINTAINER
│   ├── User F, user_f, AccessLevel.MAINTAINER
│   ├── User G, user_g, AccessLevel.MAINTAINER
│   ├── User H, user_h, AccessLevel.MAINTAINER
│   ├── User I, user_i, AccessLevel.MAINTAINER
│   └── User C, user_c, AccessLevel.OWNER
└── https://gitlab.example.com/group-0/subgroup-1/project-b
    ├── User A, user_a, AccessLevel.OWNER
    ├── User B, user_b, AccessLevel.OWNER
    ├── User E, user_e, AccessLevel.MAINTAINER
    ├── User F, user_f, AccessLevel.MAINTAINER
    ├── User G, user_g, AccessLevel.MAINTAINER
    ├── User H, user_h, AccessLevel.MAINTAINER
    ├── User I, user_i, AccessLevel.MAINTAINER
    └── User C, user_c, AccessLevel.OWNER
```
