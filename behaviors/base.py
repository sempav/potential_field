class BehaviorBase():
    """
    "Abstract" base class for movement logic.

    Any concrete subclass must redefine calc_desired_velocity.
    """

    def calc_desired_velocity(self, bots, obstacles, targets):
        raise NotImplemented


    def update_vel(self, bots, obstacles, targets):
        self.vel = self.calc_desired_velocity(bots, obstacles, targets)


    def sync_to_real(self, real):
        self.pos = real.pos
        self.vel = real.vel


