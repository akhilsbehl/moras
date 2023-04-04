#!/usr/bin/env python

"""Practice Kana."""
import random
from typing import Dict
from typing import Tuple


class KanaPractice:
    """Practice Kana."""

    def __init__(self) -> None:
        """Initialize."""
        self.session_score = {"correct": 0, "total": 0}
        self.choices = ["Hiragana", "Katakana"]
        self.selected_choice = None
        self.kana_dict: Dict[str, Dict[str, str]] = {
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

    def ask_for_choice(self) -> None:
        """Ask the user for a choice."""
        while self.selected_choice not in self.choices:
            self.selected_choice = input(
                "Which one do you want to practice "
                f"({', '.join(self.choices)})? "
            )

    def start_practice(self) -> None:
        """Start the session."""
        try:
            while True:
                kana_char, romanji = self.get_random_kana()
                user_input = input(
                    "Enter the romaji representation"
                    f" of {kana_char}: "
                )
                if user_input.lower() == romanji.lower():
                    print("Correct!")
                    self.session_score["correct"] += 1
                else:
                    print(f"Incorrect! The correct answer is {romanji}.")
                self.session_score["total"] += 1
                accuracy = (
                    self.session_score["correct"] / self.session_score["total"]
                ) * 100
                print(
                    "Session score: "
                    f"{self.session_score['correct']}/"
                    f"{self.session_score['total']} ({accuracy:.2f}%)\n"
                )
        except KeyboardInterrupt:
            print("\nSession aborted. Final score:")
            accuracy = (
                self.session_score["correct"] / self.session_score["total"]
            ) * 100
            print(
                f"{self.session_score['correct']}/"
                f"{self.session_score['total']} ({accuracy:.2f}%)"
            )

    def get_random_kana(self) -> Tuple[str, str]:
        """Get a randomized kana."""
        assert self.selected_choice is not None
        kana_dict = self.kana_dict[self.selected_choice]
        kana_char = random.choice(list(kana_dict.keys()))
        romanji = kana_dict[kana_char]
        return kana_char, romanji


if __name__ == "__main__":
    practice = KanaPractice()
    practice.ask_for_choice()
    practice.start_practice()
