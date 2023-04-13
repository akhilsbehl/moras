"""Library of functions to implement interfaces to practice Kana."""
import copy
import csv
import datetime
import os
import random
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

CHOICES = list(KANA_TO_ROMAJI.keys())
TEMPLATE_DATA_STORE = "analytics-template.csv"

KTYPE_DICT_TEMPLATE = {k: {} for k in KANA_TO_ROMAJI.keys()}


class Analytics(object):
    """Analytics for the practice sessions."""

    def __init__(self, file_name: str = "analytics.csv"):
        """Initialize."""
        self.file_name = file_name
        self.past_data = self.load_past_data()
        self.this_session_data = copy.deepcopy(KTYPE_DICT_TEMPLATE)

    def load_past_data(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Load the analytics data."""
        past_data = copy.deepcopy(KTYPE_DICT_TEMPLATE)

        if not os.path.exists(self.file_name):
            self.create_data_store()

        with open(TEMPLATE_DATA_STORE, "r") as temp:
            reader = csv.reader(temp)
            next(reader)
            rows = [r for r in reader]

        with open(self.file_name, "r") as file:
            reader = csv.reader(file)
            next(reader)
            rows += [r for r in reader]

        for row in rows:
            _, ktype, kana, seen, correct, _ = row
            if kana not in past_data[ktype]:
                past_data[ktype][kana] = {
                    "seen": int(seen),
                    "correct": int(correct),
                }
            else:
                past_data[ktype][kana]["seen"] += int(seen)
                past_data[ktype][kana]["correct"] += int(correct)

        for ktype in KTYPE_DICT_TEMPLATE.keys():
            for kana, data in past_data[ktype].items():
                seen = data["seen"]
                correct = data["correct"]
                accuracy = correct / seen if seen != 0 else 0
                data["accuracy"] = accuracy

        return past_data

    def create_data_store(self) -> None:
        """Create a new file for analytics the first time."""
        with open(TEMPLATE_DATA_STORE, "r", newline="") as temp:
            colnames = temp.readline().strip().split(",")
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(colnames)

    def calculate_accuracies(self) -> Dict[str, Dict[str, float]]:
        """Calculate accuracies at Kana level."""
        accuracies = copy.deepcopy(KTYPE_DICT_TEMPLATE)
        for ktype in KTYPE_DICT_TEMPLATE.keys():
            for kana in self.past_data[ktype]:
                seen = self.past_data[ktype][kana]["seen"]
                correct = self.past_data[ktype][kana]["correct"]
                accuracy = (correct / seen) if seen > 0 else 0
                accuracies[ktype][kana] = accuracy
        return accuracies

    def calculate_seen_and_acc_ranges(self, ktype: str) -> Tuple:
        """Calculate the ranges for relative calculations."""
        accuracies = self.calculate_accuracies()
        kana_data = [
            {
                "kana": kana,
                "seen": self.past_data[ktype][kana]["seen"],
                "accuracy": accuracy,
            }
            for kana, accuracy in accuracies[ktype].items()
        ]

        min_seen = min(data["seen"] for data in kana_data)
        max_seen = max(data["seen"] for data in kana_data)
        min_acc = min(data["accuracy"] for data in kana_data)
        max_acc = max(data["accuracy"] for data in kana_data)

        if max_seen == min_seen:
            range_seen = 1
        else:
            range_seen = max_seen - min_seen

        if max_acc == min_acc:
            range_acc = 1
        else:
            range_acc = max_acc - min_acc

        return (kana_data, min_seen, range_seen, min_acc, range_acc)

    def adjust_rates(self, seen_relative, accuracy_relative) -> float:
        """Adjust sampling rates per seen and accuracy."""
        if seen_relative < 0.5:
            rate = 2 ** (1 - seen_relative * 2)
        else:
            if accuracy_relative < 0.5:
                rate = 1 + (1 - accuracy_relative * 2)
            else:
                rate = 1 - (accuracy_relative - 0.5) * 2
        return rate

    def calculate_sampling_rates(self) -> Dict[str, Dict[str, float]]:
        """Calculate sampling rates based on seen frequency and accuracy."""
        sampling_rates = copy.deepcopy(KTYPE_DICT_TEMPLATE)

        for ktype in KTYPE_DICT_TEMPLATE.keys():
            adjusted_rates = {}
            (
                kana_data,
                min_seen,
                range_seen,
                min_acc,
                range_acc,
            ) = self.calculate_seen_and_acc_ranges(ktype)

            for data in kana_data:
                seen_relative = (data["seen"] - min_seen) / range_seen
                accuracy_relative = (data["accuracy"] - min_acc) / range_acc
                adjusted_rates[data["kana"]] = self.adjust_rates(
                    seen_relative,
                    accuracy_relative,
                )

            total_adjusted_rate = sum(adjusted_rates.values())
            normalized_sampling_rate = {
                kana: rate / total_adjusted_rate
                for kana, rate in adjusted_rates.items()
            }

            sampling_rates[ktype] = normalized_sampling_rate
        return sampling_rates

    def update_analytics_data(
        self,
        ktype: str,
        kana: str,
        correct: bool,
    ) -> None:
        """Update the analytics data for the current session."""
        if kana not in self.this_session_data[ktype]:
            self.this_session_data[ktype][kana] = {"seen": 0, "correct": 0}
        self.this_session_data[ktype][kana]["seen"] += 1
        if correct:
            self.this_session_data[ktype][kana]["correct"] += 1

    def calculate_score(self, session: Dict, ktype: str) -> Dict[str, int]:
        """Calculate score for historical or this session."""
        seen, correct = 0, 0
        for kana in session[ktype]:
            seen += session[ktype][kana]["seen"]
            correct += session[ktype][kana]["correct"]
        return {"seen": seen, "correct": correct}

    def combine_scores(self, ktype) -> Dict[str, int]:
        """Combine the past and current scores."""
        this = self.calculate_score(self.this_session_data, ktype)
        past = self.calculate_score(self.past_data, ktype)
        session_score = {k: this[k] + past[k] for k in this.keys()}
        return session_score

    def get_score(self, for_session: str, ktype: str) -> Tuple:
        """Print the score for historical or this session."""
        assert for_session in ("This", "Past", "Total")

        if for_session == "This":
            score = self.calculate_score(self.this_session_data, ktype)
            label = "This session's"
        elif for_session == "Past":
            score = self.calculate_score(self.past_data, ktype)
            label = "Past sessions'"
        else:
            score = self.combine_scores(ktype)
            label = "Overall"

        if score["seen"] != 0:
            percentage = score["correct"] / score["seen"] * 100
        else:
            percentage = 0

        print(
            f"{label} score:",
            colored(
                f"{score['correct']}/{score['seen']} " f"({percentage:.2f}%)",
                "blue",
                attrs=["bold"],
            ),
        )

        return score["seen"], score["correct"], percentage

    def save_analytics_data(self) -> None:
        """Save the analytics data to the file."""
        today = datetime.date.today().strftime("%Y-%m-%d")

        with open(self.file_name, "a") as file:
            writer = csv.writer(file)
            for ktype, data in self.this_session_data.items():
                for kana, stats in data.items():
                    seen = stats["seen"]
                    correct = stats["correct"]
                    accuracy = correct / seen if seen != 0 else 0
                    row = [
                        today,
                        ktype,
                        kana,
                        seen,
                        correct,
                        f"{accuracy:.2f}",
                    ]
                    writer.writerow(row)
        return None


ANALYTICS = Analytics()
SAMPLING_RATES = {
    k: (list(v.keys()), list(v.values()))
    for k, v in ANALYTICS.calculate_sampling_rates().items()
}


def get_random_kana_romaji_pair(ktype: str) -> Tuple[str, str]:
    """Get a randomized kana."""
    kanas, rates = SAMPLING_RATES[ktype]
    kana = random.choices(kanas, weights=rates, k=1)[0]
    romaji = KANA_TO_ROMAJI[ktype][kana]
    return kana, romaji


def validate_input_against_answer(input_: str, answer: str) -> bool:
    """Validate the known romaji answer against input answer."""
    correct, msg = True, colored("\u2714 Correct!", "green", attrs=["bold"])
    if input_.lower() != answer.lower():
        correct = False
        msg = " ".join(
            [
                colored("\u2716 Incorrect!", "red", attrs=["bold"]),
                "The correct answer is",
                colored(f"{answer}", "red", attrs=["bold"]) + ".",
            ]
        )
    print(msg)
    return correct


def get_final_scores(ktype) -> Dict[str, Dict]:
    """Prepare all the scores for the final analysis."""
    sessions = ("Past", "This", "Total")
    results = {}
    for session in sessions:
        _ = ANALYTICS.get_score(session, ktype)
        results[session] = {
            "session": session,
            "kana_seen": _[0],
            "kana_answered_correctly": _[1],
            "accuracy": f"{_[2]:.1f}",
        }
    return results
