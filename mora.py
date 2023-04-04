#!/usr/bin/env python
"""Practice Kana."""
import random
import sys
from typing import Dict
from typing import Tuple

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


class KanaPractice:
    """Practice Kana."""

    def __init__(self) -> None:
        """Initialize."""
        self.session_score = {"correct": 0, "total": 0}
        self.kana_to_romaji_score = {"correct": 0, "total": 0}
        self.romaji_to_kana_score = {"correct": 0, "total": 0}
        self.choices = ["Hiragana", "Katakana"]
        self.selected_choice = None

    def ask_for_choice(self) -> None:
        """Ask the user for a choice."""
        try:
            while self.selected_choice not in self.choices:
                user_input = input(
                    "Which one do you want to practice "
                    f"({', '.join(self.choices)})? "
                ).lower()
                matched_choices = [
                    c for c in self.choices if
                    c.lower().startswith(user_input)
                ]
                if len(matched_choices) == 1:
                    self.selected_choice = matched_choices[0]
                elif len(matched_choices) > 1:
                    print(
                        "Multiple matches found:"
                        f" {', '.join(matched_choices)}"
                    )
                else:
                    print("No matches found.")
        except KeyboardInterrupt:
            print("\nSession aborted.")
            sys.exit()

    def start_practice(self) -> None:
        """Start the session."""
        try:
            while True:
                kana_char, romaji = self.get_random_kana()
                prompt = random.choice([0, 1])  # randomly choose prompt type
                if prompt == 0:  # Kana to Romaji
                    user_input = input(
                        f"What is the romaji representation of {self.selected_choice} {kana_char}: "
                    )
                    if user_input.lower() == romaji.lower():
                        print("Correct!")
                        self.session_score["correct"] += 1
                        self.kana_to_romaji_score["correct"] += 1
                    else:
                        print(f"Incorrect! The correct answer is {romaji}.")
                    self.session_score["total"] += 1
                    self.kana_to_romaji_score["total"] += 1
                else:  # Romaji to Kana
                    user_input = input(
                        f"What is the {self.selected_choice} representation of {romaji}: "
                    )
                    if user_input.lower() == kana_char.lower():
                        print("Correct!")
                        self.session_score["correct"] += 1
                        self.romaji_to_kana_score["correct"] += 1
                    else:
                        print(f"Incorrect! The correct answer is {kana_char}.")
                    self.session_score["total"] += 1
                    self.romaji_to_kana_score["total"] += 1

                # Handle division by zero error
                if self.session_score["total"] == 0:
                    accuracy = 0
                else:
                    accuracy = (
                        self.session_score["correct"] /
                        self.session_score["total"]
                    ) * 100

                if self.kana_to_romaji_score["total"] == 0:
                    kana_to_romaji_accuracy = 0
                else:
                    kana_to_romaji_accuracy = (
                        self.kana_to_romaji_score["correct"]
                        / self.kana_to_romaji_score["total"]
                    ) * 100

                if self.romaji_to_kana_score["total"] == 0:
                    romaji_to_kana_accuracy = 0
                else:
                    romaji_to_kana_accuracy = (
                        self.romaji_to_kana_score["correct"]
                        / self.romaji_to_kana_score["total"]
                    ) * 100

                print(
                    "Session score: "
                    f"{self.session_score['correct']}/"
                    f"{self.session_score['total']} ({accuracy:.2f}%)\n"
                    f"{self.selected_choice} to Romaji score: "
                    f"{self.kana_to_romaji_score['correct']}/"
                    f"{self.kana_to_romaji_score['total']} "
                    f"({kana_to_romaji_accuracy:.2f}%)\n"
                    f"Romaji to {self.selected_choice} score: "
                    f"{self.romaji_to_kana_score['correct']}/"
                    f"{self.romaji_to_kana_score['total']} "
                    f"({romaji_to_kana_accuracy:.2f}%)\n"
                )

        except KeyboardInterrupt:
            print("\nSession aborted. Final score:")

            # Handle division by zero error
            if self.session_score["total"] == 0:
                accuracy = 0
            else:
                accuracy = (
                    self.session_score["correct"] / self.session_score["total"]
                )

            if self.kana_to_romaji_score["total"] == 0:
                kana_to_romaji_accuracy = 0
            else:
                kana_to_romaji_accuracy = (
                    self.kana_to_romaji_score["correct"]
                    / self.kana_to_romaji_score["total"]
                ) * 100

            if self.romaji_to_kana_score["total"] == 0:
                romaji_to_kana_accuracy = 0
            else:
                romaji_to_kana_accuracy = (
                    self.romaji_to_kana_score["correct"]
                    / self.romaji_to_kana_score["total"]
                ) * 100

            print(
                "Session score: "
                f"{self.session_score['correct']}/"
                f"{self.session_score['total']} ({accuracy:.2f}%)\n"
                f"{self.selected_choice} to Romaji score: "
                f"{self.kana_to_romaji_score['correct']}/"
                f"{self.kana_to_romaji_score['total']} "
                f"({kana_to_romaji_accuracy:.2f}%)\n"
                f"Romaji to {self.selected_choice} score: "
                f"{self.romaji_to_kana_score['correct']}/"
                f"{self.romaji_to_kana_score['total']} "
                f"({romaji_to_kana_accuracy:.2f}%)\n"
            )

    def get_random_kana(self) -> Tuple[str, str]:
        """Get a randomized kana."""
        assert self.selected_choice is not None
        kana_dict = KANA_TO_ROMAJI[self.selected_choice]
        kana_char = random.choice(list(kana_dict.keys()))
        romaji = kana_dict[kana_char]
        return kana_char, romaji


if __name__ == "__main__":
    practice = KanaPractice()
    practice.ask_for_choice()
    practice.start_practice()
