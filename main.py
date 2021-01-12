#!/usr/bin/env python3
from social_api import SocialNetworkConnector
from api_vk import VkontakteConnector
from api_github import GithubConnector
from pprint import pprint


def main():
    vk_conn = VkontakteConnector(
        login="LOGIN", password="PASSWORD"
        # token="TOKEN"
    )

    github_conn = GithubConnector(
        # login="LOGIN", password="PASSWORD"
        token="TOKEN"
    )

    universal = SocialNetworkConnector({
        "vk.com": vk_conn,
        "github.com": github_conn,
    })

    universal.current_connector("vk.com")
    pprint(universal.get_user_profile(""))
    pprint(list(universal.get_personal_content()))
    pprint(list(universal.get_personal_followers()))

    universal.current_connector("github.com")
    pprint(universal.get_user_profile(""))
    pprint(list(universal.get_personal_content()))
    pprint(list(universal.get_personal_followers()))


if __name__ == "__main__":
    main()
