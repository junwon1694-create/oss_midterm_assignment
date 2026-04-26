# ============================================================
# Chapter 1. 라이브러리 불러오기
# ============================================================
# base64: 이미지 파일을 HTML에서 사용할 수 있는 data URI로 변환합니다.
# json: Python 데이터를 JavaScript에서 사용할 수 있는 JSON 문자열로 변환합니다.
# Path: 프로젝트 내부 파일 경로를 안전하게 다룹니다.
# streamlit: Python 기반 웹앱을 만듭니다.
# components: HTML/CSS/JavaScript 컴포넌트를 Streamlit에 삽입합니다.
import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# Chapter 2. 기본 설정값
# ============================================================
STUDENT_ID = "2025511009"
STUDENT_NAME = "최준원"

USERS = {
    "player": "1234",
}

# app.py 기준으로 assets 폴더를 찾습니다.
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

ICON_PATH = ASSETS_DIR / "작업대.png"
ENDING_IMAGE_PATH = ASSETS_DIR / "엔딩.png"


# ============================================================
# Chapter 3. 이미지 파일을 HTML용 data URI로 변환
# ============================================================
def image_to_data_uri(path):
    """이미지 파일을 HTML img 태그에서 사용할 수 있는 data URI 문자열로 변환합니다."""

    if not path.exists():
        return ""

    suffix = path.suffix.lower()

    if suffix == ".png":
        mime = "image/png"
    elif suffix == ".webp":
        mime = "image/webp"
    elif suffix == ".ico":
        mime = "image/x-icon"
    else:
        mime = "application/octet-stream"

    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


# ============================================================
# Chapter 4. session_state 초기화
# ============================================================
# Streamlit은 상호작용마다 app.py를 다시 실행하므로
# 로그인 상태처럼 유지해야 하는 값은 session_state에 저장합니다.
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""


# ============================================================
# Chapter 5. 아이템 데이터 캐싱
# ============================================================
# 아이템 이미지는 반복 사용되므로 한 번 data URI로 변환한 뒤 캐싱합니다.
@st.cache_data
def load_item_data():
    """assets 폴더의 아이템 이미지를 읽어 HTML에서 사용할 수 있는 데이터로 변환합니다."""

    item_files = {
        "oak_planks": {"label": "참나무 판자", "file": "참나무판자.webp", "fallback": "판자"},
        "chest": {"label": "상자", "file": "상자.webp", "fallback": "상자"},
        "diamond": {"label": "다이아몬드", "file": "다이아몬드.png", "fallback": "Dia"},
        "stick": {"label": "막대기", "file": "막대기.png", "fallback": "막대"},
        "diamond_pickaxe": {"label": "다이아몬드 곡괭이", "file": "다이아몬드_곡괭이.png", "fallback": "곡괭이"},
        "cake": {"label": "케이크", "file": "케이크.png", "fallback": "케이크"},
        "milk": {"label": "우유", "file": "우유.webp", "fallback": "우유"},
        "sugar": {"label": "설탕", "file": "설탕.png", "fallback": "설탕"},
        "egg": {"label": "달걀", "file": "달걀.webp", "fallback": "달걀"},
        "wheat": {"label": "밀", "file": "밀.png", "fallback": "밀"},
        "stone_slab": {"label": "매끄러운 돌 반블록", "file": "매끄러운 돌반블록.webp", "fallback": "반블록"},
        "armor_stand": {"label": "갑옷 거치대", "file": "갑옷거치대.webp", "fallback": "거치대"},
        "baked_potato": {"label": "구운 감자", "file": "구운감자.png", "fallback": "감자"},
        "carrot": {"label": "당근", "file": "당근.png", "fallback": "당근"},
        "mushroom": {"label": "버섯", "file": "버섯.webp", "fallback": "버섯"},
        "bowl": {"label": "그릇", "file": "그릇.png", "fallback": "그릇"},
        "rabbit": {"label": "토끼고기", "file": "토끼고기.png", "fallback": "토끼"},
        "rabbit_stew": {"label": "토끼 스튜", "file": "토끼 스튜.png", "fallback": "스튜"},
    }

    items = {}

    for item_id, meta in item_files.items():
        image_path = ASSETS_DIR / meta["file"]
        items[item_id] = {
            "label": meta["label"],
            "fallback": meta["fallback"],
            "image": image_to_data_uri(image_path),
        }

    return items


