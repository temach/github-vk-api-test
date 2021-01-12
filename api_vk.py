import vk_api  # type:ignore
from social_api import BaseSocialNetworkConnector, Profile, Content
from typing import TypedDict, Generator, Iterator, Any
from datetime import datetime


class VkontakteConnector(BaseSocialNetworkConnector):
    """Specific connector for the vkontakte social network."""

    def __init__(self, **kwargs):
        """Constructor accepts the same parameters as VkApi.

        more details:
        https://github.com/python273/vk_api/blob/571bb92fba174c827aba874c190f0d4f05264120/vk_api/vk_api.py#L88
        """

        session = vk_api.VkApi(**kwargs)
        try:
            session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            raise
        self.api = session.get_api()

    @staticmethod
    def build_profile(payload) -> Profile:
        return {
            "visible_name": "{} {}".format(payload["first_name"], payload["last_name"]),
            "unique_id": payload["id"]
        }

    @staticmethod
    def build_content(payload) -> Content:
        return {
            "text": payload["text"],
            "date": datetime.fromtimestamp(payload["date"])
        }

    def get_user_profile(self, username: str = None) -> Profile:
        """Get basic profile information for a user by ID or screen_name

        :param username: ID or screen_name
        """
        if username:
            res: dict[str, Any] = self.api.users.get(user_ids=username).pop()
        else:
            res = self.api.users.get().pop()
        return VkontakteConnector.build_profile(res)

    def get_personal_followers(self) -> Generator[Profile, None, None]:
        for user_id in self.api.users.getFollowers()["items"]:
            yield self.get_user_profile(user_id)

    def get_personal_content(self) -> Generator[Content, None, None]:
        for p in self.api.wall.get()["items"]:
            yield VkontakteConnector.build_content(p)
