#!/usr/bin/env python3
"""
Website DOZE Company (Flask)
----------------------------
Menjalankan website DOZE Company sebagai aplikasi Python.

Persiapan:
    pip install flask

Struktur folder:
    app.py
    logo.png        <- logo DOZE (sudah disertakan)

Jalankan:
    python app.py
    lalu buka http://localhost:5000

Fitur tambahan dibanding versi HTML biasa:
    - Permintaan dari form kontak otomatis tersimpan ke leads.csv
      (selain tetap membuka WhatsApp), jadi tidak ada calon klien yang terlewat.

Deploy (contoh): pip install gunicorn && gunicorn app:app
"""
import csv
import os
import threading
from datetime import datetime

from flask import Flask, Response, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(BASE, "leads.csv")
FIELDS = ["nama", "kontak", "layanan", "budget", "deadline", "kebutuhan"]
MAX_LEN = 2000
_lock = threading.Lock()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # batasi ukuran request


def bersihkan(nilai) -> str:
    """Potong teks dan cegah CSV injection (sel diawali = + - @)."""
    s = str(nilai or "").strip()[:MAX_LEN].replace("\r", " ").replace("\n", " ")
    return "'" + s if s[:1] in ("=", "+", "-", "@") else s


@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/logo.png")
def logo():
    return send_from_directory(BASE, "logo.png", max_age=86400)


@app.route("/kirim", methods=["POST"])
def kirim():
    data = request.get_json(silent=True) or {}
    if not str(data.get("nama", "")).strip() or not str(data.get("kebutuhan", "")).strip():
        return jsonify(ok=False, error="Data tidak lengkap"), 400
    baris = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + [bersihkan(data.get(f)) for f in FIELDS]
    with _lock:
        baru = not os.path.exists(LEADS_FILE)
        with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if baru:
                w.writerow(["waktu"] + FIELDS)
            w.writerow(baris)
    return jsonify(ok=True)


