from random import randint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_coin_sequence(sequence_length: int) -> list:
    coin_flips = []
    conversion_dict = {0: "H", 1: "T"}
    number_of_flips = sequence_length
    for i in range(number_of_flips):
        coin_flip = randint(a=0, b=1)
        coin_flips.append(conversion_dict[coin_flip])
    return coin_flips


def score_sequence(flip_sequence: list) -> dict:
    alice_score = 0
    bob_score = 0
    for i in range(1, len(flip_sequence)):
        current_flip = flip_sequence[i]
        previous_flip = flip_sequence[i - 1]
        test_sequence = previous_flip + current_flip
        if test_sequence == "HH":
            alice_score = alice_score + 1
        if test_sequence == "HT":
            bob_score = bob_score + 1

    return_val = {"alice_score": alice_score, "bob_score": bob_score}

    return return_val


def run_simulation(num_simulations: int, num_flips: int) -> pd.DataFrame:
    all_alice_scores = []
    all_bob_scores = []
    for i in range(num_simulations):
        sequence = create_coin_sequence(num_flips)
        scores = score_sequence(sequence)
        all_alice_scores.append(scores["alice_score"])
        all_bob_scores.append(scores["bob_score"])

    scores_df = pd.DataFrame()
    scores_df["alice"] = all_alice_scores
    scores_df["bob"] = all_bob_scores
    scores_df["ratio"] = scores_df["alice"] / scores_df["bob"]
    scores_df["win"] = np.where((scores_df["alice"]) > (scores_df["bob"]), "a", "b")

    return scores_df

df = run_simulation(num_simulations=10_000, num_flips=100)
print(df["win"].value_counts())