"""事業承継M&AEX対策 デモアプリ（全5章・各2問、合計10問）。"""

import random
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
import history_manager

QUESTIONS = [
    # ── 第1章：事業承継関連税制等 ──
    {
        "number": 1,
        "question": "M&Aの事実を従業員へ知らせる時期として、ガイドラインが原則としているのは。",
        "choices": {
            "a": "基本合意締結の直後",
            "b": "買収監査（DD）が開始される前",
            "c": "可能な限りクロージング後（早くとも最終契約締結後）",
            "d": "譲渡希望条件の整理（案件化）が完了した時点",
            "e": "仲介機関との提携仲介契約を締結した時点",
            "f": "わからない",
        },
        "answer": "c",
        "chapter": 1,
        "chapter_title": "第1章：事業承継関連税制等",
        "section": "事業承継ガイドライン・M&Aの基本",
        "explanation": "機密保持が重要であり、従業員への開示は原則として可能な限りクロージング後、早くとも最終契約締結後に行う。",
    },
    {
        "number": 2,
        "question": "M&Aの手続き全般において、譲渡企業側が情報漏洩を防ぐために最も厳守すべきことは。",
        "choices": {
            "a": "秘密の厳守",
            "b": "早期の資金回収の確約",
            "c": "従業員への先行開示",
            "d": "高値での譲渡交渉",
            "e": "競合他社への積極的な情報開示",
            "f": "わからない",
        },
        "answer": "a",
        "chapter": 1,
        "chapter_title": "第1章：事業承継関連税制等",
        "section": "事業承継ガイドライン・M&Aの基本",
        "explanation": "情報漏洩は成約を妨げる最大のリスクであり、秘密の厳守が実務の鉄則である。",
    },
    # ── 第2章：事業承継関連法制等 ──
    {
        "number": 3,
        "question": "特定の株主から自己株式を取得する場合、株主総会のどの決議が必要か。",
        "choices": {
            "a": "普通決議",
            "b": "特別決議",
            "c": "全員の同意",
            "d": "取締役会決議のみ",
            "e": "監査役の承認",
            "f": "わからない",
        },
        "answer": "b",
        "chapter": 2,
        "chapter_title": "第2章：事業承継関連法制等",
        "section": "会社法：自己株式の取得・保有・消却",
        "explanation": "特定の株主から自己株式を取得する場合、他の株主との不平等が生じるため、株主総会の特別決議が必要である（会社法160条1項、309条2項2号）。",
    },
    {
        "number": 4,
        "question": "自己株式を取得できる対価の範囲は。",
        "choices": {
            "a": "分配可能額の範囲内",
            "b": "資本金の額まで",
            "c": "負債総額の2分の1まで",
            "d": "純資産額に制限なし",
            "e": "前期売上高の10％まで",
            "f": "わからない",
        },
        "answer": "a",
        "chapter": 2,
        "chapter_title": "第2章：事業承継関連法制等",
        "section": "会社法：自己株式の取得・保有・消却",
        "explanation": "自己株式の取得対価は、原則として分配可能額の範囲内でなければならない（会社法461条1項2号）。",
    },
    # ── 第3章：M&A基礎知識・関連会計 ──
    {
        "number": 5,
        "question": "M&Aの買収価格を決定する際、最も基礎となる「企業の静的な価値」に着目した評価手法は。",
        "choices": {
            "a": "インカム・アプローチ",
            "b": "マーケット・アプローチ",
            "c": "コスト・アプローチ（時価純資産法など）",
            "d": "類似上場会社法",
            "e": "EBITDAマルチプル法",
            "f": "わからない",
        },
        "answer": "c",
        "chapter": 3,
        "chapter_title": "第3章：M&A基礎知識・関連会計",
        "section": "企業価値評価の手法と基礎",
        "explanation": "コスト・アプローチは、貸借対照表の純資産に着目して価値を測る手法で、企業の静的な価値（清算価値）の把握に適しています。",
    },
    {
        "number": 6,
        "question": "フリー・キャッシュ・フロー（FCF）を現在価値に割り引いて計算する、投資対効果の測定に適した手法は。",
        "choices": {
            "a": "配当還元方式",
            "b": "DCF法（ディスカウント・キャッシュ・フロー法）",
            "c": "年買法",
            "d": "純資産価額方式",
            "e": "類似業種比準方式",
            "f": "わからない",
        },
        "answer": "b",
        "chapter": 3,
        "chapter_title": "第3章：M&A基礎知識・関連会計",
        "section": "企業価値評価の手法と基礎",
        "explanation": "DCF法は、将来のフリー・キャッシュ・フロー（FCF）を現在価値に割り引いて企業価値を算出する、投資対効果の測定に適した手法です。",
    },
    # ── 第4章：M&A関連法制等 ──
    {
        "number": 7,
        "question": "2024年10月の改正により、株式会社の代表取締役が登記簿上の住所を一部非表示にする措置を申し出た場合、表示される範囲はどこまでか。",
        "choices": {
            "a": "都道府県まで",
            "b": "市区町村まで（例：東京都千代田区まで）",
            "c": "番地まで",
            "d": "郵便番号まで",
            "e": "すべて非表示（＊＊＊と表示）",
            "f": "わからない",
        },
        "answer": "b",
        "chapter": 4,
        "chapter_title": "第4章：M&A関連法制等",
        "section": "M&Aの手法・登記・独占禁止法",
        "explanation": "2024年10月施行の商業登記規則改正により、代表取締役等は申出によって登記簿上の住所を市区町村まで表示し、番地以下を非表示にすることができます。",
    },
    {
        "number": 8,
        "question": "登記事項証明書（登記簿謄本）の交付を請求できる者は、法律上どのように定められているか。",
        "choices": {
            "a": "会社の株主に限定される",
            "b": "会社の債権者に限定される",
            "c": "誰でも所定の手数料を納付して請求できる",
            "d": "役員および親族に限定される",
            "e": "弁護士や司法書士などの専門家に限定される",
            "f": "わからない",
        },
        "answer": "c",
        "chapter": 4,
        "chapter_title": "第4章：M&A関連法制等",
        "section": "M&Aの手法・登記・独占禁止法",
        "explanation": "登記事項証明書（登記簿謄本）は、誰でも手数料を納付して法務局に請求することができます（商業登記法11条の2）。",
    },
    # ── 第5章：事業承継・M&Aコンサルティング（総合問題） ──
    {
        "number": 9,
        "question": "被相続人Aに配偶者B、長男C、長女D、およびDの夫D'（Aの普通養子）がいる場合、民法上の法定相続人の組み合わせとして適切なのは。",
        "choices": {
            "a": "配偶者B",
            "b": "配偶者B、長男C、長女D",
            "c": "配偶者B、長男C、長女D、Dの夫D'",
            "d": "配偶者B、長男C、Dの夫D'",
            "e": "長男C、長女D、Dの夫D'",
            "f": "わからない",
        },
        "answer": "c",
        "chapter": 5,
        "chapter_title": "第5章：事業承継・M&Aコンサルティング（総合問題）",
        "section": "民法：相続人の範囲と順位",
        "explanation": "普通養子縁組では、養子は養親の嫡出子の身分を取得しながら実父母との親族関係も続きます。Dの夫D'はAの普通養子のため実子と同様の相続権を持ちます。配偶者は常に相続人となるため、B・C・D・D'の4人全員が法定相続人です。",
    },
    {
        "number": 10,
        "question": "被相続人Aに配偶者B、長男C（死亡）、孫E（Aの普通養子かつCの子）、孫F（Cの子）がいる場合、孫Eの法定相続分は。",
        "choices": {
            "a": "4分の1",
            "b": "2分の1",
            "c": "8分の3",
            "d": "8分の1",
            "e": "3分の1",
            "f": "わからない",
        },
        "answer": "c",
        "chapter": 5,
        "chapter_title": "第5章：事業承継・M&Aコンサルティング（総合問題）",
        "section": "民法：相続人の範囲と順位",
        "explanation": "EはAの養子（子として1/2×1/2=1/4）かつCの死亡による代襲相続人でもあります。養子としての相続分（1/4）と代襲相続人としての相続分（Cの1/4をE・Fで等分した1/8）を合算し、8分の3となります。",
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

st.markdown("""
<style>
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stToolbarActions"] {display: none !important;}
[data-testid="stHeader"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stDeployButton"] {display: none !important;}
[data-testid="stAppToolbar"] {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}
[data-testid="stBottom"] {display: none !important;}
.stAppDeployButton {display: none !important;}
.stToolbar {display: none !important;}
.viewerBadge_container__r5tak {display: none !important;}
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)


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

    mode_options = {
        "通常（ランダム）": "normal",
        "間違えた問題のみ": "wrong_only",
        "未回答のみ": "unanswered",
    }
    selected_mode_label = st.selectbox("出題モード", list(mode_options.keys()))
    selected_mode = mode_options[selected_mode_label]

    order_options = {"ランダム": False, "番号順": True}
    selected_order_label = st.radio(
        "出題順序", list(order_options.keys()), horizontal=True
    )
    selected_sequential = order_options[selected_order_label]

    pool = QUESTIONS if selected_chapter is None else [q for q in QUESTIONS if q.get("chapter") == selected_chapter]
    max_q = len(pool)
    num_questions = st.number_input(
        "問題数", min_value=1, max_value=max_q, value=max_q, step=1
    )

    st.divider()

    if st.button("スタート ▶", type="primary", use_container_width=True):
        try:
            start_quiz(int(num_questions), selected_mode, selected_sequential, selected_chapter)
            st.rerun()
        except ValueError as e:
            st.error(str(e))

    st.divider()
    st.info(
        "💡 **これはデモ版です（全5章・各2問、合計10問）**\n\n"
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

        explanation = quiz.get("explanation", "")
        if explanation:
            st.info(f"📝 **解説**\n\n{explanation}")

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
        "💡 **これはデモ版です（全5章・各2問、合計10問）**\n\n"
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
