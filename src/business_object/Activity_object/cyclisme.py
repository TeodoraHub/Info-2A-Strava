from business_object.Activity_object.abstract_activity import AbstractActivity

class Cyclisme(AbstractActivity):
    __mapper_args__ = {'polymorphic_identity': 'cyclisme'}

    def vitesse(self) -> float:
        if self.duree and self.duree > 0:
            return (self.distance / self.duree) * 60  # km/h
        return 0
