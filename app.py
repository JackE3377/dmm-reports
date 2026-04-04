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

# ── CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #1a1a2e; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  .stSelectbox label { color: #a0aec0 !important; font-size: 0.85em !important; }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  .block-container { padding-top: 1rem; padding-bottom: 0; max-width: 100% !important; }
  iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

# ── reports 폴더에서 HTML 파일 목록 로드 ───────────────────
REPORTS_DIR = Path(__file__).parent / "reports"
html_files = sorted(
    REPORTS_DIR.glob("*_Sourcing_Daily.html"),
    reverse=True,
)

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
        index=0,
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

# 다운로드 버튼 (사이드바)
with st.sidebar:
    st.download_button(
        label="⬇️ HTML 다운로드",
        data=html_content.encode("utf-8"),
        file_name=selected_file.name,
        mime="text/html",
    )

# HTML을 감싸서 높이 자동 계산 후 iframe 리사이즈
wrapped_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8">
<style>html,body{{margin:0;padding:0;}}</style>
</head>
<body>
{html_content}
<script>
window.addEventListener('load', function() {{
  const h = document.documentElement.scrollHeight;
  window.parent.postMessage({{isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height: h}}, '*');
}});
</script>
</body>
</html>"""

st.components.v1.html(wrapped_html, height=7000, scrolling=True)
