from business_object.Activity_object.abstract_activity import AbstractActivity


class CoursePied(AbstractActivity):
    """Activité de course à pied"""

    def __init__(self, id_activite, titre, description, date_activite, duree, distance, id_user):
        super().__init__(id_activite, titre, description, date_activite, duree, distance, id_user)

    def __str__(self):
        return f" {self.get_type_activite()} - {super().__str__()}"
