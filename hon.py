"""
Surprise_flask_app_fixed.py

Bản này: chỉ hiển thị lời chúc sinh nhật cố định (do bạn nhập sẵn trong biến FIXED_NOTE),
không có form thay đổi hoặc lưu file.
"""

from flask import Flask, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

VIDEO_PATH = 'static/media/qq.mp4'

# 🔹 Nhập lời chúc cố định ở đây:
FIXED_NOTE = """Chúc Anh Phương có 1 ngày sinh nhật thật vui vẻ, vững bước trên con đường tương lai ,luôn cười tươi và hạnh phúc như bây giờ nhé 🎂❤️"""

TEMPLATE = """
<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Happy Birthday ❤️</title>
  <style>
    html,body{height:100%;margin:0;font-family:Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial}
    .bg{background:linear-gradient(135deg,#ffe7f0 0%, #fff6ea 100%);min-height:100%;display:flex;align-items:center;justify-content:center;padding:20px}
    .card{width:100%;max-width:900px;background:rgba(255,255,255,0.85);backdrop-filter:blur(6px);box-shadow:0 10px 30px rgba(0,0,0,0.08);border-radius:18px;overflow:hidden}
    .grid{display:grid;grid-template-columns:1fr 400px}
    @media(max-width:900px){.grid{grid-template-columns:1fr}}
    .left{padding:24px}
    h1{margin:0;font-size:28px}
    .lead{color:#444;margin-top:8px}
    .video-wrap{margin-top:16px;border-radius:12px;overflow:hidden;background:#000}
    video{width:100%;height:100%;display:block}
    .controls{margin-top:12px;display:flex;gap:8px}
    button{cursor:pointer;padding:10px 14px;border-radius:10px;border:0;background:#ff6b9a;color:#fff;font-weight:600}
    .muted{background:#333;color:#fff}
    .right{background:#fff;padding:22px;border-left:1px solid rgba(0,0,0,0.03)}
    .gift{display:flex;flex-direction:column;gap:12px;align-items:center;justify-content:center;height:100%}
    .surprise{padding:14px 18px;border-radius:12px;background:linear-gradient(180deg,#fff3f8,#ffeef5);text-align:center}
    .heart{font-size:56px;transform:scale(1);transition:transform .3s}
    .heart.pop{transform:scale(1.25) rotate(-8deg)}
    .message-box{margin-top:10px;padding:12px;border-radius:10px;background:#fff;border:1px dashed rgba(255,107,154,0.25);min-height:100px;white-space:pre-wrap}
    footer{padding:12px;text-align:center;color:#666;font-size:13px}
  </style>
</head>
<body>
  <div class="bg">
    <div class="card">
      <div class="grid">
        <div class="left">
          <h1>🎉 Chúc mừng sinh nhật 🎂</h1>
          <p class="lead">Một món quà nhỏ gửi tới cậu, chúc cậu một ngày thật đặc biệt ❤️</p>

          <div class="video-wrap">
            {% if video_exists %}
            <video id="bgvideo" loop muted playsinline>
              <source src="/{{ video_path }}" type="video/mp4">
              Trình duyệt của bạn không hỗ trợ video.
            </video>
            {% else %}
            <div style="padding:40px;text-align:center;color:#888">Không tìm thấy video. Đặt file tại <code>{{ video_path }}</code></div>
            {% endif %}
          </div>

          <div class="controls">
            <button id="playBtn">Phát / Tạm dừng</button>
            <button id="muteBtn" class="muted">Bật âm</button>
            <button id="openGiftBtn" style="background:#6b8cff">Mở quà</button>
          </div>
        </div>

        <div class="right">
          <div class="gift">
            <div class="surprise">
              <div id="heart" class="heart">❤️</div>
              <div style="font-weight:700;margin-top:8px">Mở quà để xem lời chúc</div>
            </div>
            <div class="message-box" id="secretBox">Nhấn "Mở quà" để xem nhé 🎁</div>
            <div style="width:100%;text-align:center;margin-top:6px">
              <small style="color:#999">Ngày tạo: {{ now }}</small>
            </div>
          </div>
        </div>
      </div>
      <footer>Thiết kế với ♥ — Một món quà nhỏ bằng Python/Flask</footer>
    </div>
  </div>

  <script>
    const video = document.getElementById('bgvideo');
    const playBtn = document.getElementById('playBtn');
    const muteBtn = document.getElementById('muteBtn');
    const openGiftBtn = document.getElementById('openGiftBtn');
    const heart = document.getElementById('heart');
    const secretBox = document.getElementById('secretBox');

    if (video){ video.play().catch(()=>{}); }

    playBtn.addEventListener('click', ()=>{ if(video){ video.paused ? video.play() : video.pause(); }});
    muteBtn.addEventListener('click', ()=>{ 
      if(video){ 
        video.muted = !video.muted;
        muteBtn.textContent = video.muted ? 'Bật âm' : 'Tắt âm';
        muteBtn.classList.toggle('muted', video.muted);
      }
    });

    openGiftBtn.addEventListener('click', ()=>{
      heart.classList.add('pop');
      setTimeout(()=>heart.classList.remove('pop'),800);
      runConfetti();
      secretBox.textContent = {{ fixed_note|tojson }};
    });

    function runConfetti(){
      const duration = 1200, end = Date.now() + duration;
      (function frame(){
        const left = end - Date.now(); if(left<=0) return;
        for(let i=0;i<10;i++){
          const el = document.createElement('div');
          el.style.position='fixed';
          el.style.left=(Math.random()*100)+'%';
          el.style.top='-10px';
          el.style.fontSize=(8+Math.random()*18)+'px';
          el.textContent=['🎉','💖','✨'][Math.floor(Math.random()*3)];
          document.body.appendChild(el);
          const anim = el.animate([{transform:`translateY(0)`},{transform:`translateY(${window.innerHeight}px)`}],{duration:1500+Math.random()*800});
          anim.onfinish=()=>el.remove();
        }
        requestAnimationFrame(frame);
      })();
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    video_exists = os.path.exists(VIDEO_PATH)
    now = datetime.now().strftime('%d %B %Y')
    return render_template_string(TEMPLATE, video_exists=video_exists, video_path=VIDEO_PATH, now=now, fixed_note=FIXED_NOTE)

if __name__ == '__main__':
    app.run(debug=True)
