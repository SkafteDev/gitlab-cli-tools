from gitlab_api import GitLabAPI
from treelib import Tree


def create_tree(root_node_name, subgroups):
    tree = Tree()
    root = tree.create_node(identifier=root_node_name, data=root_node_name)

    for subgroup in subgroups:
        n = tree.create_node(tag=subgroup, datga=subgroup, parent=root)
        for member in subgroups[subgroup]:
            tree.create_node(tag=member["name"], data=member, parent=n)

    return tree


gitlab_access_token = "PATsAy6ocVtA7oUKUCQiWDw"
gitlab_url = "gitlab.sdu.dk"
gitlab_root_group_id = 672
gitlab_root_group_name = "cei"

api = GitLabAPI(gitlab_access_token, gitlab_url)
subgroup_members = api.get_all_subgroup_members(gitlab_root_group_id)
project_members = api.get_all_project_members(gitlab_root_group_id)

# Merges the dictionaries to form a combined report of memberships.
merged = {**subgroup_members, **project_members}
# Prints a tree structure of the whole hierarchy.
print("----------------- Group and Project membership for all users for root group id {} -----------------".format(gitlab_root_group_id))
create_tree(gitlab_url + "/" + gitlab_root_group_name, merged).show()

username = "chcla15"
def filter_by_username(pair):
    key, value = pair

    for user in value:
        if user["username"] == username:
            return True

    return False


# Filters the merged lists to find only groups that a given user is member of.
print("----------------- Group and Project membership for user {} -----------------".format(username))
filtered = dict(filter(filter_by_username, merged.items()))
# Prints a tree structure of the hierarchy containing the specified username.
create_tree(gitlab_url + "/" + gitlab_root_group_name, filtered).show()