import github3  # type:ignore
from social_api import BaseSocialNetworkConnector, Profile, Content
from pprint import pprint


class GithubConnector(BaseSocialNetworkConnector):
    """Specific connector to Github as a social network."""

    def __init__(self, **kwargs):
        """Constructor accepts the same parameters as github3.GitHub object.

        more details here:
        https://github3py.readthedocs.io/en/master/api-reference/github.html#github3.github.GitHub
        """
        # using username and password
        self.api = github3.GitHub(**kwargs)

    @staticmethod
    def build_profile(payload) -> Profile:
        if payload.name:
            name = payload.name
        else:
            name = payload.email
        return {
            "visible_name": name,
            "unique_id": payload.login
        }

    @staticmethod
    def build_content(payload) -> Content:
        return {
            "text": payload.description,
            "date": payload.created_at
        }

    def get_user_profile(self, username):
        """Get basic profile information for a user by ID or screen_name

        :param username: ID or screen_name
        """
        if username:
            res = self.api.user(username)
        else:
            res = self.api.me()
        return GithubConnector.build_profile(res)

    def get_personal_followers(self):
        for short_user in self.api.followers():
            yield self.get_user_profile(short_user.login)

    def get_personal_content(self):
        for g in self.api.gists():
            yield GithubConnector.build_content(g)
