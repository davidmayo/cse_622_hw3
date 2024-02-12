import random
from math import sqrt

random.seed(40351)

# Problem explicitly states that the function that returns
# uniform numbers from [0,1) should be called "rand"
rand = random.random

def F_inverse(x: float) -> float:
    """Inverse distribution function for the given triangle distribution"""
    if 0.0 <= x and x <= 0.5:
        return sqrt(2.0 * x)
    elif 0.0 < x and x <= 1.0:
        return 2.0 - sqrt(2.0 - 2.0 * x)
    else:
        raise ValueError(f"X value out of bounds: {x=!r}")
    
def triangle_variate() -> float:
    """Variate generator for the given """
    return F_inverse(rand())

if __name__ == "__main__":
    n = 100000
    results = [
        triangle_variate()
        for _
        in range(n)
    ]

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(f"matplotlib not installed")
    else:
        bins = [
            t / 10.0
            for t
            in range(0, 21)
        ]
        plt.hist(results, color="red", edgecolor="black", bins=bins)
        plt.title(f"{n=:,} points")
        plt.xlabel("Bin")
        plt.xticks(bins)
        plt.ylabel("Count")
        plt.show()