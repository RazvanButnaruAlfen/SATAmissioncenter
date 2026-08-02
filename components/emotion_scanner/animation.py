"""Fullscreen visual effects used during E.M.O.S. scanning."""


def overlay_html(title: str, message: str, progress: int, *, detected: bool = False) -> str:
    accent = "#ff70b8" if detected else "#36aef5"
    pulse_name = "emosPinkPulse" if detected else "emosBluePulse"
    return f"""
    <style>
    @keyframes emosBluePulse {{
      0%,100% {{background:rgba(16,65,98,.72); box-shadow:inset 0 0 80px rgba(54,174,245,.22);}}
      50% {{background:rgba(13,39,63,.88); box-shadow:inset 0 0 180px rgba(54,174,245,.62);}}
    }}
    @keyframes emosPinkPulse {{
      0%,100% {{background:rgba(83,24,61,.76); box-shadow:inset 0 0 90px rgba(255,112,184,.30);}}
      50% {{background:rgba(38,18,47,.92); box-shadow:inset 0 0 210px rgba(255,112,184,.78);}}
    }}
    @keyframes scanLine {{
      0% {{top:-10%; opacity:0;}}
      15% {{opacity:.9;}}
      85% {{opacity:.9;}}
      100% {{top:110%; opacity:0;}}
    }}
    .emos-overlay {{
      position:fixed; inset:0; z-index:999999;
      display:flex; align-items:center; justify-content:center;
      padding:20px; color:white; backdrop-filter:blur(5px);
      animation:{pulse_name} 1.15s ease-in-out infinite;
    }}
    .emos-overlay::after {{
      content:""; position:absolute; left:0; right:0; height:3px;
      background:linear-gradient(90deg,transparent,{accent},transparent);
      box-shadow:0 0 22px {accent}; animation:scanLine 2.2s linear infinite;
    }}
    .emos-console {{
      position:relative; width:min(720px,94vw); padding:28px;
      border:1px solid {accent}; border-radius:20px;
      background:rgba(3,13,22,.88); text-align:center;
      box-shadow:0 0 40px {accent}55;
    }}
    .emos-system {{font-size:.75rem;letter-spacing:.18em;color:{accent};font-weight:900;}}
    .emos-main {{font-size:clamp(1.7rem,7vw,3rem);font-weight:950;margin-top:12px;line-height:1.08;}}
    .emos-message {{font-size:clamp(1rem,4vw,1.25rem);color:#d6e2ea;margin-top:18px;line-height:1.45;}}
    .emos-warning {{margin-top:12px;color:#ffd98d;font-weight:800;}}
    .emos-bar {{height:12px;background:#172b38;border-radius:10px;margin-top:24px;overflow:hidden;}}
    .emos-fill {{height:100%;width:{progress}%;background:linear-gradient(90deg,#36aef5,{accent});box-shadow:0 0 18px {accent};}}
    .emos-percent {{margin-top:8px;color:#8ea5b5;font-size:.8rem;letter-spacing:.08em;}}
    </style>
    <div class="emos-overlay">
      <div class="emos-console">
        <div class="emos-system">S.A.T.A. • E.M.O.S. v1.0</div>
        <div class="emos-main">{title}</div>
        <div class="emos-message">{message}</div>
        {('<div class="emos-warning">SCANARE ÎN PROGRES • NU MIȘCAȚI TELEFONUL</div>' if detected else '')}
        <div class="emos-bar"><div class="emos-fill"></div></div>
        <div class="emos-percent">PROGRES {progress}%</div>
      </div>
    </div>
    """
