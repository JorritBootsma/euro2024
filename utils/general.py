import pandas as pd


def get_match_cols(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if "-" in col]


def get_question_cols(df: pd.DataFrame) -> list[str]:
    questions_with_extra = [col for col in df.columns if " " in col]

    unnamed_cols = [col for col in df.columns if "Unnamed" in col]
    wrong_cols = ["Stand oud"]

    questions = [col for col in questions_with_extra if col not in unnamed_cols and col not in wrong_cols]
    return questions
