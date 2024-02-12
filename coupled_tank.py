import dataclasses

@dataclasses.dataclass
class CoupledTankSim:
    a1: float
    a2: float
    f0: float
    f1: float
    f2: float
    h1: float
    h2: float

    def __post_init__(self):
        self.k: int = 1
        self.h1_empty = self.h1 <= 0.0
        self.h2_empty = self.h2 <= 0.0

    def step(self, count: int = 1):
        """Do `count` steps of the simulation. Defaults to 1 step.
        """
        for _ in range(count):
            self._single_step()

    def _single_step(self):
        """Do a single step of the simulation
        """
        self.h1_empty_previous = self.h1_empty
        self.h2_empty_previous = self.h2_empty

        # Account for empty tanks
        self.h1_empty = self.h1 <= 0.0
        self.h2_empty = self.h2 <= 0.0

        # If emptiness status changed, print to screen
        # (Could do more elegant analysis of this, if desired.)
        if self.h1_empty_previous != self.h1_empty:
            string = "empty" if self.h1_empty else "not empty"
            print(f"Tank 1 became {string} during step k={self.k}")
        if self.h2_empty_previous != self.h2_empty:
            string = "empty" if self.h2_empty else "not empty"
            print(f"Tank 2 became {string} during step k={self.k}")

        if self.h1_empty:
            self.h1 = 0.0
            self.f2 = self.f1
        if self.h2_empty:
            self.h2 = 0.0
            self.f0 = self.f2

        # Difference equations, given in problem appendix.
        delta_h1 = (self.f1 - self.f2) / self.a1
        delta_h2 = (self.f2 - self.f0) / self.a2
        self.h1 += delta_h1
        self.h2 += delta_h2
        self.k += 1


if __name__ == "__main__":
    sim = CoupledTankSim(
        a1=1.0,
        a2=2.0,
        f2=0.01,
        f1=0.01,
        f0=0.02,
        h1=0.0,
        h2=1.5,
    )
    number_of_simulations = 50
    print(f"Initial parameters: {sim}")
    for _ in range(number_of_simulations):
        # print(f"{sim.k=}   {sim.h1=}   {sim.h2=}")
        print(sim)
        sim.step(10)
        