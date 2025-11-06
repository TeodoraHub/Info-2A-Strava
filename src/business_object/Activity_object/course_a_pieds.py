from business_object.Activity_object.abstract_activity import AbstractActivity


class CoursePied(AbstractActivity):
    __tablename__ = 'activities'
    __mapper_args__ = {
        'polymorphic_identity': 'course',
        'polymorphic_on': 'sport'
    }

    def vitesse(self) -> float:
        if self.duree and self.duree > 0:
            return self.distance / self.duree
        return 0.0