# ============================================================
# Chapter 6. 퀴즈 데이터 캐싱
# ============================================================
# 퀴즈 문제는 실행 중 바뀌지 않는 고정 데이터이므로 캐싱합니다.
@st.cache_data
def load_quiz_data():
    """Easy부터 Impossible까지 5단계 조합법 퀴즈 데이터를 반환합니다."""

    return [
        {
            "level": "Easy",
            "name": "상자",
            "question": "상자(Chest)를 조합해보세요.",
            "target_item": "chest",
            "available_items": ["oak_planks", "stick", "diamond"],
            "hint": "가운데만 비우고 참나무 판자로 둘러싸면 됩니다.",
            "answer": {
                "1": "oak_planks", "2": "oak_planks", "3": "oak_planks",
                "4": "oak_planks", "5": "", "6": "oak_planks",
                "7": "oak_planks", "8": "oak_planks", "9": "oak_planks",
            },
        },
        {
            "level": "Normal",
            "name": "다이아몬드 곡괭이",
            "question": "다이아몬드 곡괭이를 조합해보세요.",
            "target_item": "diamond_pickaxe",
            "available_items": ["diamond", "stick", "oak_planks"],
            "hint": "위쪽 3칸은 다이아몬드, 가운데 세로줄은 막대기입니다.",
            "answer": {
                "1": "diamond", "2": "diamond", "3": "diamond",
                "4": "", "5": "stick", "6": "",
                "7": "", "8": "stick", "9": "",
            },
        },
        {
            "level": "Hard",
            "name": "케이크",
            "question": "케이크(Cake)를 조합해보세요.",
            "target_item": "cake",
            "available_items": ["milk", "sugar", "egg", "wheat"],
            "hint": "위 줄은 우유 3개, 가운데는 설탕-달걀-설탕, 아래 줄은 밀 3개입니다.",
            "answer": {
                "1": "milk", "2": "milk", "3": "milk",
                "4": "sugar", "5": "egg", "6": "sugar",
                "7": "wheat", "8": "wheat", "9": "wheat",
            },
        },
        {
            "level": "Extreme",
            "name": "갑옷 거치대",
            "question": "갑옷 거치대(Armor Stand)를 조합해보세요.",
            "target_item": "armor_stand",
            "available_items": ["stick", "stone_slab", "oak_planks"],
            "hint": "위쪽 3칸은 막대기, 가운데도 막대기, 아래 줄은 막대기-매끄러운 돌 반블록-막대기 입니다.",
            "answer": {
                "1": "stick", "2": "stick", "3": "stick",
                "4": "", "5": "stick", "6": "",
                "7": "stick", "8": "stone_slab", "9": "stick",
            },
        },
        {
            "level": "Impossible",
            "name": "토끼 스튜",
            "question": "토끼 스튜(Rabbit Stew)를 조합해보세요.",
            "target_item": "rabbit_stew",
            "available_items": ["rabbit", "carrot", "baked_potato", "mushroom", "bowl"],
            "hint": "토끼고기, 당근, 구운 감자, 버섯, 그릇을 올바른 위치에 배치합니다.",
            "answer": {
                "1": "", "2": "rabbit", "3": "",
                "4": "carrot", "5": "baked_potato", "6": "mushroom",
                "7": "", "8": "bowl", "9": "",
            },
        },
    ]


