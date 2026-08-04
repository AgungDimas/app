from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# 1. FRONTEND (UI) - Multi-Step & Modern Design
# ==========================================
TAMPILAN_UI = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tech Assessment</title>
    <style>
        /* Desain UI Modern ala Startup */
        body { font-family: 'Inter', 'Segoe UI', sans-serif; background-color: #f0f4f8; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: #333; }
        .card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); width: 100%; max-width: 600px; display: none; transition: all 0.3s ease; }
        .card.active { display: block; animation: fadeIn 0.5s; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        h1, h2 { color: #102a43; margin-top: 0; }
        h1 { font-size: 24px; border-bottom: 2px solid #3e82f7; padding-bottom: 15px; text-align: center; }
        
        .form-group { margin-bottom: 20px; }
        label { font-weight: 600; font-size: 14px; color: #486581; display: block; margin-bottom: 8px; }
        input[type="text"], textarea { width: 100%; padding: 12px; border: 1px solid #d9e2ec; border-radius: 8px; font-family: inherit; font-size: 14px; box-sizing: border-box; transition: border 0.3s; }
        input[type="text"]:focus, textarea:focus { outline: none; border-color: #3e82f7; box-shadow: 0 0 0 3px rgba(62, 130, 247, 0.1); }
        textarea { resize: vertical; height: 80px; }
        
        .btn { width: 100%; padding: 14px; background-color: #3e82f7; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.3s; margin-top: 10px; }
        .btn:hover { background-color: #265cb3; }
        .btn-outline { background-color: white; color: #3e82f7; border: 1px solid #3e82f7; margin-top: 15px; }
        .btn-outline:hover { background-color: #f0f4f8; }

        .result-header { text-align: center; margin-bottom: 20px; }
        .score-circle { width: 120px; height: 120px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 36px; font-weight: bold; color: white; margin: 0 auto 15px auto; }
        .feedback-item { background: #f8f9fa; padding: 15px; border-left: 4px solid #3e82f7; border-radius: 4px; margin-bottom: 10px; font-size: 14px; }
        
        .badge { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; background: #e0e7ff; color: #3730a3; margin-left: 10px; }
    </style>
</head>
<body>

    <!-- TAHAP 1: SCREEN WELCOME & INPUT NAMA -->
    <div id="step1" class="card active">
        <h1>🚀 Portal AI Tech Assessment</h1>
        <p style="text-align: center; color: #627d98; margin-bottom: 30px;">Selamat datang! Silakan masukkan identitas Anda sebelum memulai tes berbasis AI.</p>
        <div class="form-group">
            <label>Nama Lengkap:</label>
            <input type="text" id="inputNama" placeholder="Ketik nama Anda di sini..." autocomplete="off">
        </div>
        <button class="btn" onclick="mulaiTes()">Mulai Kerjakan Soal ➔</button>
    </div>

    <!-- TAHAP 2: SCREEN SOAL -->
    <div id="step2" class="card">
        <h1>📝 Soal Teknis (5 Soal)</h1>
        <p style="font-size: 14px; color: #627d98;">Kandidat: <b id="displayNama"></b></p>
        
        <div class="form-group">
            <label>1. Apa kepanjangan dari API?</label>
            <input type="text" id="j1" placeholder="Jawaban singkat...">
        </div>
        <div class="form-group">
            <label>2. Sebutkan minimal 2 bahasa pemrograman untuk Backend!</label>
            <input type="text" id="j2" placeholder="Contoh: Java...">
        </div>
        <div class="form-group">
            <label>3. Apa perintah Git untuk mengirim kode ke GitHub (remote repository)?</label>
            <input type="text" id="j3" placeholder="Contoh: git...">
        </div>
        <div class="form-group">
            <label>4. Dalam database SQL, perintah apa yang dipakai untuk mengambil/menampilkan data?</label>
            <input type="text" id="j4" placeholder="Ketik perintah dasarnya saja...">
        </div>
        <div class="form-group">
            <label>5. Flask dan Django adalah framework web yang menggunakan bahasa pemrograman apa?</label>
            <input type="text" id="j5" placeholder="...">
        </div>

        <button class="btn" id="btnSubmit" onclick="kirimJawaban()">Kirim Jawaban</button>
    </div>

    <!-- TAHAP 3: SCREEN HASIL & EVALUASI -->
    <div id="step3" class="card">
        <div class="result-header">
            <h2 id="hasil-status"></h2>
            <div id="score-circle" class="score-circle">100</div>
            <p>Terima kasih <b><span id="hasil-nama"></span></b>. Berikut adalah evaluasi otomatis dari AI API kami:</p>
        </div>
        
        <div id="feedback-container"></div>

        <button class="btn btn-outline" onclick="location.reload()">Selesai & Kembali ke Awal</button>
    </div>

    <!-- JAVASCRIPT: Logika UI dan Komunikasi API -->
    <script>
        let namaKandidat = "";

        // Fungsi Pindah dari Tahap 1 ke Tahap 2
        function mulaiTes() {
            namaKandidat = document.getElementById("inputNama").value.trim();
            if(namaKandidat === "") {
                alert("Mohon isi nama Anda terlebih dahulu!");
                return;
            }
            document.getElementById("displayNama").innerText = namaKandidat;
            document.getElementById("step1").classList.remove("active");
            document.getElementById("step2").classList.add("active");
        }

        // Fungsi Tembak API dan Pindah ke Tahap 3
        function kirimJawaban() {
            let btn = document.getElementById("btnSubmit");
            btn.innerText = "Memproses Analisis AI...";
            btn.style.opacity = "0.7";
            btn.disabled = true;

            // Kumpulkan jawaban
            let payload = {
                nama_kandidat: namaKandidat,
                jawaban1: document.getElementById("j1").value,
                jawaban2: document.getElementById("j2").value,
                jawaban3: document.getElementById("j3").value,
                jawaban4: document.getElementById("j4").value,
                jawaban5: document.getElementById("j5").value
            };

            // Tembak API
            fetch('/api/submit_test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(response => response.json())
            .then(data => {
                // Sembunyikan Tahap 2, Munculkan Tahap 3
                document.getElementById("step2").classList.remove("active");
                document.getElementById("step3").classList.add("active");

                // Render Hasil
                document.getElementById("hasil-nama").innerText = data.kandidat;
                
                let scoreCircle = document.getElementById("score-circle");
                scoreCircle.innerText = data.skor_akhir;
                
                let statusHeader = document.getElementById("hasil-status");
                statusHeader.innerText = data.status;

                // Atur warna berdasarkan skor
                let warna = data.skor_akhir >= 80 ? "#27ae60" : (data.skor_akhir >= 60 ? "#f39c12" : "#e74c3c");
                scoreCircle.style.backgroundColor = warna;
                statusHeader.style.color = warna;

                // Render Feedback Soal
                let fbContainer = document.getElementById("feedback-container");
                fbContainer.innerHTML = ""; // Bersihkan dulu
                
                data.evaluasi_detail.forEach((item, index) => {
                    let badgeWarna = item.poin === 20 ? "#e0e7ff" : "#ffe3e3";
                    let badgeTeksWarna = item.poin === 20 ? "#3730a3" : "#c92a2a";
                    fbContainer.innerHTML += `
                        <div class="feedback-item" style="border-color: ${warna}">
                            <b>Soal ${index + 1}:</b> ${item.komentar} 
                            <span class="badge" style="background: ${badgeWarna}; color: ${badgeTeksWarna};">+${item.poin} Poin</span>
                        </div>
                    `;
                });
            });
        }
    </script>
</body>
</html>
"""

# ==========================================
# 2. BACKEND (API) - Mesin Penilai 5 Soal
# ==========================================

@app.route('/', methods=['GET'])
def home():
    return render_template_string(TAMPILAN_UI)

@app.route('/api/submit_test', methods=['POST'])
def evaluate_test():
    data = request.get_json()
    nama = data.get("nama_kandidat", "Anonim")
    
    # Ambil 5 Jawaban
    j = [
        data.get("jawaban1", "").lower(),
        data.get("jawaban2", "").lower(),
        data.get("jawaban3", "").lower(),
        data.get("jawaban4", "").lower(),
        data.get("jawaban5", "").lower()
    ]

    total_skor = 0
    evaluasi = []

    # Fungsi pembantu untuk menilai per soal
    def beri_nilai(soal_ke, kondisi_benar, komentar_benar, komentar_salah):
        nonlocal total_skor
        if kondisi_benar:
            total_skor += 20
            evaluasi.append({"poin": 20, "komentar": komentar_benar})
        else:
            evaluasi.append({"poin": 0, "komentar": komentar_salah})

    # Evaluasi Soal 1: API
    beri_nilai(1, "application programming interface" in j[0], 
               "Tepat sekali! Itu kepanjangan dari API.", 
               "Salah. Jawabannya adalah 'Application Programming Interface'.")

    # Evaluasi Soal 2: Bahasa Backend (Min 2)
    bahasa_backend = ["python", "java", "php", "javascript", "node", "go", "ruby", "c#", "golang"]
    ditemukan = [lang for lang in bahasa_backend if lang in j[1]]
    beri_nilai(2, len(ditemukan) >= 2, 
               f"Hebat! Kamu paham. ({', '.join(ditemukan)})", 
               "Kurang tepat. Kamu harus menyebutkan minimal 2 bahasa seperti Python, Java, atau PHP.")

    # Evaluasi Soal 3: Git
    beri_nilai(3, "git push" in j[2], 
               "Benar! 'git push' dipakai untuk mengunggah kode.", 
               "Salah. Perintah yang benar adalah 'git push'.")

    # Evaluasi Soal 4: SQL
    beri_nilai(4, "select" in j[3], 
               "Sempurna. Perintah SELECT digunakan untuk mengambil data.", 
               "Salah. Untuk mengambil data di SQL kita menggunakan perintah SELECT.")

    # Evaluasi Soal 5: Flask/Django
    beri_nilai(5, "python" in j[4], 
               "Benar sekali! Keduanya berbasis Python.", 
               "Salah. Flask dan Django ditulis menggunakan bahasa Python.")

    # Status Kelulusan
    if total_skor >= 80:
        status = "🌟 Lulus (Excellent)"
    elif total_skor >= 60:
        status = "👍 Dipertimbangkan (Average)"
    else:
        status = "❌ Gagal (Below Standard)"

    return jsonify({
        "kandidat": nama,
        "skor_akhir": total_skor,
        "status": status,
        "evaluasi_detail": evaluasi
    })

if __name__ == '__main__':
    app.run(debug=True)