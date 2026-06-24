# CLAUDE.md — text-to-sql-agent

このリポジトリは「日本語の質問 → SQL」に変えるエージェントと、その採点係（実行オラクル）です。
出力する SQL は書き方が一通りに決まらないため、**実際に小さな DB で実行し、結果がお手本と一致するか**で正しさを判定します。

## 確認のしかた

- `python eval/oracle.py --selftest` … 採点係が正しいか（お手本=PASS／わざと壊した例=FAIL）
- `python eval/oracle.py --candidate candidate` … エージェントの答え（`eval/corpus/candidate.py`）を採点
- `python eval/oracle.py` … お手本(reference)を採点

## いじるときの約束（評価駆動 / EDD）

- 先に eval（合否の基準）を満たすことを確認してから「完成」とする。雰囲気で done にしない。
- `eval/corpus/reference.py`（お手本）と `broken_*.py`（わざと壊した例）は採点係の検証用。むやみに変えない。
- 標準ライブラリのみ（sqlite3 は標準）。秘密情報・個人情報・客先コードを入れない。

## ファイルの役割

- `.claude/agents/text-to-sql-agent.md` … エージェントの定義（お題。Claude Code が認識・起動する）
- `eval/oracle.py` … 採点係（オラクル本体）
- `design/design.md` … なぜこの作りにしたか
- `README.md` … 全体の説明（図つき）
