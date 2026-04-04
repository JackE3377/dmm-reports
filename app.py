"""
안티그레비티 — 데일리 소싱 리포트 뷰어
Streamlit 앱: reports/ 폴더의 HTML 파일을 날짜별로 조회
"""
import re
import streamlit as st
from pathlib import Path

# ── 페이지 설정 ────────────────────────────────────────────
st.set_page_config(
    page_title="안티그레비티 소싱 리포트",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS: 사이드바 & 기본 스타일 ────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #1a1a2e; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  .stSelectbox label { color: #a0aec0 !important; font-size: 0.85em !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .block-container { padding-top: 1rem; padding-bottom: 0; }
</style>
""", unsafe_allow_html=True)

# ── reports 폴더에서 HTML 파일 목록 로드 ───────────────────
REPORTS_DIR = Path(__file__).parent / "reports"
html_files = sorted(
    REPORTS_DIR.glob("*_Sourcing_Daily.html"),
    reverse=True,  # 최신 날짜 먼저
)

# ── 날짜 파싱 ─────────────────────────────────────────────
dated_files = []
for f in html_files:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
    if m:
        dated_files.append((m.group(1), f))

# ── 사이드바 ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 안티그레비티")
    st.markdown("### 소싱 리포트 아카이브")
    st.markdown("---")

    if not dated_files:
        st.warning("리포트 없음")
        st.stop()

    st.markdown(f"📁 **{len(dated_files)}개** 리포트 저장됨")
    st.markdown("")

    selected_date = st.selectbox(
        "날짜 선택",
        options=[d for d, _ in dated_files],
        format_func=lambda x: f"📅  {x}",
        index=0,  # 기본: 가장 최신
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.78em; color:#718096; line-height:1.6;'>"
        "도매매(domeggook.com)<br>인기 100위 AI 분석 리포트<br>"
        "매일 자동 업데이트</div>",
        unsafe_allow_html=True,
    )

# ── 선택된 HTML 파일 렌더링 ───────────────────────────────
selected_file = next(f for d, f in dated_files if d == selected_date)

try:
    html_content = selected_file.read_text(encoding="utf-8")
except Exception as e:
    st.error(f"파일 읽기 실패: {e}")
    st.stop()

# 전체 화면에 HTML 렌더링 (스크롤 포함)
st.components.v1.html(html_content, height=5000, scrolling=True)
