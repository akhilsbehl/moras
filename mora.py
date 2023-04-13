#!/usr/bin/env python
"""Practice Kana."""
import csv
import datetime
import os
import sys
from typing import Dict
from typing import Tuple

import numpy as np
from termcolor import colored

KANA_TO_ROMAJI: Dict[str, Dict[str, str]] = {
    "Hiragana": {
        "あ": "a",
        "い": "i",
        "う": "u",
        "え": "e",
        "お": "o",
        "か": "ka",
        "き": "ki",
        "く": "ku",
        "け": "ke",
        "こ": "ko",
        "さ": "sa",
        "し": "shi",
        "す": "su",
        "せ": "se",
        "そ": "so",
        "た": "ta",
        "ち": "chi",
        "つ": "tsu",
        "て": "te",
        "と": "to",
        "な": "na",
        "に": "ni",
        "ぬ": "nu",
        "ね": "ne",
        "の": "no",
        "は": "ha",
        "ひ": "hi",
        "ふ": "fu",
        "へ": "he",
        "ほ": "ho",
        "ま": "ma",
        "み": "mi",
        "む": "mu",
        "め": "me",
        "も": "mo",
        "や": "ya",
        "ゆ": "yu",
        "よ": "yo",
        "ら": "ra",
        "り": "ri",
        "る": "ru",
        "れ": "re",
        "ろ": "ro",
        "わ": "wa",
        "を": "wo",
        "ん": "n",
    },
    "Katakana": {
        "ア": "a",
        "イ": "i",
        "ウ": "u",
        "エ": "e",
        "オ": "o",
        "カ": "ka",
        "キ": "ki",
        "ク": "ku",
        "ケ": "ke",
        "コ": "ko",
        "サ": "sa",
        "シ": "shi",
        "ス": "su",
        "セ": "se",
        "ソ": "so",
        "タ": "ta",
        "チ": "chi",
        "ツ": "tsu",
        "テ": "te",
        "ト": "to",
        "ナ": "na",
        "ニ": "ni",
        "ヌ": "nu",
        "ネ": "ne",
        "ノ": "no",
        "ハ": "ha",
        "ヒ": "hi",
        "フ": "fu",
        "ヘ": "he",
        "ホ": "ho",
        "マ": "ma",
        "ミ": "mi",
        "ム": "mu",
        "メ": "me",
        "モ": "mo",
        "ヤ": "ya",
        "ユ": "yu",
        "ヨ": "yo",
        "ラ": "ra",
        "リ": "ri",
        "ル": "ru",
        "レ": "re",
        "ロ": "ro",
        "ワ": "wa",
        "ヲ": "wo",
        "ン": "n",
    },
}


