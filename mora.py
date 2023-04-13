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
        self.current_session_data = {"Hiragana": {}, "Katakana": {}}

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

        for kana_type in analytics:
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

    def calculate_accuracies(self) -> Dict[str, Dict[str, float]]:
        """Calculate accuracies at Kana level."""
        accuracies = {"Hiragana": {}, "Katakana": {}}
        for kana_type in self.analytics:
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
        """Calculate sampling rates inversely proportional to accuracies."""
        sampling_rates = {"Hiragana": {}, "Katakana": {}}
        for kana_type in accuracies:
            reciprocal_accuracies = {
                kana: max(20, 1 / accuracy)
                for kana, accuracy in accuracies[kana_type].items()
            }
            total_reciprocal_accuracy = sum(reciprocal_accuracies.values())
            normalized_sampling_rate = {
                kana: reciprocal_accuracy / total_reciprocal_accuracy
                for kana, reciprocal_accuracy in reciprocal_accuracies.items()
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

    @property
    def session_score(self) -> Dict[str, int]:
        """Return the session score."""
        total, correct = 0, 0
        for kana_type in self.current_session_data:
            for kana in self.current_session_data[kana_type]:
                total += self \
                    .current_session_data[kana_type][kana]["Times Seen"]
                correct += self \
                    .current_session_data[kana_type][kana]["Times Correct"]
        return {"total": total, "correct": correct}

    def print_session_scores(self) -> None:
        """Print the session scores."""
        session_score = self.session_score
        percentage = (
            session_score["correct"] / session_score["total"] * 100
            if session_score["total"] != 0
            else 0
        )
        print(
            "Session score:",
            colored(
                f"{session_score['correct']}/"
                f"{session_score['total']} "
                f"({percentage:.2f}%)",
                "blue",
                attrs=["bold"],
            ),
        )

    def calculate_final_scores(self) -> float:
        """Print the final scores."""
        session_score = self.session_score
        session_percentage = (
            session_score["correct"] / session_score["total"] * 100
            if session_score["total"] != 0
            else 0
        )
        return session_percentage

    def print_final_scores(self) -> None:
        """Print the final scores."""
        session_percentage = self.calculate_final_scores()
        session_score = self.session_score

        print(
            colored(
                f"\nFinal score: {session_score['correct']}/"
                f"{session_score['total']} "
                f"({session_percentage:.2f}%)",
                "blue",
                attrs=["bold"],
            )
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
        self.selected_choice = None
        self.analytics = PracticeAnalytics()

    def ask_for_choice(self) -> None:
        """Ask the user for a choice."""
        try:
            while self.selected_choice not in self.choices:
                user_input = input(
                    "Which one do you want to practice "
                    f"({', '.join(self.choices)})? "
                ).lower()
                matched_choices = [
                    c for c in self.choices if c.lower().startswith(user_input)
                ]
                if len(matched_choices) == 1:
                    self.selected_choice = matched_choices[0]
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

    def get_random_kana(self) -> Tuple[str, str]:
        """Get a randomized kana."""
        assert self.selected_choice is not None
        kana_dict = KANA_TO_ROMAJI[self.selected_choice]
        rates = self.analytics.calculate_sampling_rates(
            self.analytics.calculate_accuracies()
        )
        kana = np.random.choice(list(kana_dict.keys()), p=rates)
        romaji = kana_dict[kana]
        return kana, romaji

    def start_practice(self) -> None:
        """Start the session."""
        try:
            while True:
                kana, romaji = self.get_random_kana()
                self.prompt_kana_to_romaji(kana, romaji)
                self.analytics.print_session_scores()

        except KeyboardInterrupt:
            self.finish_practice()

    def prompt_kana_to_romaji(self, kana: str, romaji: str) -> None:
        """Prompt the user for kana to romaji translation."""
        user_input = input(
            f"What is the romaji representation of {self.selected_choice} "
            + colored(f"{kana}", "yellow", attrs=["bold"])
            + ": "
        )
        kana_type = self.selected_choice
        assert kana_type is not None
        self.analytics \
            .current_session_data[kana_type][kana]['Times Seen'] \
            += 1

        if user_input.lower() == romaji.lower():
            print(colored("\u2714 Correct!", "green", attrs=["bold"]))
            self.analytics \
                .current_session_data[kana_type][kana]['Times Correct'] \
                += 1
        else:
            print(
                colored("\u2716 Incorrect!", "red", attrs=["bold"]),
                "The correct answer is ",
                colored(f"{romaji}", "red", attrs=["bold"]) + ".",
            )
        self.analytics.session_score["total"] += 1

    def finish_practice(self) -> None:
        """Finish the session."""
        self.analytics.print_final_scores()
        self.analytics.save_analytics_data()


if __name__ == "__main__":
    practice = KanaPractice()
    practice.ask_for_choice()
    practice.start_practice()