# ---------------------------------------------------------------------
# Isi halaman website (HTML/CSS/JS). Edit teks di bawah ini sesuai kebutuhan.
# ---------------------------------------------------------------------
HTML = r'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>DOZE Company — Jasa Akademik, Desain & Solusi Profesional</title>
<meta name="description" content="DOZE Company menyediakan jasa akademik, desain grafis, olah data, presentation design, branding, social media design, dan berbagai layanan profesional lainnya. Konsultasikan kebutuhan Anda bersama kami.">
<link rel="icon" href="/logo.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap">
<style>
:root{--bg:#f6f9f7;--card:#fff;--ink:#0e1d19;--mute:#52625c;--line:#dce5e0;--acc:#17784f;--ai:#fff;--dk:#0a1814;--dki:#eaf2ee;
box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0c1512;--card:#13201b;--ink:#e8f0ec;--mute:#94a59e;--line:#23342d;--acc:#3fc08a;--ai:#04130d;--dk:#070e0c}}
:root[data-theme="dark"]{--bg:#0c1512;--card:#13201b;--ink:#e8f0ec;--mute:#94a59e;--line:#23342d;--acc:#3fc08a;--ai:#04130d;--dk:#070e0c}
html{scroll-behavior:smooth;scroll-padding-top:calc(72px + env(safe-area-inset-top,0px))}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.65 "Plus Jakarta Sans",system-ui,sans-serif;overflow-x:hidden}
h1,h2,h3{margin:0;line-height:1.15;letter-spacing:-.02em}
a{color:inherit}
.w{max-width:1100px;margin:0 auto;padding:0 20px}
header{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
header .w{display:flex;align-items:center;justify-content:space-between;height:68px;gap:14px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;text-decoration:none}
.lg{background:#fff;border-radius:10px;padding:3px;height:46px;width:46px;object-fit:contain}
nav{display:flex;gap:18px;font-size:14px}
nav a{text-decoration:none;color:var(--mute)}nav a:hover{color:var(--acc)}
.btn{display:inline-block;background:var(--acc);color:var(--ai);padding:12px 22px;border-radius:8px;font-weight:600;text-decoration:none;border:0;font:inherit;font-weight:600;cursor:pointer;transition:transform .2s,box-shadow .2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(23,120,79,.3)}
.btn.o{background:none;color:var(--ink);border:1px solid var(--line)}
#bg{display:none;background:none;border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:8px 12px;font:inherit}
.hero{padding:84px 0 64px;display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center}
.hero h1{font-size:clamp(34px,5.4vw,56px);font-weight:800}
.hero p{color:var(--mute);font-size:18px;margin:20px 0 28px;max-width:54ch}
.trust{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:28px;font-size:13px;color:var(--mute)}
.trust span:before{content:"✓ ";color:var(--acc);font-weight:800}
.fl{display:grid;gap:14px}
.fl div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:0 10px 30px rgba(10,24,20,.06);animation:fl 6s ease-in-out infinite}
.fl div:nth-child(2){margin-left:36px;animation-delay:-2s}.fl div:nth-child(3){animation-delay:-4s}
.fl b{display:block;color:var(--acc)}.fl small{color:var(--mute)}
@keyframes fl{50%{transform:translateY(-8px)}}
section{padding:68px 0}
.lbl{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);font-weight:600;margin-bottom:10px}
h2{font-size:clamp(26px,4vw,38px);font-weight:800;margin-bottom:12px}
.sub{color:var(--mute);max-width:60ch;margin:0 0 32px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;transition:transform .25s,box-shadow .25s}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 30px rgba(10,24,20,.1)}
.card h3{font-size:18px;margin-bottom:6px}.card p{margin:0;color:var(--mute);font-size:15px}
.card .ac{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}
.card .ac a{font-size:13px;color:var(--acc);font-weight:600;text-decoration:none}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px;padding:0 0 8px}
.stats b{font-size:34px;font-weight:800;color:var(--acc);display:block}.stats span{color:var(--mute);font-size:14px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chips span{border:1px solid var(--line);background:var(--bg);border-radius:99px;padding:5px 13px;font-size:13px}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.pf-f{display:flex;gap:8px;overflow-x:auto;padding-bottom:10px;margin-bottom:16px}
.pf-f button{flex:none;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:99px;padding:7px 16px;font:inherit;font-size:14px;cursor:pointer}
.pf-f button.on{background:var(--acc);color:var(--ai);border-color:var(--acc)}
.pf{border-radius:10px;overflow:hidden;margin-bottom:12px;background:#dcebe3}.pf svg{display:block;width:100%;height:auto}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:24px;counter-reset:s}
.steps div{counter-increment:s;border-top:2px solid var(--line);padding-top:16px}
.steps div:before{content:"0" counter(s);font-weight:800;font-size:26px;color:var(--acc);display:block}
.steps h3{font-size:18px;margin:4px 0}.steps p{margin:0;color:var(--mute);font-size:15px}
.q{color:var(--acc);letter-spacing:2px}
.ph{font-size:12px;color:var(--mute);margin-top:10px}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 20px;margin-bottom:10px}
summary{cursor:pointer;font-weight:600}details p{margin:10px 0 0;color:var(--mute)}
.cta{background:var(--dk);color:var(--dki);text-align:center;border-radius:20px;padding:60px 24px}
.cta p{opacity:.8;max-width:56ch;margin:0 auto 26px}.cta .btn.o{color:var(--dki);border-color:#ffffff40}
form{display:grid;grid-template-columns:1fr 1fr;gap:12px}
form .f{grid-column:1/-1}
input,select,textarea{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:11px 13px;width:100%}
input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,a:focus-visible,button:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.ct{display:grid;grid-template-columns:.8fr 1.2fr;gap:36px}
.ct p{margin:0 0 12px;color:var(--mute)}.ct b{color:var(--ink);display:block}
#ok{display:none;color:var(--acc);font-weight:600;margin-top:8px}
footer{background:var(--dk);color:var(--dki);padding:48px 0 28px;margin-top:40px}
footer .cols{display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:24px}
footer h4{margin:0 0 10px;font-size:14px}footer a,footer li{font-size:14px;opacity:.78;text-decoration:none}
footer ul{list-style:none;padding:0;margin:0;display:grid;gap:6px}
footer small{display:block;opacity:.6;margin-top:28px;border-top:1px solid #ffffff22;padding-top:18px;line-height:1.6}
.wa{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));background:#1fa855;color:#fff;border-radius:99px;padding:13px 20px;font-weight:600;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.25);z-index:9}
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s,transform .6s}.rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.fl div{animation:none}html{scroll-behavior:auto}}
@media(max-width:820px){
 nav{display:none;position:absolute;top:68px;left:0;right:0;background:var(--bg);flex-direction:column;padding:16px 20px;border-bottom:1px solid var(--line)}nav.open{display:flex}
 #bg{display:block}header .btn{display:none}
 .hero,.ct{grid-template-columns:1fr}.hero{padding:48px 0}.fl{display:none}
 footer .cols{grid-template-columns:1fr 1fr}form{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="w">
  <a class="brand" href="#home"><img class="lg" src="/logo.png" alt="Logo DOZE Company"><span>DOZE Company</span></a>
  <nav id="nv"><a href="#home">Home</a><a href="#tentang">Tentang Kami</a><a href="#layanan">Layanan</a><a href="#portofolio">Portofolio</a><a href="#proses">Proses</a><a href="#testimoni">Testimoni</a><a href="#faq">FAQ</a><a href="#kontak">Kontak</a></nav>
  <a class="btn" href="#" data-wa="Halo DOZE Company, saya ingin konsultasi gratis.">Konsultasi Gratis</a>
  <button id="bg" aria-label="Buka menu">Menu</button>
</div></header>

<main id="home">
<div class="w hero">
  <div>
    <div class="lbl">Professional Academic &amp; Creative Services</div>
    <h1>Solusi Profesional untuk Akademik, Kreativitas, dan Kebutuhan Digital Anda.</h1>
    <p>DOZE Company membantu mahasiswa, pelajar, guru, peneliti, bisnis, organisasi, dan individu melalui layanan akademik, desain, dan solusi digital yang profesional, kreatif, dan berkualitas.</p>
    <a class="btn" href="#" data-wa="Halo DOZE Company, saya ingin konsultasi gratis.">Konsultasi Gratis</a> <a class="btn o" href="#layanan">Lihat Layanan</a>
    <div class="trust"><span>Professional Service</span><span>Quality Focused</span><span>Confidential</span><span>On-Time Delivery</span></div>
  </div>
  <div class="fl"><div><b>Academic Support</b><small>Pendampingan, editing, olah data</small></div><div><b>Creative Design</b><small>Logo, poster, branding, CV</small></div><div><b>Digital Solutions</b><small>PPT, Excel, video editing</small></div></div>
</div>

<div class="w"><div class="stats rv">
  <div class="card"><b>[500+]</b><span>Projects Completed</span></div>
  <div class="card"><b>[100+]</b><span>Satisfied Clients</span></div>
  <div class="card"><b>[10+]</b><span>Professional Services</span></div>
  <div class="card"><b>Fast</b><span>&amp; Responsive Support</span></div>
</div><p class="ph w" style="padding:0">Angka dalam kurung [ ] adalah placeholder, ganti dengan data asli.</p></div>

<section id="tentang"><div class="w rv">
  <div class="lbl">Tentang Kami</div><h2>More Than Just a Service.</h2>
  <p class="sub">DOZE Company hadir sebagai partner profesional untuk membantu menyelesaikan berbagai kebutuhan akademik, kreatif, desain, dan digital. Kami mengutamakan kualitas, ketepatan waktu, komunikasi yang jelas, serta solusi yang disesuaikan dengan kebutuhan setiap klien.</p>
  <div class="grid" id="vals"></div>
</div></section>

<section id="layanan" style="padding-top:0"><div class="w rv">
  <div class="lbl">Layanan</div><h2>Our Professional Services</h2>
  <div class="two">
    <div class="card"><h3>Akademik</h3><p>Membantu kebutuhan akademik dengan pendekatan profesional, sistematis, dan disesuaikan dengan kebutuhan pengguna.</p><div class="chips" id="ak"></div></div>
    <div class="card"><h3>Creative &amp; Design</h3><p>Mengubah ide menjadi visual yang profesional, menarik, dan memiliki karakter brand yang kuat.</p><div class="chips" id="ds"></div></div>
  </div>
  <div class="card" style="margin-top:16px"><h3>Need Something Else?</h3><p>Tidak menemukan layanan yang Anda cari? DOZE Company juga menerima berbagai kebutuhan profesional, kreatif, digital, dan administrasi lainnya. Ceritakan kebutuhan Anda, kami bantu menentukan solusi yang paling sesuai.</p><div class="ac"><a class="btn" href="#" data-wa="Halo DOZE Company, saya ingin mendiskusikan kebutuhan di luar daftar layanan.">Diskusikan Kebutuhan Anda</a></div></div>
</div></section>

<section style="padding-top:0"><div class="w rv">
  <div class="lbl">Popular</div><h2>Popular Services</h2>
  <div class="grid" id="pop"></div>
</div></section>

<section id="portofolio" style="padding-top:0"><div class="w rv">
  <div class="lbl">Portofolio</div><h2>Selected Works</h2>
  <div class="pf-f" id="pff"></div>
  <div class="grid" id="pfg"></div>
  <p class="ph">Gambar di atas adalah ilustrasi contoh. Ganti dengan foto hasil karya asli Anda.</p>
</div></section>

<section id="proses" style="padding-top:0"><div class="w rv">
  <div class="lbl">Proses</div><h2>Simple Process. Professional Results.</h2><div style="height:20px"></div>
  <div class="steps">
    <div><h3>Konsultasi</h3><p>Sampaikan kebutuhan Anda kepada tim DOZE Company.</p></div>
    <div><h3>Brief &amp; Estimasi</h3><p>Kami memberikan rekomendasi, scope pekerjaan, estimasi waktu, dan biaya.</p></div>
    <div><h3>Production</h3><p>Pekerjaan dikerjakan profesional sesuai brief yang disepakati.</p></div>
    <div><h3>Review &amp; Delivery</h3><p>Hasil dikirim untuk direview dan diselesaikan sesuai kesepakatan.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="w rv">
  <div class="lbl">Keunggulan</div><h2>Why Choose DOZE Company?</h2><div style="height:16px"></div>
  <div class="grid" id="why"></div>
</div></section>

<section id="testimoni" style="padding-top:0"><div class="w rv">
  <div class="lbl">Testimoni</div><h2>What Our Clients Say</h2><div style="height:16px"></div>
  <div class="grid">
    <div class="card"><div class="q">★★★★★</div><p>“Gila sih, fast respon banget! Desainnya sesuai ekspektasi, bahkan lebih bagus dari yang aku bayangin. Worth it parah, auto langganan!”</p><div class="ph">— F*i*r*z El-T*ani</div></div>
    <div class="card"><div class="q">★★★★★</div><p>“Awalnya bingung mau mulai dari mana, ternyata dibantuin step by step sampai kelar. Komunikasinya enak, gak bikin overthinking. Recommended banget, no debat!”</p><div class="ph">— C*r**ine</div></div>
    <div class="card"><div class="q">★★★★★</div><p>“Formatting dokumennya rapi banget, deadline aman, nggak pake drama. Makasih DOZE, beneran jadi penyelamat!”</p><div class="ph">— W*la*dar* S**t**ni</div></div>
  </div>
</div></section>

<section id="faq" style="padding-top:0"><div class="w rv">
  <div class="lbl">FAQ</div><h2>Pertanyaan Umum</h2><div style="height:12px"></div><div id="fq"></div>
</div></section>

<section style="padding-top:0"><div class="w"><div class="cta rv">
  <h2 style="max-width:none">Punya Kebutuhan? Mari Diskusikan.</h2>
  <p>Tidak perlu bingung mencari banyak penyedia jasa. Ceritakan kebutuhan Anda kepada DOZE Company dan kami akan membantu menemukan solusi yang tepat.</p>
  <a class="btn" href="#" data-wa="Halo DOZE Company, saya ingin berkonsultasi.">Konsultasi via WhatsApp</a> <a class="btn o" href="#layanan">Lihat Layanan</a>
</div></div></section>

<section id="kontak" style="padding-top:0"><div class="w ct rv">
  <div>
    <div class="lbl">Kontak</div><h2>Let’s Work Together.</h2><div style="height:12px"></div>
    <p><b>WhatsApp</b><a href="https://wa.me/6281225112413">0812-2511-2413</a></p>
    <p><b>Email</b><a href="mailto:dozejokii@gmail.com">dozejokii@gmail.com</a></p>
    <p><b>Instagram</b><a href="https://instagram.com/dozejokitugas" target="_blank" rel="noopener">@dozejokitugas</a></p>
    <p><b>Area layanan</b>Seluruh Indonesia (online)</p>
  </div>
  <form id="fm">
    <input id="nm" placeholder="Nama" required><input id="kt" placeholder="Email / WhatsApp" required>
    <select id="jl" class="f"></select>
    <input id="bd" placeholder="Budget (opsional)"><input id="dl" placeholder="Deadline, mis. 20 Oktober">
    <textarea id="ds2" class="f" rows="4" placeholder="Deskripsi kebutuhan" required></textarea>
    <button class="btn f" type="submit">Kirim Permintaan</button>
    <div class="f" id="ok">Terima kasih! WhatsApp akan terbuka, kirim pesannya untuk melanjutkan. File pendukung bisa dikirim langsung lewat chat.</div>
  </form>
</div></section>
</main>

<footer><div class="w">
  <div class="cols">
    <div><div class="brand"><img class="lg" src="/logo.png" alt="DOZE Company"><span>DOZE Company</span></div><p style="opacity:.7;font-size:14px">Professional Academic &amp; Creative Services</p></div>
    <div><h4>Company</h4><ul><li><a href="#tentang">Tentang Kami</a></li><li><a href="#layanan">Layanan</a></li><li><a href="#portofolio">Portofolio</a></li><li><a href="#kontak">Kontak</a></li></ul></div>
    <div><h4>Academic</h4><ul><li>Pendampingan Skripsi</li><li>Makalah</li><li>Jurnal</li><li>Olah Data</li><li>PPT</li></ul></div>
    <div><h4>Creative</h4><ul><li>Poster</li><li>Banner</li><li>Logo</li><li>CV</li><li>Video Editing</li></ul></div>
    <div><h4>Connect</h4><ul><li><a href="https://wa.me/6281225112413">WhatsApp</a></li><li><a href="mailto:dozejokii@gmail.com">Email</a></li><li><a href="https://instagram.com/dozejokitugas" target="_blank" rel="noopener">Instagram</a></li></ul></div>
  </div>
  <small>© 2026 DOZE Company. All Rights Reserved.<br>DOZE Company menyediakan layanan profesional sesuai kebutuhan klien. Untuk layanan akademik, kami berfokus pada konsultasi, pendampingan, editing, formatting, research assistance, dan dukungan akademik yang bertanggung jawab.</small>
</div></footer>

<a class="wa" href="#" data-wa="Halo DOZE Company, saya ingin berkonsultasi mengenai layanan [jenis layanan]. Berikut kebutuhan saya: [deskripsi kebutuhan].">Chat with us</a>

<script>
const NO='6281225112413',$=i=>document.getElementById(i);
const AK=['Pendampingan Skripsi','Pendampingan Thesis','Makalah','Jurnal & Artikel','Paper','Esai','Laporan','Proposal','Olah Data','Modul Ajar Guru','Presentasi / PPT','Excel','Research Assistance','Editing & Formatting','Referencing / Sitasi'];
const DS=['Spanduk','Poster','Pamflet','Banner','Foto Produk','Video Editing','Feed Instagram','Logo','Web Graphic','Portofolio','CV','Company Profile','Social Media Design','Presentation Design','Branding'];
const chips=(a)=>a.map(x=>`<span>${x}</span>`).join('');
$('ak').innerHTML=chips(AK);$('ds').innerHTML=chips(DS);
const card=(t,p)=>`<div class="card"><h3>${t}</h3><p>${p}</p></div>`;
$('vals').innerHTML=[['Professional','Dikerjakan dengan standar profesional dan perhatian terhadap detail.'],['Creative','Solusi kreatif yang relevan dengan kebutuhan klien.'],['Reliable','Mengutamakan komunikasi, transparansi, dan ketepatan waktu.'],['Flexible','Melayani individu, akademik, organisasi, UMKM, hingga bisnis.']].map(x=>card(...x)).join('');
$('why').innerHTML=[['Quality First','Kami mengutamakan kualitas dalam setiap pekerjaan.'],['Professional Approach','Setiap project berdasarkan brief dan kebutuhan yang jelas.'],['Clear Communication','Komunikasi adalah bagian penting dari proses kerja.'],['On-Time','Penyelesaian sesuai timeline yang disepakati.'],['Confidential','Menjaga privasi dan kerahasiaan informasi klien.'],['One Professional Partner','Kebutuhan akademik, desain, dan digital dalam satu tempat.']].map(x=>card(...x)).join('');
const POP=[['Skripsi & Academic Assistance','Pendampingan, editing, dan formatting.'],['Olah Data','Analisis dan penyajian data penelitian.'],['Jurnal & Artikel','Penyusunan, editing, dan sitasi.'],['Presentation Design','Slide yang rapi dan komunikatif.'],['Social Media Design','Feed dan konten visual konsisten.'],['Logo & Branding','Identitas visual yang berkarakter.']];
$('pop').innerHTML=POP.map(([t,p])=>`<div class="card"><h3>${t}</h3><p>${p}</p><div class="ac"><a href="#layanan">Detail</a><a href="#" data-wa="Halo DOZE Company, saya ingin konsultasi layanan ${t}.">Konsultasi</a></div></div>`).join('');
const CATS=['All','Academic','Graphic Design','Branding','Social Media','Presentation','Digital'];
const ART={'Academic':`<svg viewBox="0 0 240 150" role="img" aria-label="Ilustrasi Academic"><rect width="240" height="150" fill="#dcebe3"/><rect x="70" y="12" width="100" height="130" rx="4" fill="#fff"/><rect x="82" y="26" width="60" height="7" fill="#17784f"/><g fill="#c5d3cc"><rect x="82" y="42" width="76" height="3"/><rect x="82" y="50" width="70" height="3"/><rect x="82" y="58" width="76" height="3"/><rect x="82" y="114" width="76" height="3"/><rect x="82" y="122" width="50" height="3"/></g><rect x="82" y="70" width="76" height="36" rx="2" fill="#eef5f1"/><g fill="#3fc08a"><rect x="88" y="94" width="10" height="8"/><rect x="104" y="86" width="10" height="16"/><rect x="120" y="78" width="10" height="24"/><rect x="136" y="88" width="10" height="14"/></g></svg>`,'Graphic Design':`<svg viewBox="0 0 240 150" role="img" aria-label="Ilustrasi Graphic Design"><rect width="240" height="150" fill="#dcebe3"/><rect x="78" y="10" width="84" height="130" rx="3" fill="#0a1814"/><circle cx="120" cy="56" r="26" fill="#17784f"/><circle cx="130" cy="48" r="14" fill="#3fc08a"/><rect x="92" y="94" width="56" height="8" fill="#fff"/><g fill="#94a59e"><rect x="92" y="108" width="40" height="4"/><rect x="92" y="118" width="48" height="4"/></g></svg>`,'Branding':`<svg viewBox="0 0 240 150" role="img" aria-label="Ilustrasi Branding"><rect width="240" height="150" fill="#dcebe3"/><rect x="40" y="20" width="160" height="76" rx="8" fill="#fff"/><path d="M120 30l22 10-22 10-22-10z" fill="#17784f"/><path d="M106 48v10q14 8 28 0V48" fill="none" stroke="#17784f" stroke-width="3"/><rect x="92" y="74" width="56" height="6" fill="#0a1814"/><circle cx="70" cy="122" r="12" fill="#0a1814"/><circle cx="104" cy="122" r="12" fill="#17784f"/><circle cx="138" cy="122" r="12" fill="#3fc08a"/><circle cx="172" cy="122" r="12" fill="#fff" stroke="#c5d3cc"/></svg>`,'Social Media':`<svg viewBox="0 0 240 150" role="img" aria-label="Ilustrasi Social Media"><rect width="240" height="150" fill="#dcebe3"/><rect x="70" y="8" width="100" height="134" rx="9" fill="#fff"/><g><rect x="78" y="20" width="26" height="26" fill="#17784f"/><rect x="107" y="20" width="26" height="26" fill="#0a1814"/><rect x="136" y="20" width="26" height="26" fill="#3fc08a"/><rect x="78" y="49" width="26" height="26" fill="#0a1814"/><rect x="107" y="49" width="26" height="26" fill="#3fc08a"/><rect x="136" y="49" width="26" height="26" fill="#17784f"/><rect x="78" y="78" width="26" height="26" fill="#3fc08a"/><rect x="107" y="78" width="26" height="26" fill="#17784f"/><rect x="136" y="78" width="26" height="26" fill="#0a1814"/></g><g fill="#c5d3cc"><rect x="78" y="114" width="60" height="4"/><rect x="78" y="124" width="40" height="4"/></g></svg>`,'Presentation':`<svg viewBox="0 0 240 150" role="img" aria-label="Ilustrasi Presentation"><rect width="240" height="150" fill="#dcebe3"/><rect x="30" y="18" width="180" height="104" rx="4" fill="#0a1814"/><rect x="44" y="34" width="70" height="8" fill="#3fc08a"/><g fill="#fff"><rect x="44" y="52" width="86" height="5"/><rect x="44" y="64" width="66" height="5"/></g><g fill="#17784f"><rect x="146" y="88" width="12" height="20"/><rect x="164" y="76" width="12" height="32"/></g><rect x="182" y="62" width="12" height="46" fill="#3fc08a"/><rect x="112" y="122" width="16" height="12" fill="#b5c4bd"/><rect x="92" y="134" width="56" height="4" rx="2" fill="#b5c4bd"/></svg>`,'Digital':`<svg viewBox="0 0 240 150" role="img" aria-label="Ilustrasi Digital"><rect width="240" height="150" fill="#dcebe3"/><rect x="25" y="12" width="190" height="126" rx="6" fill="#fff"/><rect x="25" y="12" width="190" height="14" rx="6" fill="#0a1814"/><g fill="#eef5f1"><rect x="35" y="36" width="52" height="26" rx="3"/><rect x="94" y="36" width="52" height="26" rx="3"/><rect x="153" y="36" width="52" height="26" rx="3"/></g><g fill="#3fc08a"><rect x="40" y="108" width="14" height="20"/><rect x="62" y="96" width="14" height="32"/><rect x="84" y="102" width="14" height="26"/><rect x="106" y="84" width="14" height="44"/></g><polyline points="140,120 160,100 180,108 200,78" fill="none" stroke="#17784f" stroke-width="3"/></svg>`};
const PF=[['Academic','Contoh Proyek Akademik'],['Graphic Design','Contoh Poster'],['Branding','Contoh Logo & Branding'],['Social Media','Contoh Feed Instagram'],['Presentation','Contoh Presentasi'],['Digital','Contoh Olah Data']];
function pf(c){$('pfg').innerHTML=PF.filter(x=>c==='All'||x[0]===c).map(x=>`<div class="card"><div class="pf">${ART[x[0]]}</div><h3>${x[1]}</h3><p>Placeholder portofolio</p></div>`).join('');
 [...$('pff').children].forEach(b=>b.classList.toggle('on',b.textContent===c))}
$('pff').innerHTML=CATS.map(c=>`<button>${c}</button>`).join('');
$('pff').onclick=e=>{if(e.target.tagName==='BUTTON')pf(e.target.textContent)};pf('All');
$('fq').innerHTML=[['Apa saja layanan yang tersedia?','DOZE Company menyediakan layanan akademik, desain, kreatif, digital, dan berbagai kebutuhan profesional lainnya.'],['Apakah bisa request layanan di luar daftar?','Ya. Hubungi kami untuk mendiskusikan kebutuhan khusus.'],['Bagaimana cara melakukan pemesanan?','Hubungi admin melalui WhatsApp, jelaskan kebutuhan Anda, lalu kami bantu proses konsultasi dan estimasi.'],['Apakah bisa revisi?','Ketentuan revisi disesuaikan dengan jenis layanan dan kesepakatan project.'],['Berapa lama pengerjaan?','Timeline bergantung pada jenis dan kompleksitas pekerjaan.'],['Apakah data klien aman?','Kami mengutamakan privasi dan kerahasiaan informasi yang diberikan klien.'],['Apakah bisa konsultasi terlebih dahulu?','Ya. Anda dapat berkonsultasi sebelum menentukan layanan.']].map(([q,a])=>`<details><summary>${q}</summary><p>${a}</p></details>`).join('');
$('jl').innerHTML='<option value="">Jenis layanan</option>'+['Akademik','Desain & Kreatif','Olah Data / Excel','Presentasi','Lainnya'].map(x=>`<option>${x}</option>`).join('');
const wa=t=>'https://wa.me/'+NO+'?text='+encodeURIComponent(t);
document.addEventListener('click',e=>{const a=e.target.closest('[data-wa]');if(a){e.preventDefault();window.open(wa(a.dataset.wa),'_blank','noopener')}});
$('fm').onsubmit=e=>{e.preventDefault();
 const m=`Halo DOZE Company, saya ${$('nm').value} (${$('kt').value}). Saya ingin berkonsultasi mengenai layanan ${$('jl').value||'-'}. Budget: ${$('bd').value||'-'}. Deadline: ${$('dl').value||'-'}. Kebutuhan saya: ${$('ds2').value}`;
 fetch('/kirim',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({nama:$('nm').value,kontak:$('kt').value,layanan:$('jl').value,budget:$('bd').value,deadline:$('dl').value,kebutuhan:$('ds2').value})}).catch(()=>{});
 $('ok').style.display='block';window.open(wa(m),'_blank','noopener')};
$('bg').onclick=()=>$('nv').classList.toggle('open');
$('nv').onclick=()=>$('nv').classList.remove('open');
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.08});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
</script>
</body>
</html>
'''


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
