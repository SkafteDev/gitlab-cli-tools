import requests
from gitlab_access_levels import AccessLevel
import logging, sys


class GitLabAPI:
    def __init__(self, access_token, gitlab_url):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.results_per_page = 100  # 100 is max.
        self.access_token = access_token
        self.gitlab_url = gitlab_url
        self.session = requests.Session()
        self.session.headers.update({"PRIVATE-TOKEN": self.access_token})

    def set_results_per_page(self, results_per_page):
        self.results_per_page = results_per_page

    def __traverse_pages__(self, url):
        logging.info("GET: {}".format(url))
        all_pages_content = list()

        response = self.session.get(url)
        all_pages_content.extend(response.json())

        next_page = response.links.get("next")
        while next_page is not None:
            response = self.session.get(next_page["url"])
            response_json = response.json()
            all_pages_content.extend(response_json)
            next_page = response.links.get("next")

        return all_pages_content

    def __init_member__(self, member_data):
        username = member_data["username"]
        name = member_data["name"]
        access_level = AccessLevel(member_data["access_level"])
        member = {
            'username': username,
            'name': name,
            'access_level': AccessLevel(access_level)
        }

        return member

    def get_group_information(self, gitlab_group_id):
        group_information_url = "https://{}/api/v4/groups/{}?with_projects=false" \
            .format(self.gitlab_url, gitlab_group_id)
        response = self.session.get(group_information_url).json()

        return response

    """Returns all projects for the given root group id. Including archived projects."""
    def get_all_projects(self, gitlab_root_group_id):
        all_projects_url = "https://{}/api/v4/groups/{}/projects?include_subgroups=true&per_page={}" \
            .format(self.gitlab_url, gitlab_root_group_id, self.results_per_page)
        response = self.__traverse_pages__(all_projects_url)

        return response

    """Returns all subgroups (including descendants) of the given gitlab root group id."""
    def get_all_subgroups(self, gitlab_root_group_id):
        all_subgroups_url = "https://{}/api/v4/groups/{}/descendant_groups?per_page={}" \
            .format(self.gitlab_url, gitlab_root_group_id, self.results_per_page)
        response = self.__traverse_pages__(all_subgroups_url)

        return response

    def get_all_subgroup_members(self, gitlab_root_group_id):
        subgroups = self.get_all_subgroups(gitlab_root_group_id)

        out = dict()

        for subgroup in subgroups:
            subgroup_id = subgroup["id"]
            subgroup_full_path = subgroup["web_url"]
            out[subgroup_full_path] = list()

            all_members_url = "https://{}/api/v4/groups/{}/members/all?&per_page={}" \
                .format(self.gitlab_url, subgroup_id, self.results_per_page)
            members = self.__traverse_pages__(all_members_url)

            for member_data in members:
                member = self.__init_member__(member_data)
                out[subgroup_full_path].append(member)

        return out

    """Returns all members including subgroups for the given root group id."""
    def get_all_project_members(self, gitlab_root_group_id):
        projects = self.get_all_projects(gitlab_root_group_id)

        out = dict()

        for project in projects:
            project_id = project["id"]
            path_with_namespace = project["web_url"]
            out[path_with_namespace] = list()

            all_members_url = "https://{}/api/v4/projects/{}/members/all?&per_page={}" \
                .format(self.gitlab_url, project_id, self.results_per_page)
            members = self.__traverse_pages__(all_members_url)

            for member_data in members:
                member = self.__init_member__(member_data)
                out[path_with_namespace].append(member)

        return out

    def get_all_project_and_subgroup_members(self, gitlab_root_group_id):
        subgroup_members = self.get_all_subgroup_members(gitlab_root_group_id)
        project_members = self.get_all_project_members(gitlab_root_group_id)

        # Merges the dictionaries to form a combined report of memberships.
        merged = {**subgroup_members, **project_members}

        return merged
