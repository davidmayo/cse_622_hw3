import random

random.seed(40351)

POSSIBLE_ANSWERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
]

def random_answers(size: int = 20):
    return [
        random.choice(POSSIBLE_ANSWERS)
        for _
        in range(size)
    ]

def last_answers(size: int = 20):
    return [
        POSSIBLE_ANSWERS[-1]
        for _
        in range(size)
    ]

def random_guesses(size: int = 20):
    return [
        random.choice(POSSIBLE_ANSWERS)
        for _
        in range(size)
    ]

def score_test(
    correct_answers: list[str], test_taker_answers: list[str],
    print_results = False,
) -> float:
    correct_count = 0
    for count, (correct, test_taker) in enumerate(zip(correct_answers, test_taker_answers), start=1):
        is_correct = correct == test_taker
        if is_correct:
            correct_count += 1
        if print_results:
            print(f"    Question #{count}: Correct: {correct}  Answer: {test_taker}  {'CORRECT' if is_correct else 'INCORRECT'}")
    score = correct_count / len(correct_answers)
    if print_results:
        print(f"    Score: {score:%}")
    return score


if __name__ == "__main__":
    test_length = 3
    random_location_answers = random_answers(test_length)
    last_answers_ = last_answers(test_length)
    test_taker_guesses = random_guesses(test_length)
    # score_test(
    #     correct_answers=random_location_answers,
    #     test_taker_answers=test_taker_guesses,
    #     print_results=True
    # )

    sim_count = 10
    random_location_scores = []
    last_scores = []
    for test_taker in range(sim_count):
        random_location_answers = random_answers(test_length)
        last_answers_ = last_answers(test_length)
        test_taker_guesses = random_guesses(test_length)

        print(f"TEST TAKER #{test_taker+1} of {sim_count}")
        print(f"  Under 'LAST LOCATION' assumption:")
        last_scores.append(score_test(
            correct_answers=last_answers_,
            test_taker_answers=test_taker_guesses,
            print_results=True
        ))
        print(f"  Under 'RANDOM LOCATION' assumption:")
        random_location_scores.append(score_test(
            correct_answers=random_location_answers,
            test_taker_answers=test_taker_guesses,
            print_results=True
        ))

    def success_rate(scores: list[float], cutoff: float):
        count = 0
        for score in scores:
            if score >= cutoff:
                count += 1
        return count / len(scores)

    print()
    print(f"RESULTS FOR {sim_count:,} sims of {test_length:,} question test")

    last_answer_average = sum(last_scores) / len(last_scores)
    last_answer_success_rate = success_rate(last_scores, 0.5)
    print(f"LAST ANSWER STRATEGY:")
    print(f"  AVERAGE SCORE: {last_answer_average:%}")
    print(f"  PASS RATE: {last_answer_success_rate:%}")

    random_answer_average = sum(random_location_scores) / len(random_location_scores)
    random_answer_success_rate = success_rate(random_location_scores, 0.5)
    print(f"RANDOM LOCATION STRATEGY:")
    print(f"  AVERAGE SCORE: {random_answer_average:%}")
    print(f"  PASS RATE: {random_answer_success_rate:%}")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(f"matplotlib not available")
    else:
        bins = [
            t / 20.0
            for t
            in range(20+1)
        ]
        fig, [ax1, ax2] = plt.subplots(1,2)

        fig.suptitle(f"Running {sim_count:,} simulations of {test_length:,} question test")
        
        ax1: plt.Axes
        ax2: plt.Axes


        ax1.hist(last_scores, color="green", edgecolor="black", bins=bins)
        ax1.set_title("Candidate score distribution (Last Answer Assumption)")
        mean = sum(last_scores) / len(last_scores)
        ax1.axvline(mean, label=f"{mean=:.6f}", color="blue")

        ax2.hist(random_location_scores, color="green", edgecolor="black", bins=bins)
        ax2.set_title("Candidate score distribution (Random Location Assumption)")
        mean = sum(random_location_scores) / len(random_location_scores)
        ax2.axvline(mean, label=f"{mean=:.6f}", color="red")

        for ax in [ax1, ax2]:
            ax.set_xticks([bins[i] for i in range(len(bins)) if i % 4 == 0])
            ax.set_xlabel("Bins")
            ax.set_ylabel("Count")
            ax.axvline(0.5, label="passing (50%)", color="#888888")
            ax.legend()
        plt.show()

