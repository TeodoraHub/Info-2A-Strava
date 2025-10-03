from business_object.Activity_object.abstract_activity import AbstractActivity
from business_object.User_object import utilisateur


class FilActualite:
    def __init__(self):
        self.activites: list[AbstractActivity] = []

    def obtenir_activites(self, user: utilisateur) -> list[AbstractActivity]:
        return self.activites
