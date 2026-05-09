"""事業承継M&AEX対策 デモアプリ（全3問）。"""

import random
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
import history_manager

QUESTIONS = [
    {
        "number": 1,
        "question": "M&Aにおいて、買収対象企業の財務・法務・事業などを詳細に調査するプロセスを何というか？",
        "choices": {
            "A": "デューデリジェンス（DD）",
            "B": "バリュエーション",
            "C": "PMI（ポスト・マージャー・インテグレーション）",
            "D": "ティーザー",
            "E": "LOI（基本合意書）",
            "F": "わからない",
        },
        "answer": "A",
        "chapter": 1,
        "chapter_title": "第1章：M&A基礎知識",
        "section": "M&A用語",
    },
    {
        "number": 2,
        "question": "株式譲渡によるM&Aの特徴として、最も適切なものはどれか？",
        "choices": {
            "A": "売り手企業の許認可・既存契約が原則としてそのまま引き継がれる",
            "B": "売り手企業の簿外債務は買い手に引き継がれない",
            "C": "従業員との雇用契約は買収後に個別に締結し直す必要がある",
            "D": "株主である売り手個人には法人税のみが課税される",
            "E": "買い手は対象会社の事業資産のみを選択的に取得できる",
            "F": "わからない",
        },
        "answer": "A",
        "chapter": 1,
        "chapter_title": "第1章：M&A基礎知識",
        "section": "M&Aスキーム",
    },
    {
        "number": 3,
        "question": "事業承継における「経営者保証」の説明として、最も適切なものはどれか？",
        "choices": {
            "A": "金融機関が経営者個人に求める個人保証のことで、事業承継時の障壁になることがある",
            "B": "後継者が前経営者の経営手法を継続することを保証する制度である",
            "C": "事業承継後5年間、前経営者が経営に関与することを義務付けた制度である",
            "D": "後継者が金融機関に担保を提供することで代替できる",
            "E": "現在すべての金融機関で経営者保証の提供が義務付けられている",
            "F": "わからない",
        },
        "answer": "A",
        "chapter": 1,
        "chapter_title": "第1章：M&A基礎知識",
        "section": "事業承継の基礎",
    },
]

TOTAL = len(QUESTIONS)


def _get_question(used_numbers=None, allowed_numbers=None, sequential=False, chapter=None):
    pool = QUESTIONS
    if chapter is not None:
        pool = [q for q in pool if q.get("chapter") == chapter]
    if allowed_numbers is not None:
        pool = [q for q in pool if q["number"] in allowed_numbers]
    if used_numbers:
        pool = [q for q in pool if q["number"] not in used_numbers]
    if not pool:
        return None
    return pool[0] if sequential else random.choice(pool)


st.set_page_config(
    page_title="事業承継M&AEX対策【デモ】",
    page_icon="📚",
    layout="centered",
)


