#!/usr/bin/env python
"""Practice Kana."""
import random
import sys
from typing import Dict
from typing import Tuple

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

    def get_random_kana(self) -> Tuple[str, str]:
        """Get a randomized kana."""
        assert self.selected_choice is not None
        kana_dict = KANA_TO_ROMAJI[self.selected_choice]
        kana_char = random.choice(list(kana_dict.keys()))
        romaji = kana_dict[kana_char]
        return kana_char, romaji

    def start_practice(self) -> None:
        """Start the session."""
        try:
            while True:
                kana_char, romaji = self.get_random_kana()
                #  prompt = random.choice([0, 1])
                prompt = 0
                if prompt == 0:
                    self.prompt_kana_to_romaji(kana_char, romaji)
                else:
                    self.prompt_romaji_to_kana(kana_char, romaji)

                self.print_session_scores()

        except KeyboardInterrupt:
            self.print_final_scores()

    def prompt_kana_to_romaji(self, kana_char: str, romaji: str) -> None:
        """Prompt the user for kana to romaji translation."""
        user_input = input(
            f"What is the romaji representation of {self.selected_choice} " +
            colored(f"{kana_char}", "yellow", attrs=["bold"]) + ": "
        )
        if user_input.lower() == romaji.lower():
            print(
                colored("\u2714 Correct!", "green", attrs=["bold"])
            )
            self.session_score["correct"] += 1
            self.kana_to_romaji_score["correct"] += 1
        else:
            print(
                colored("\u2716 Incorrect!", "red", attrs=["bold"]),
                "The correct answer is ",
                colored(f"{romaji}", "red", attrs=["bold"]) + "."
            )
        self.session_score["total"] += 1
        self.kana_to_romaji_score["total"] += 1

    def prompt_romaji_to_kana(self, kana_char: str, romaji: str) -> None:
        """Prompt the user for romaji to kana translation."""
        user_input = input(
            f"What is the {self.selected_choice} representation of " +
            colored(f"{romaji}", "yellow", attrs=["bold"]) + ": "
        )
        if user_input.lower() == kana_char.lower():
            print(
                colored("\u2714 Correct!", "green", attrs=["bold"])
            )
            self.session_score["correct"] += 1
            self.romaji_to_kana_score["correct"] += 1
        else:
            print(
                colored("\u2716 Incorrect!", "red", attrs=["bold"]),
                "The correct answer is ",
                colored(f"{kana_char}", "red", attrs=["bold"]) + "."
            )
        self.session_score["total"] += 1
        self.romaji_to_kana_score["total"] += 1

    def print_session_scores(self) -> None:
        """Print the session scores."""
        print(
            "Session score:",
            colored(
                f"{self.session_score['correct']}/"
                f"{self.session_score['total']}",
                "blue",
                attrs=["bold"]
            )
        )

    def print_final_scores(self) -> None:
        """Print the final scores."""
        print(
            colored(
                f"\nFinal score: {self.session_score['correct']}/"
                f"{self.session_score['total']}",
                "blue",
                attrs=["bold"],
            )
        )
        print(
            colored(
                "Kana to romaji score:"
                f" {self.kana_to_romaji_score['correct']}/"
                f"{self.kana_to_romaji_score['total']}",
                "blue",
                attrs=["bold"],
            )
        )
        print(
            colored(
                f"Romaji to kana score:"
                f" {self.romaji_to_kana_score['correct']}/"
                f"{self.romaji_to_kana_score['total']}",
                "blue",
                attrs=["bold"],
            )
        )


if __name__ == "__main__":
    practice = KanaPractice()
    practice.ask_for_choice()
    practice.start_practice()
