"""
안티그레비티 — 데일리 소싱 리포트 뷰어
HTML을 base64 data URL로 변환해 iframe에 직접 렌더링
"""
import re
import base64
import streamlit as st
from pathlib import Path

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

# ── HTML 읽기 ─────────────────────────────────────────────
selected_file = next(f for d, f in dated_files if d == selected_date)

try:
    html_bytes = selected_file.read_bytes()
except Exception as e:
    st.error(f"파일 읽기 실패: {e}")
    st.stop()

# 다운로드 버튼
with st.sidebar:
    st.markdown("---")
    st.download_button(
        label="⬇️ HTML 다운로드",
        data=html_bytes,
        file_name=selected_file.name,
        mime="text/html",
    )

# ── base64 data URL → iframe 렌더링 ──────────────────────
b64 = base64.b64encode(html_bytes).decode()
iframe_html = f"""
<iframe
  src="data:text/html;base64,{b64}"
  width="100%"
  height="7000px"
  style="border:none; display:block;"
  scrolling="yes"
></iframe>
"""
st.markdown(iframe_html, unsafe_allow_html=True)
