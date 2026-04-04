"""
안티그레비티 — 데일리 소싱 리포트 뷰어
GitHub Pages URL을 iframe으로 렌더링
"""
import re
import streamlit as st
from pathlib import Path

GITHUB_PAGES_BASE = "https://jacke3377.github.io/dmm-reports"

st.set_page_config(
    page_title="안티그레비티 소싱 리포트",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #1a1a2e; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .block-container { padding-top: 0.5rem; padding-bottom: 0; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# ── reports 폴더 HTML 목록 ─────────────────────────────────
REPORTS_DIR = Path(__file__).parent / "reports"
dated_files = []
for f in sorted(REPORTS_DIR.glob("*_Sourcing_Daily.html"), reverse=True):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
    if m:
        dated_files.append((m.group(1), f))

# ── 사이드바 ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 안티그레비티")
    st.markdown("### 소싱 리포트 아카이브")
    st.markdown("---")

    if not dated_files:
        st.warning("저장된 리포트가 없습니다.")
        st.stop()

    st.markdown(f"📁 **{len(dated_files)}개** 리포트 저장됨")

    selected_date = st.selectbox(
        "날짜 선택",
        options=[d for d, _ in dated_files],
        format_func=lambda x: f"📅  {x}",
        index=0,
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.78em;color:#718096;line-height:1.8'>"
        "도매매(domeggook.com)<br>인기 100위 AI 분석 리포트<br>매일 자동 업데이트</div>",
        unsafe_allow_html=True,
    )

    # 다운로드 버튼
    selected_file = next(f for d, f in dated_files if d == selected_date)
    st.markdown("---")
    st.download_button(
        label="⬇️ HTML 다운로드",
        data=selected_file.read_bytes(),
        file_name=selected_file.name,
        mime="text/html",
    )

# ── GitHub Pages URL로 iframe 렌더링 ─────────────────────
page_url = f"{GITHUB_PAGES_BASE}/reports/{selected_file.name}"
st.components.v1.iframe(page_url, height=7000, scrolling=True)