# ============================================================
# Chapter 7. Streamlit 페이지 스타일
# ============================================================
def apply_page_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: #1d1d1d;
            color: #f5f5f5;
        }

        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
        }

        .mc-title-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }

        .mc-title-icon {
            width: 46px;
            height: 46px;
            image-rendering: pixelated;
        }

        .mc-title {
            font-size: 30px;
            font-weight: 900;
            color: #ffff55;
            text-shadow: 3px 3px 0 #000;
        }

        .student-box {
            background: #c6c6c6;
            color: #333;
            border: 3px solid;
            border-color: #fff #555 #555 #fff;
            padding: 14px 16px;
            font-weight: 900;
            margin-bottom: 18px;
        }

        div.stButton > button,
        div.stFormSubmitButton > button {
            background: #2f6b35;
            color: #fff8d7;
            border-radius: 0;
            border: 3px solid;
            border-color: #79b56f #123d18 #123d18 #79b56f;
            font-weight: 900;
            box-shadow: inset 3px 3px 0 rgba(255,255,255,0.16),
                        inset -3px -3px 0 rgba(0,0,0,0.32);
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            background: #3f7f3f;
            color: #ffffff;
            border-color: #9ad18d #174d20 #174d20 #9ad18d;
        }

        div.stButton > button:active,
        div.stFormSubmitButton > button:active {
            background: #255928;
            color: #ffffff;
            border-color: #123d18 #79b56f #79b56f #123d18;
        }

        div.stButton > button:focus,
        div.stFormSubmitButton > button:focus {
            color: #ffffff;
            outline: 2px solid #f8d44d;
            outline-offset: 2px;
        }

        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] label p {
            color: #f5f5f5;
            font-weight: 900;
        }

        div[data-testid="stExpander"] {
            background: #1d1d1d;
            border: 2px solid #333;
            border-radius: 6px;
        }

        div[data-testid="stExpander"] details summary {
            background: #2b2b2b;
            color: #f5f5f5;
            border-radius: 6px 6px 0 0;
        }

        div[data-testid="stExpander"] details summary p {
            color: #f5f5f5;
            font-weight: 900;
        }

        div[data-testid="stExpander"] details div[data-testid="stMarkdownContainer"] {
            color: #f5f5f5;
        }

        .mc-help-box,
        .copyright-box {
            background: #2b2b2b;
            color: #f5f5f5;
            border: 3px solid;
            border-color: #777 #111 #111 #777;
            padding: 14px 16px;
            margin-top: 18px;
            margin-bottom: 10px;
            box-shadow: inset 3px 3px 0 rgba(255,255,255,0.08),
                        inset -3px -3px 0 rgba(0,0,0,0.35);
        }

        .mc-help-title {
            color: #ffff55;
            font-weight: 900;
            font-size: 18px;
            text-shadow: 2px 2px 0 #000;
            margin-bottom: 8px;
        }

        .mc-help-text {
            color: #e8e8e8;
            font-size: 16px;
            font-weight: 700;
        }

        .mc-help-text code {
            background: #143d1d;
            color: #9cff8f;
            border: 2px solid #2f6b35;
            padding: 2px 6px;
            font-weight: 900;
        }

        .copyright-title {
            color: #ff5555;
            font-weight: 900;
            font-size: 18px;
            text-shadow: 2px 2px 0 #000;
            margin-bottom: 8px;
        }

        .copyright-text {
            color: #e8e8e8;
            font-size: 15px;
            font-weight: 700;
            line-height: 1.7;
        }

        .copyright-text strong {
            color: #ffff55;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Chapter 8. 공통 제목 출력
# ============================================================
def render_app_title():
    icon_src = image_to_data_uri(ICON_PATH)

    if icon_src:
        title_html = f"""
        <div class="mc-title-row">
            <img class="mc-title-icon" src="{icon_src}" alt="Crafting table icon">
            <div class="mc-title">Minecraft Crafting Quiz</div>
        </div>
        """
    else:
        title_html = '<div class="mc-title">Minecraft Crafting Quiz</div>'

    st.markdown(title_html, unsafe_allow_html=True)


# ============================================================
# Chapter 9. 캐싱 설명 영역
# ============================================================
def render_cache_expander():
    with st.expander("캐싱 적용 위치: 퀴즈 데이터/아이템 데이터 로딩"):
        st.markdown(
            """
            - `load_quiz_data()`에 `@st.cache_data`를 적용했습니다.
            - `load_item_data()`에 `@st.cache_data`를 적용했습니다.
            - 퀴즈 데이터는 실행 중 자주 바뀌지 않으므로 캐싱해서 재사용합니다.
            - 아이템 이미지는 한 번 base64로 변환한 뒤 캐싱해서 반복 변환을 줄입니다.
            """
        )


# ============================================================
# Chapter 10. 저작권 안내 영역
# ============================================================
def render_copyright_notice():
    st.markdown(
        """
        <div class="copyright-box">
            <div class="copyright-title">저작권 안내</div>
            <div class="copyright-text">
                이 웹앱은 <strong>학습 및 과제 제출을 위한 비공식 팬 제작물</strong>입니다.<br>
                Minecraft 및 관련 명칭, 아이템 이미지는 Mojang Studios 및 Microsoft의 자산일 수 있습니다.<br>
                본 프로젝트는 Mojang Studios 또는 Microsoft와 공식적으로 관련이 없습니다.<br>
                사용된 이미지는 <strong>광운대학교 정보융합학부 오픈소스소프트웨어실습</strong> 과제 시연 목적이며, 상업적 용도로 사용하지 않습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Chapter 11. 로그인 전 화면
# ============================================================
def render_login_page():
    render_app_title()

    st.markdown(
        f"""
        <div class="student-box">
            제출자 정보 | 학번: {STUDENT_ID} &nbsp;&nbsp; 이름: {STUDENT_NAME}
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_cache_expander()

    st.subheader("로그인")
    st.caption("퀴즈는 로그인 후에만 풀 수 있습니다.")

    with st.form("login_form"):
        username = st.text_input("아이디", placeholder="player")
        password = st.text_input("비밀번호", type="password", placeholder="1234")
        submitted = st.form_submit_button("로그인", use_container_width=True)

    if submitted:
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호를 확인하세요.")

    st.markdown(
        """
        <div class="mc-help-box">
            <div class="mc-help-title">테스트 계정</div>
            <div class="mc-help-text">
                아이디: <code>player</code> &nbsp; 비밀번호: <code>1234</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_copyright_notice()


# ============================================================
# Chapter 12. 퀴즈 HTML 컴포넌트 생성
# ============================================================
def build_quiz_html(recipes, items, ending_image_src):
    recipes_json = json.dumps(recipes, ensure_ascii=False)
    items_json = json.dumps(items, ensure_ascii=False)
    ending_image_json = json.dumps(ending_image_src, ensure_ascii=False)

    return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 12px;
    background: #1d1d1d;
    color: #f5f5f5;
    font-family: Arial, sans-serif;
}}

.topbar {{
    width: min(860px, 100%);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}}

.quiz-title {{
    color: #ffff55;
    font-size: 24px;
    font-weight: 900;
    text-shadow: 2px 2px 0 #000;
}}

.score {{
    color: #55ff55;
    font-size: 18px;
    font-weight: 900;
    text-align: right;
}}

.progress {{
    width: min(860px, 100%);
    height: 12px;
    background: #111;
    border: 2px solid #555;
    margin-bottom: 14px;
}}

.progress-fill {{
    height: 100%;
    width: 0%;
    background: #3a8a3a;
    transition: width 0.25s;
}}

.question-box {{
    width: min(860px, 100%);
    background: #242424;
    border: 3px solid;
    border-color: #777 #111 #111 #777;
    padding: 14px;
    margin-bottom: 14px;
}}

.level {{
    display: inline-block;
    padding: 5px 10px;
    font-weight: 900;
    margin-bottom: 8px;
    border: 2px solid;
    text-shadow: 1px 1px 0 #000;
}}

.level-easy {{
    background: #123456;
    color: #8fd3ff;
    border-color: #2f80ed;
}}

.level-normal {{
    background: #143d1d;
    color: #9cff8f;
    border-color: #2f9e44;
}}

.level-hard {{
    background: #4a3b00;
    color: #ffe066;
    border-color: #f2c94c;
}}

.level-extreme {{
    background: #4a1f00;
    color: #ff9f6e;
    border-color: #f97316;
}}

.level-impossible {{
    background: #3a123f;
    color: #ff8ff3;
    border-color: #c026d3;
}}

.question {{
    color: #fff8d7;
    font-size: 20px;
    font-weight: 900;
    margin-bottom: 8px;
}}

.hint {{
    color: #d0d0d0;
    font-size: 14px;
}}

.craft-window {{
    display: inline-block;
    background: #c6c6c6;
    border: 3px solid;
    border-color: #fff #555 #555 #fff;
    padding: 10px;
    color: #404040;
    image-rendering: pixelated;
}}

.craft-label {{
    font-size: 24px;
    margin-bottom: 8px;
}}

.craft-body {{
    display: flex;
    align-items: center;
    gap: 28px;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(3, 64px);
    grid-template-rows: repeat(3, 64px);
}}

.slot,
.result-slot,
.palette-slot {{
    background: #8b8b8b;
    border: 3px solid;
    border-color: #373737 #fff #fff #373737;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.slot {{
    width: 64px;
    height: 64px;
    margin: 1px;
    cursor: pointer;
}}

.slot.drag-over {{
    background: #a8a8a8;
}}

.arrow {{
    color: #909090;
    font-size: 72px;
    font-weight: 900;
}}

.result-area {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}}

.result-slot {{
    width: 78px;
    height: 78px;
}}

.result-name {{
    color: #333;
    font-weight: 900;
    max-width: 100px;
    text-align: center;
}}

.item-img {{
    width: 52px;
    height: 52px;
    image-rendering: pixelated;
    pointer-events: none;
}}

.result-slot .item-img {{
    width: 60px;
    height: 60px;
}}

.fallback-item {{
    width: 50px;
    height: 50px;
    background: #333;
    color: #fff;
    border: 2px solid #111;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 900;
    text-align: center;
    pointer-events: none;
}}

.dim {{
    opacity: 0.25;
}}

.button-row {{
    display: flex;
    gap: 8px;
    margin: 14px 0;
    flex-wrap: wrap;
}}

.mc-btn {{
    background: #2f6b35;
    color: #fff8d7;
    border: 3px solid;
    border-color: #79b56f #123d18 #123d18 #79b56f;
    padding: 10px 16px;
    font-weight: 900;
    cursor: pointer;
}}

.mc-btn:active {{
    border-color: #123d18 #79b56f #79b56f #123d18;
}}

.mc-btn.gray {{
    background: #5a5a5a;
    border-color: #aaa #222 #222 #aaa;
}}

.feedback {{
    display: none;
    width: min(860px, 100%);
    padding: 12px;
    margin-bottom: 12px;
    font-weight: 900;
    text-align: center;
}}

.feedback.ok {{
    display: block;
    background: #143d1d;
    color: #9cff8f;
    border: 2px solid #2f6b35;
}}

.feedback.fail {{
    display: block;
    background: #3d1414;
    color: #ffb0b0;
    border: 2px solid #7d2f2f;
}}

.palette-title {{
    margin: 12px 0 6px;
    color: #fff8d7;
    font-weight: 900;
}}

.palette {{
    width: min(860px, 100%);
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    background: #8b8b8b;
    border: 3px solid;
    border-color: #373737 #fff #fff #373737;
    padding: 6px;
}}

.palette-slot {{
    width: 84px;
    min-height: 92px;
    flex-direction: column;
    gap: 4px;
    cursor: grab;
}}

.palette-slot.selected {{
    outline: 4px solid #ffff55;
    outline-offset: -4px;
}}

.palette-name {{
    color: #fff;
    font-size: 12px;
    font-weight: 900;
    text-shadow: 1px 1px 0 #000;
    text-align: center;
}}

.final {{
    width: min(860px, 100%);
    min-height: 720px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 28px 10px 46px;
}}

.final-panel {{
    width: min(760px, 100%);
    background: #242424;
    border: 4px solid;
    border-color: #777 #111 #111 #777;
    padding: 18px;
    text-align: center;
    box-shadow: inset 4px 4px 0 rgba(255,255,255,0.08),
                inset -4px -4px 0 rgba(0,0,0,0.35);
}}

.final-art-wrap {{
    width: 100%;
    background: #111;
    border: 3px solid;
    border-color: #111 #777 #777 #111;
    margin-bottom: 18px;
    overflow: hidden;
}}

.final-art {{
    display: block;
    width: 100%;
    max-height: 380px;
    object-fit: contain;
    image-rendering: auto;
}}

.final h1 {{
    color: #ffff55;
    font-size: 32px;
    text-shadow: 3px 3px 0 #000;
    margin: 8px 0 14px;
}}

.final-score {{
    color: #55ff55;
    font-size: 42px;
    font-weight: 900;
    text-shadow: 3px 3px 0 #000;
    margin: 10px 0;
}}

.final-complete {{
    color: #8fd3ff;
    font-size: 18px;
    font-weight: 900;
    margin: 10px 0;
}}

.final-message {{
    color: #fff8d7;
    font-size: 18px;
    font-weight: 900;
    margin: 14px 0 10px;
}}

.final-time {{
    display: inline-block;
    background: #143d1d;
    color: #9cff8f;
    border: 2px solid #2f6b35;
    padding: 8px 12px;
    margin: 8px 0 18px;
    font-weight: 900;
}}
</style>
</head>
<body>
<div id="app"></div>

<script>
const RECIPES = {recipes_json};
const ITEMS = {items_json};
const ENDING_IMAGE = {ending_image_json};
const SLOTS = ["1","2","3","4","5","6","7","8","9"];

let qIndex = 0;
let score = 0;
let selectedItem = "";
let board = emptyBoard();
let answered = false;
let triedWrong = false;
let startTime = Date.now();
let timerId = null;

function emptyBoard() {{
    return Object.fromEntries(SLOTS.map(slot => [slot, ""]));
}}

function itemHtml(itemId, dim=false) {{
    if (!itemId) return "";

    const item = ITEMS[itemId] || {{}};
    const dimClass = dim ? " dim" : "";

    if (item.image) {{
        return `<img class="item-img${{dimClass}}" src="${{item.image}}" alt="${{item.label || itemId}}">`;
    }}

    return `<div class="fallback-item${{dimClass}}">${{item.fallback || itemId}}</div>`;
}}

function labelOf(itemId) {{
    return (ITEMS[itemId] && ITEMS[itemId].label) || itemId;
}}

function elapsedSeconds() {{
    return Math.floor((Date.now() - startTime) / 1000);
}}

function formatSeconds(totalSeconds) {{
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;

    if (minutes > 0) {{
        return `${{minutes}}분 ${{seconds}}초`;
    }}

    return `${{seconds}}초`;
}}

function updateTimerText() {{
    const timerEl = document.getElementById("timerText");

    if (timerEl) {{
        timerEl.textContent = formatSeconds(elapsedSeconds());
    }}
}}

function startTimer() {{
    if (timerId === null) {{
        timerId = setInterval(updateTimerText, 1000);
    }}

    updateTimerText();
}}

function stopTimer() {{
    if (timerId !== null) {{
        clearInterval(timerId);
        timerId = null;
    }}
}}

function levelClass(level) {{
    const key = String(level).toLowerCase();

    if (key === "easy") return "level-easy";
    if (key === "normal") return "level-normal";
    if (key === "hard") return "level-hard";
    if (key === "extreme") return "level-extreme";
    if (key === "impossible") return "level-impossible";

    return "level-easy";
}}

function render() {{
    const q = RECIPES[qIndex];

    document.getElementById("app").innerHTML = `
        <div class="topbar">
            <div class="quiz-title">Crafting Quiz</div>
            <div class="score">
                시간 <span id="timerText">${{formatSeconds(elapsedSeconds())}}</span>
                &nbsp;|&nbsp;
                퍼펙트 조합 ${{score}} / ${{RECIPES.length}}
            </div>
        </div>

        <div class="progress">
            <div class="progress-fill" style="width:${{qIndex / RECIPES.length * 100}}%"></div>
        </div>

        <div class="question-box">
            <div class="level ${{levelClass(q.level)}}">${{q.level}}</div>
            <div class="question">${{q.question}}</div>
            <div class="hint">힌트: ${{q.hint}}</div>
        </div>

        <div class="craft-window">
            <div class="craft-label">제작</div>
            <div class="craft-body">
                <div class="grid">
                    ${{SLOTS.map(slot => `
                        <div class="slot" data-slot="${{slot}}">
                            ${{itemHtml(board[slot])}}
                        </div>
                    `).join("")}}
                </div>

                <div class="arrow">▶</div>

                <div class="result-area">
                    <div class="result-slot">
                        ${{itemHtml(q.target_item, !answered)}}
                    </div>
                    <div class="result-name">${{labelOf(q.target_item)}}</div>
                </div>
            </div>
        </div>

        <div class="button-row">
            <button class="mc-btn" id="checkBtn">정답 확인</button>
            <button class="mc-btn gray" id="resetBtn">초기화</button>
            <button class="mc-btn" id="nextBtn" style="display:${{answered ? "inline-block" : "none"}}">다음 문제</button>
        </div>

        <div id="feedback" class="feedback"></div>

        <div class="palette-title">아이템 팔레트</div>
        <div class="palette">
            ${{q.available_items.map(itemId => `
                <div class="palette-slot ${{selectedItem === itemId ? "selected" : ""}}" draggable="true" data-item="${{itemId}}">
                    ${{itemHtml(itemId)}}
                    <div class="palette-name">${{labelOf(itemId)}}</div>
                </div>
            `).join("")}}
        </div>
    `;

    bindEvents();
    updateTimerText();
}}

function bindEvents() {{
    document.querySelectorAll(".palette-slot").forEach(el => {{
        const itemId = el.dataset.item;

        el.addEventListener("click", () => {{
            selectedItem = selectedItem === itemId ? "" : itemId;
            render();
        }});

        el.addEventListener("dragstart", event => {{
            selectedItem = itemId;
            event.dataTransfer.setData("text/plain", itemId);
        }});
    }});

    document.querySelectorAll(".slot").forEach(el => {{
        const slot = el.dataset.slot;

        el.addEventListener("dragover", event => {{
            event.preventDefault();
            el.classList.add("drag-over");
        }});

        el.addEventListener("dragleave", () => {{
            el.classList.remove("drag-over");
        }});

        el.addEventListener("drop", event => {{
            event.preventDefault();
            el.classList.remove("drag-over");

            const itemId = event.dataTransfer.getData("text/plain");
            if (itemId) placeItem(slot, itemId);
        }});

        el.addEventListener("click", () => {{
            if (board[slot]) {{
                placeItem(slot, "");
            }} else if (selectedItem) {{
                placeItem(slot, selectedItem);
            }}
        }});
    }});

    document.getElementById("checkBtn").addEventListener("click", checkAnswer);
    document.getElementById("resetBtn").addEventListener("click", resetBoard);
    document.getElementById("nextBtn").addEventListener("click", nextQuestion);
}}

function placeItem(slot, itemId) {{
    if (answered) return;

    board[slot] = itemId;
    updateBoardOnly();
    clearFeedback();
}}

function updateBoardOnly() {{
    document.querySelectorAll(".slot").forEach(el => {{
        const slot = el.dataset.slot;
        el.innerHTML = itemHtml(board[slot]);
    }});
}}

function clearFeedback() {{
    const fb = document.getElementById("feedback");
    fb.className = "feedback";
    fb.textContent = "";
}}

function resetBoard() {{
    if (answered) return;

    board = emptyBoard();
    updateBoardOnly();
    clearFeedback();
}}

function checkAnswer() {{
    if (answered) return;

    const q = RECIPES[qIndex];
    const ok = SLOTS.every(slot => (board[slot] || "") === (q.answer[slot] || ""));
    const fb = document.getElementById("feedback");

    if (ok) {{
        if (!triedWrong) {{
            score += 1;
        }}

        answered = true;
        render();

        const resultText = triedWrong
            ? `정답입니다! ${{q.name}} 조합에 성공했습니다. (퍼펙트 조합 점수는 올라가지 않습니다.)`
            : `정답입니다! ${{q.name}} 조합에 성공했습니다. (퍼펙트 조합 +1점!)`;

        document.getElementById("feedback").className = "feedback ok";
        document.getElementById("feedback").textContent = resultText;
    }} else {{
        triedWrong = true;
        fb.className = "feedback fail";
        fb.textContent = "오답입니다. 다시 배치해보세요. 정답을 맞히면 다음 문제로 넘어갈 수 있습니다.";
    }}
}}

function nextQuestion() {{
    qIndex += 1;

    if (qIndex >= RECIPES.length) {{
        showFinal();
        return;
    }}

    board = emptyBoard();
    selectedItem = "";
    answered = false;
    triedWrong = false;
    render();
}}

function gradeMessage() {{
    if (score === RECIPES.length) return "전설의 크래프터입니다!";
    if (score >= 4) return "상급 생존자입니다!";
    if (score >= 2) return "조합법을 조금 더 연습해보세요.";
    return "나무부터 다시 캐야 할 것 같습니다.";
}}

function showFinal() {{
    stopTimer();

    const finalSeconds = elapsedSeconds();
    const endingImageHtml = ENDING_IMAGE
        ? `<div class="final-art-wrap">
               <img class="final-art" src="${{ENDING_IMAGE}}" alt="Quiz ending scene">
           </div>`
        : "";

    document.getElementById("app").innerHTML = `
        <div class="final">
            <div class="final-panel">
                ${{endingImageHtml}}
                <h1>퀴즈 완료</h1>
                <div class="final-complete">완성한 조합 ${{RECIPES.length}} / ${{RECIPES.length}}</div>
                <div class="final-score">퍼펙트 조합 ${{score}} / ${{RECIPES.length}}</div>
                <div class="final-message">${{gradeMessage()}}</div>
                <div class="final-time">총 소요 시간: ${{formatSeconds(finalSeconds)}}</div>
                <br>
                <button class="mc-btn" onclick="restartQuiz()">다시 풀기</button>
            </div>
        </div>
    `;
}}

function restartQuiz() {{
    qIndex = 0;
    score = 0;
    selectedItem = "";
    board = emptyBoard();
    answered = false;
    triedWrong = false;
    startTime = Date.now();

    stopTimer();
    startTimer();
    render();
}}

startTimer();
render();
</script>
</body>
</html>
"""


# ============================================================
# Chapter 13. 로그인 후 실제 퀴즈 화면
# ============================================================
def render_quiz_page():
    render_app_title()

    st.success(f"{st.session_state.username}님, 로그인되었습니다.")

    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    recipes = load_quiz_data()
    items = load_item_data()
    ending_image_src = image_to_data_uri(ENDING_IMAGE_PATH)

    components.html(
        build_quiz_html(recipes, items, ending_image_src),
        height=1050,
        scrolling=True,
    )


# ============================================================
# Chapter 14. main 함수
# ============================================================
def main():
    st.set_page_config(
        page_title="Minecraft Crafting Quiz",
        page_icon="⛏",
        layout="wide",
    )

    init_session_state()
    apply_page_style()

    if st.session_state.logged_in:
        render_quiz_page()
    else:
        render_login_page()


# ============================================================
# Chapter 15. 실행 진입점
# ============================================================
if __name__ == "__main__":
    main()