class PracticeAnalytics:
    """Analytics for the practice sessions."""

    def __init__(self, file_name: str = "analytics.csv"):
        """Initialize."""
        self.file_name = file_name
        self.analytics = self.load_analytics()
        self.current_session_data = {k: {} for k in KANA_TO_ROMAJI.keys()}

    def load_analytics(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Load the analytics data."""
        if not os.path.exists(self.file_name):
            self.create_new_analytics_file()

        analytics = {"Hiragana": {}, "Katakana": {}}
        with open(self.file_name, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                _, kana_type, kana, times_seen, times_correct, _ = row
                if kana not in analytics[kana_type]:
                    analytics[kana_type][kana] = {
                        "Times Seen": int(times_seen),
                        "Times Correct": int(times_correct),
                    }
                else:
                    analytics[kana_type][kana]["Times Seen"] \
                        += int(times_seen)
                    analytics[kana_type][kana]["Times Correct"] \
                        += int(times_correct)

        for kana_type in KANA_TO_ROMAJI.keys():
            for kana, data in analytics[kana_type].items():
                times_seen = data["Times Seen"]
                times_correct = data["Times Correct"]
                accuracy = times_correct / times_seen if times_seen != 0 else 0
                data["Accuracy"] = accuracy

        return analytics

    def create_new_analytics_file(self) -> None:
        """Create a new file for analytics the first time."""
        with open(self.file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Date",
                    "Kana Type",
                    "Kana",
                    "Times Seen",
                    "Times Correct",
                    "Accuracy"
                ]
            )

            today = datetime.date.today().strftime("%Y-%m-%d")
            for kana_type in KANA_TO_ROMAJI.keys():
                for kana in KANA_TO_ROMAJI[kana_type].keys():
                    writer.writerow([today, kana_type, kana, 0, 0, 0])

    def calculate_accuracies(self) -> Dict[str, Dict[str, float]]:
        """Calculate accuracies at Kana level."""
        accuracies = {"Hiragana": {}, "Katakana": {}}
        for kana_type in KANA_TO_ROMAJI.keys():
            for kana in self.analytics[kana_type]:
                times_seen = self.analytics[kana_type][kana]["Times Seen"]
                times_correct = self \
                    .analytics[kana_type][kana]["Times Correct"]
                accuracy = times_correct / times_seen if times_seen > 0 else 0
                accuracies[kana_type][kana] = accuracy
        return accuracies

    def calculate_sampling_rates(
        self, accuracies: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate sampling rates based on seen frequency and accuracy."""
        sampling_rates = {"Hiragana": {}, "Katakana": {}}

        for kana_type in KANA_TO_ROMAJI.keys():
            kana_data = [
                {
                    "kana": kana,
                    "times_seen": self
                    .analytics[kana_type][kana]["Times Seen"],
                    "accuracy": accuracy,
                }
                for kana, accuracy in accuracies[kana_type].items()
            ]

            min_seen = min(data["times_seen"] for data in kana_data)
            max_seen = max(data["times_seen"] for data in kana_data)
            min_accuracy = min(data["accuracy"] for data in kana_data)
            max_accuracy = max(data["accuracy"] for data in kana_data)

            if max_seen == min_seen:
                seen_range = 1
            else:
                seen_range = max_seen - min_seen

            if max_accuracy == min_accuracy:
                accuracy_range = 1
            else:
                accuracy_range = max_accuracy - min_accuracy

            adjusted_rates = {}
            for data in kana_data:
                seen_relative = (data["times_seen"] - min_seen) / seen_range
                accuracy_relative = (data["accuracy"] - min_accuracy) \
                    / accuracy_range

                if seen_relative < 0.5:
                    rate = 2 ** (1 - seen_relative * 2)
                else:
                    if accuracy_relative < 0.5:
                        rate = 1 + (1 - accuracy_relative * 2)
                    else:
                        rate = 1 - (accuracy_relative - 0.5) * 2

                adjusted_rates[data["kana"]] = rate

            total_adjusted_rate = sum(adjusted_rates.values())
            normalized_sampling_rate = {
                kana: rate / total_adjusted_rate
                for kana, rate in adjusted_rates.items()
            }

            sampling_rates[kana_type] = normalized_sampling_rate
        return sampling_rates

    def update_analytics_data(
            self, kana_type: str, kana: str, correct: bool
    ) -> None:
        """Update the analytics data for the current session."""
        if kana not in self.current_session_data[kana_type]:
            self.current_session_data[kana_type][kana] = {
                "Times Seen": 0,
                "Times Correct": 0,
            }

        self.current_session_data[kana_type][kana]["Times Seen"] += 1
        if correct:
            self.current_session_data[kana_type][kana]["Times Correct"] += 1

    def calculate_scores(
            self, from_session: Dict, kana_type: str
    ) -> Dict[str, int]:
        """Calculate scores for historical or current session."""
        total, correct = 0, 0
        for kana in from_session[kana_type]:
            total += from_session[kana_type][kana]["Times Seen"]
            correct += from_session[kana_type][kana]["Times Correct"]
        return {"total": total, "correct": correct}

    def calculate_total_scores(self, kana_type) -> Dict[str, int]:
        """Print the final scores."""
        current_scores = self.calculate_scores(
            self.current_session_data,
            kana_type
        )

        past_scores = self.calculate_scores(
            self.analytics,
            kana_type
        )

        session_scores = {
            k: current_scores[k] + past_scores[k] for k in
            current_scores.keys()
        }

        return session_scores

    def print_scores(self, from_session: str, kana_type: str) -> None:
        """Print the scores for historical or current session."""
        assert from_session in ("Current", "Past", "Total")

        if from_session == "Current":
            scores = self.calculate_scores(
                self.current_session_data,
                kana_type
            )
        elif from_session == "Past":
            scores = self.calculate_scores(self.analytics, kana_type)
        else:
            scores = self.calculate_total_scores(kana_type)

        percentage = (
            scores["correct"] / scores["total"] * 100
            if scores["total"] != 0
            else 0
        )

        print(
            f"{from_session} score:",
            colored(
                f"{scores['correct']}/"
                f"{scores['total']} "
                f"({percentage:.2f}%)",
                "blue",
                attrs=["bold"],
            ),
        )

    def save_analytics_data(self) -> None:
        """Save the analytics data to the file."""
        today = datetime.date.today().strftime("%Y-%m-%d")

        with open(self.file_name, "a") as file:
            writer = csv.writer(file)
            for kana_type, data in self.current_session_data.items():
                for kana, stats in data.items():
                    times_seen = stats["Times Seen"]
                    times_correct = stats["Times Correct"]
                    accuracy = times_correct / times_seen \
                        if times_seen != 0 else 0
                    row = [
                        today,
                        kana_type,
                        kana,
                        times_seen,
                        times_correct,
                        f"{accuracy:.2f}",
                    ]
                    writer.writerow(row)


class KanaPractice:
    """Practice Kana."""

    def __init__(self) -> None:
        """Initialize."""
        self.choices = ["Hiragana", "Katakana"]
        self.kana_type = None
        self.analytics = PracticeAnalytics()

    def ask_for_choice(self) -> None:
        """Ask the user for a choice."""
        try:
            while self.kana_type not in self.choices:
                user_input = input(
                    "Which one do you want to practice "
                    f"({', '.join(self.choices)})? "
                ).lower()
                matched_choices = [
                    c for c in self.choices if c.lower().startswith(user_input)
                ]
                if len(matched_choices) == 1:
                    self.kana_type = matched_choices[0]
                elif len(matched_choices) > 1:
                    print(
                        "Multiple matches found:",
                        f"{', '.join(matched_choices)}"
                    )
                else:
                    print("No matches found.")
        except KeyboardInterrupt:
            print("\nSession aborted.")
            sys.exit()
        else:
            self.fix_kana_sampling_rates()

    def fix_kana_sampling_rates(self) -> None:
        """Fix the sampling rates for the kana."""
        assert self.kana_type is not None
        kana_dict = KANA_TO_ROMAJI[self.kana_type]
        accuracies = self.analytics.calculate_accuracies()
        rates = self.analytics \
            .calculate_sampling_rates(accuracies)[self.kana_type]
        self.kanas = list(rates.keys())
        self.sampling_rates = list(rates.values())

    def get_random_kana(self) -> Tuple[str, str]:
        """Get a randomized kana."""
        kana = np.random.choice(self.kanas, p=self.sampling_rates)
        romaji = KANA_TO_ROMAJI[self.kana_type][kana]
        return kana, romaji

    def start_practice(self) -> None:
        """Start the session."""
        try:
            while True:
                kana, romaji = self.get_random_kana()
                self.prompt_kana_to_romaji(kana, romaji)
                assert self.kana_type is not None
                self.analytics.print_scores(
                    kana_type=self.kana_type,
                    from_session="Current",
                )

        except KeyboardInterrupt:
            self.finish_practice()

    def prompt_kana_to_romaji(self, kana: str, romaji: str) -> None:
        """Prompt the user for kana to romaji translation."""
        user_input = input(
            f"What is the romaji representation of {self.kana_type} "
            + colored(f"{kana}", "yellow", attrs=["bold"])
            + ": "
        )

        if user_input.lower() == romaji.lower():
            print(colored("\u2714 Correct!", "green", attrs=["bold"]))
            correct = True
        else:
            print(
                colored("\u2716 Incorrect!", "red", attrs=["bold"]),
                "The correct answer is ",
                colored(f"{romaji}", "red", attrs=["bold"]) + ".",
            )
            correct = False

        assert self.kana_type is not None
        self.analytics.update_analytics_data(self.kana_type, kana, correct)

    def finish_practice(self) -> None:
        """Finish the session."""
        assert self.kana_type is not None

        print("\nFinished practice.")
        self.analytics.print_scores(
            kana_type=self.kana_type,
            from_session="Past",
        )
        self.analytics.print_scores(
            kana_type=self.kana_type,
            from_session="Current",
        )
        self.analytics.print_scores(
            kana_type=self.kana_type,
            from_session="Total",
        )
        self.analytics.save_analytics_data()


if __name__ == "__main__":
    practice = KanaPractice()
    practice.ask_for_choice()
    practice.start_practice()
