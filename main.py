import sys

from gitlab_api import GitLabAPI
from treelib import Tree
import argparse


def create_tree(root_node_name, subgroups):
    tree = Tree()
    root = tree.create_node(identifier=root_node_name, data=root_node_name)

    for subgroup in subgroups:
        n = tree.create_node(tag=subgroup, data=subgroup, parent=root)
        for member in subgroups[subgroup]:
            tag = "{0}, {1}, {2}".format(member["name"], member["username"], member["access_level"])
            tree.create_node(tag=tag, data=member, parent=n)

    return tree


def filter_by_username(pair, username):
    key, value = pair

    for user in value:
        if user["username"] == username:
            return True

    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='GitLabUtility', description="Utility for generating GitLab reports.")
    parser.add_argument("--gitlab_access_token", required=True, help="The access token for making calls to the GitLab REST API. See: https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html")
    parser.add_argument("--gitlab_host", required=True, help="The host name of the GitLab instance, e.g. gitlab.mydomain.com.")
    parser.add_argument("--gitlab_root_group_id", required=True, type=int, help="The group ID of the group to traverse for information. e.g. 7703.")
    parser.add_argument("--report", required=True, choices=["full_permission_tree", "member_permission_tree"], help="The type of reporting to be produced.")
    parser.add_argument("--for_username", required=False, default=None, metavar="USERNAME", help="The GitLab username of the user e.g. chcla15 to report permissions on. Only required with the report option 'member_permission_tree'.")

    args = parser.parse_args()

    api = GitLabAPI(args.gitlab_access_token, args.gitlab_host)
    root_group_url = api.get_group_information(args.gitlab_root_group_id)["web_url"]
    result = subgroups_and_projects = api.get_all_project_and_subgroup_members(args.gitlab_root_group_id)

    if args.report == "full_permission_tree":
        # Prints a tree structure of the whole hierarchy.
        print("----------------- Group and Project membership for all users for root group id {} -----------------".format(args.gitlab_root_group_id))
        create_tree(root_group_url, result).show()
    elif args.report == "member_permission_tree":
        if args.for_username == None:
            print("Argument USERNAME is missing for report type 'member_permission_tree'")
            sys.exit(1)

        # Filters the merged lists to find only groups that a given user is member of.
        username = args.for_username
        print("----------------- Group and Project membership for user {} starting at root group id {} -----------------".format(username, args.gitlab_root_group_id))
        filtered = dict(filter(lambda pair: filter_by_username(pair, username), result.items()))
        # Prints a tree structure of the hierarchy containing the specified username.
        create_tree(root_group_url, filtered).show()