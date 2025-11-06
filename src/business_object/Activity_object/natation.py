from business_object.Activity_object.abstract_activity import AbstractActivity

class Natation(AbstractActivity):
    __mapper_args__ = {'polymorphic_identity': 'natation'}

    def vitesse(self) -> float:
        if self.duree and self.duree > 0:
            # distance en km, durée en minutes -> vitesse en m/s
            return (self.distance * 1000) / (self.duree * 60)
        return 0