def init_state():
    defaults = {
        "quiz_started": False,
        "quiz_finished": False,
        "score": 0,
        "current_question_num": 0,
        "current_quiz": None,
        "used_numbers": [],
        "answered": False,
        "user_answer": None,
        "num_questions": TOTAL,
        "mode": "normal",
        "sequential": False,
        "allowed_numbers": None,
        "chapter": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def _build_allowed(mode):
    if mode == "wrong_only":
        allowed = history_manager.get_wrong_numbers()
        if not allowed:
            raise ValueError("間違えた問題の記録がありません。通常モードで解いてから試してください。")
        return allowed
    if mode == "unanswered":
        answered = set(history_manager.get_answered_numbers())
        unanswered = sorted({q["number"] for q in QUESTIONS} - answered)
        if not unanswered:
            raise ValueError("未回答の問題がありません。")
        return unanswered
    return None


def start_quiz(num_questions, mode, sequential, chapter=None):
    allowed = _build_allowed(mode)
    st.session_state.update({
        "num_questions": num_questions,
        "mode": mode,
        "sequential": sequential,
        "allowed_numbers": allowed,
        "chapter": chapter,
        "quiz_started": True,
        "quiz_finished": False,
        "score": 0,
        "current_question_num": 1,
        "used_numbers": [],
        "answered": False,
        "user_answer": None,
    })
    st.session_state.current_quiz = _get_question(
        allowed_numbers=allowed,
        sequential=sequential,
        chapter=chapter,
    )


def answer_mc(user_answer):
    st.session_state.user_answer = user_answer
    st.session_state.answered = True
    correct = (user_answer == st.session_state.current_quiz["answer"])
    if correct:
        st.session_state.score += 1
    history_manager.record_answer(st.session_state.current_quiz["number"], correct)


def go_next():
    st.session_state.used_numbers.append(st.session_state.current_quiz["number"])
    st.session_state.current_question_num += 1
    st.session_state.answered = False
    st.session_state.user_answer = None
    st.session_state.current_quiz = _get_question(
        used_numbers=st.session_state.used_numbers,
        allowed_numbers=st.session_state.allowed_numbers,
        sequential=st.session_state.sequential,
        chapter=st.session_state.chapter,
    )


# ──────────────────────────────────────────
# 画面①：設定
# ──────────────────────────────────────────
def show_settings():
    st.title("📚 事業承継M&AEX 対策ツール")
    st.divider()

    wrong_count = len(history_manager.get_wrong_numbers())
    answered_count = len(history_manager.get_answered_numbers())
    st.caption(
        f"📄 全5章　（全 {TOTAL} 問 ／ "
        f"解答済 {answered_count} 問 ／ 誤答 {wrong_count} 問）"
    )
    st.divider()

    # 章選択（全5章表示、デモ問題は第1章のみ）
    ALL_CHAPTERS = [
        (1, "第1章：事業承継関連税制等"),
        (2, "第2章：事業承継関連法制等"),
        (3, "第3章：M&A基礎知識・関連会計"),
        (4, "第4章：M&A関連法制等"),
        (5, "第5章：事業承継・M&Aコンサルティング（総合問題）"),
    ]
    q_counts = {}
    for q in QUESTIONS:
        ch = q.get("chapter")
        q_counts[ch] = q_counts.get(ch, 0) + 1
    chapter_options = {"全章（ランダム出題）": None}
    for num, title in ALL_CHAPTERS:
        count = q_counts.get(num, 0)
        chapter_options[f"{title}（{count}問）"] = num
    selected_label = st.selectbox("出題範囲", list(chapter_options.keys()))
    selected_chapter = chapter_options[selected_label]

    # 出題モード
    mode_options = {
        "通常（ランダム）": "normal",
        "間違えた問題のみ": "wrong_only",
        "未回答のみ": "unanswered",
    }
    selected_mode_label = st.selectbox("出題モード", list(mode_options.keys()))
    selected_mode = mode_options[selected_mode_label]

    # 出題順序
    order_options = {"ランダム": False, "番号順": True}
    selected_order_label = st.radio(
        "出題順序", list(order_options.keys()), horizontal=True
    )
    selected_sequential = order_options[selected_order_label]

    # 問題数
    num_questions = st.number_input(
        "問題数", min_value=1, max_value=TOTAL, value=TOTAL, step=1
    )

    st.divider()

    if st.button("スタート ▶", type="primary", use_container_width=True):
        if selected_chapter is not None and q_counts.get(selected_chapter, 0) == 0:
            st.error("デモ版では第1章のみ問題があります。本格版（全600問）はメールでご連絡ください。")
        else:
            try:
                start_quiz(int(num_questions), selected_mode, selected_sequential, selected_chapter)
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    st.divider()
    st.info(
        "💡 **これはデモ版です（全3問）**\n\n"
        "本格版（全600問・全5章）のご利用をご希望の方は、\n"
        "メールアドレスをお知らせください。個別にご招待します。\n\n"
        "📧 kawakanpasakeyu@gmail.com"
    )


# ──────────────────────────────────────────
# 画面②：問題
# ──────────────────────────────────────────
def show_question():
    quiz = st.session_state.current_quiz
    num = st.session_state.current_question_num
    total = st.session_state.num_questions

    st.progress(num / total)
    col_l, col_r = st.columns([3, 1])
    with col_l:
        chapter_title = quiz.get("chapter_title", "")
        section = quiz.get("section", "")
        header = f"**問題 {num} / {total}**"
        if chapter_title:
            header += f"　{chapter_title}"
        if section:
            header += f"　【{section}】"
        st.markdown(header)
    with col_r:
        st.markdown(f"スコア: **{st.session_state.score}** / {num - 1}")

    stats = history_manager.get_question_stats(quiz["number"])
    if stats and stats.get("last_attempt"):
        st.caption(
            f"Q{quiz['number']} ／ 前回: {stats['last_attempt']} ／ "
            f"誤答回数: {stats.get('wrong_count', 0)}"
        )

    choices = quiz["choices"]
    choice_keys = sorted(choices.keys())
    choice_lines = "\n\n".join(f"{k}．{choices[k]}" for k in choice_keys)
    st.markdown(f"**Q{quiz['number']}．{quiz['question']}**\n\n{choice_lines}")
    st.divider()

    if not st.session_state.answered:
        for i in range(0, len(choice_keys), 3):
            row = choice_keys[i:i + 3]
            cols = st.columns(len(row))
            for col, key in zip(cols, row):
                with col:
                    if st.button(key, use_container_width=True, key=f"choice_{key}"):
                        answer_mc(key)
                        st.rerun()
    else:
        user_ans = st.session_state.user_answer
        correct = quiz["answer"]
        for key in choice_keys:
            label = choices[key]
            if key == correct and key == user_ans:
                st.success(f"✅ {key}．{label}　← 正解！あなたの回答")
            elif key == correct:
                st.success(f"✅ {key}．{label}　← 正解")
            elif key == user_ans:
                st.error(f"❌ {key}．{label}　← あなたの回答")
            else:
                st.write(f"　　{key}．{label}")

        st.divider()
        if num >= total:
            if st.button("結果を見る →", type="primary", use_container_width=True):
                st.session_state.quiz_finished = True
                st.rerun()
        else:
            if st.button("次の問題へ →", type="primary", use_container_width=True):
                go_next()
                st.rerun()

    with st.sidebar:
        if st.button("← 設定に戻る"):
            reset()
            st.rerun()


# ──────────────────────────────────────────
# 画面③：結果
# ──────────────────────────────────────────
def show_results():
    score = st.session_state.score
    total = st.session_state.num_questions
    pct = score / total * 100

    st.title("📊 結果")
    st.markdown(f"## {total} 問中　**{score} 問** 正解")
    st.progress(score / total)

    if pct >= 80:
        st.success(f"🎉 素晴らしい！　正解率 {pct:.0f}%")
    elif pct >= 60:
        st.warning(f"👍 もう少し！　正解率 {pct:.0f}%")
    else:
        st.error(f"📖 復習が必要です。　正解率 {pct:.0f}%")

    wrong_total = len(history_manager.get_wrong_numbers())
    answered_total = len(history_manager.get_answered_numbers())
    st.info(f"累計：解答済 {answered_total} 問 ／ 誤答問題 {wrong_total} 問")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("もう一度", use_container_width=True):
            mode = st.session_state.mode
            sequential = st.session_state.sequential
            nq = st.session_state.num_questions
            reset()
            init_state()
            try:
                start_quiz(nq, mode, sequential)
            except ValueError as e:
                st.error(str(e))
            st.rerun()
    with col2:
        if st.button("設定に戻る", type="primary", use_container_width=True):
            reset()
            st.rerun()

    st.divider()
    st.info(
        "💡 **これはデモ版です（全3問）**\n\n"
        "本格版（全600問・全5章）のご利用をご希望の方は、\n"
        "メールアドレスをお知らせください。個別にご招待します。\n\n"
        "📧 kawakanpasakeyu@gmail.com"
    )


# ──────────────────────────────────────────
# メイン
# ──────────────────────────────────────────
def main():
    init_state()
    if st.session_state.quiz_finished:
        show_results()
    elif st.session_state.quiz_started:
        show_question()
    else:
        show_settings()


if __name__ == "__main__":
    main()
