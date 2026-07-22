#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oracle.py — 実行（execution）オラクル。

text-to-SQL は、同じ意味の SQL が何通りも書ける（書き方は自由）。だから文字列一致では測れない。
候補の SQL を実際に小さな DB で実行し、お手本(reference)の SQL の実行結果と一致するかで判定する。
＝結果が同じなら正解（書式の違いは問わない）。DB は固定なので再現可能。

使い方:
  python oracle.py                  # reference.py（正例）を採点
  python oracle.py --candidate NAME # corpus/NAME.py を採点
  python oracle.py --selftest       # オラクル自身を検証（正例→PASS / 既知バグ→FAIL）
終了コード: PASS（または selftest 期待どおり）で 0、それ以外 1。
"""
import argparse
import importlib.util
import sqlite3
import sys
from pathlib import Path

# Windows コンソール(cp932)でも日本語・記号を出せるよう出力を UTF-8 に統一。
# Linux/Mac は元から UTF-8 なので無害。これが無いと Windows で print が落ちる。
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EVAL = Path(__file__).resolve().parent
CORPUS = EVAL / "corpus"

# 小さなデータベース（社員テーブル）と、お題（日本語の質問）。これがエージェントの“世界”。
SCHEMA = "CREATE TABLE employees (id INTEGER, name TEXT, dept TEXT, salary INTEGER);"
SEED = [
    (1, "佐藤", "営業", 500000),
    (2, "鈴木", "営業", 420000),
    (3, "高橋", "開発", 600000),
    (4, "田中", "開発", 550000),
    (5, "渡辺", "総務", 380000),
]
TASKS = {
    "q1": "社員は全部で何人いるか",
    "q2": "営業部の人の名前を全部",
    "q3": "部署ごとの平均給与",
    "q4": "いちばん給与が高い人の名前",
    "q5": "給与が50万円以上の人数",
}


def load(path):
    spec = importlib.util.spec_from_file_location("cand_" + path.stem, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if not hasattr(m, "QUERIES"):
        raise AttributeError(f"{path.name} に QUERIES（質問ID→SQL の辞書）が無い")
    return m.QUERIES


def run(query):
    """SQL を小さな DB で実行し、結果を“順序を無視した集合”で返す。動かなければ例外。"""
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(SCHEMA)
        con.executemany("INSERT INTO employees VALUES (?,?,?,?)", SEED)
        rows = con.execute(query).fetchall()
    finally:
        con.close()  # 実行エラー時も必ず接続を閉じる
    return sorted(str(r) for r in rows)  # 行の順番や書き方が違っても結果が同じなら一致とみなす


def evaluate(candidate):
    ref = load(CORPUS / "reference.py")
    for qid, question in TASKS.items():
        want = run(ref[qid])
        if qid not in candidate:
            return ("FAIL", f"{qid}『{question}』: SQL が無い")
        try:
            got = run(candidate[qid])
        except Exception as e:
            return ("FAIL", f"{qid}『{question}』: SQL が実行できない（{type(e).__name__}: {e}）")
        if got != want:
            return ("FAIL", f"{qid}『{question}』: 実行結果がお手本と違う（got={got} / want={want}）")
    return ("PASS", f"全{len(TASKS)}問、実行結果がお手本と一致")


def grade(path):
    try:
        cand = load(path)
    except Exception as e:
        return ("FAIL", f"読込失敗: {e}")
    try:
        return evaluate(cand)
    except Exception as e:
        return ("FAIL", f"実行エラー: {type(e).__name__}: {e}")


def table(rows, title):
    print(f"\n### {title}")
    print("| 対象 | 判定 | 詳細 |")
    print("|---|---|---|")
    for n, v, d in rows:
        print(f"| {n} | {v} | {d} |")


def selftest():
    print("# オラクル自己検証 — text-to-SQL（実行オラクル）")
    rv, rd = grade(CORPUS / "reference.py")
    table([("reference", rv, rd)], "① 正しい SQL 集 reference（PASS であるべき）")
    controls = [
        ("broken_wrongdept.py", "部署を取り違える → 結果が違う"),
        ("broken_nofilter.py", "WHERE を忘れる → 結果が違う"),
        ("broken_syntax.py", "SQL が壊れている → 実行エラー"),
    ]
    brows, caught = [], True
    for f, why in controls:
        v, d = grade(CORPUS / f)
        ok = (v == "FAIL")
        caught = caught and ok
        brows.append((f, v, ("検出OK " if ok else "検出NG ") + d))
    table(brows, "② 壊れた実装（FAIL であるべき）")
    valid = (rv == "PASS") and caught
    print(f"\n## オラクル判定: {'PASS（バグを捕まえ正例を通す＝信頼できる）' if valid else 'FAIL（オラクル自体に欠陥）'}")
    return valid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", default="reference")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    v, d = grade(CORPUS / f"{a.candidate}.py")
    table([(f"{a.candidate}.py", v, d)], "採点（実行オラクル）")
    sys.exit(0 if v == "PASS" else 1)


if __name__ == "__main__":
    main()
