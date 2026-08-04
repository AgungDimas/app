from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ==========================================
# 1. FRONTEND (UI) - Tampilan Tes Wawancara
# ==========================================
TAMPILAN_UI = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>AI Interview Test</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #e9ecef; display: flex; justify-content: center; padding: 20px; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 500px; }
        h2 { color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px;}
        .form-group { margin-bottom: 15px; }
        label { font-weight: bold; color: #34495e; display: block; margin-bottom: 5px; }
        input[type="text"], textarea { width: 100%; padding: 10px; border: 1px solid #bdc3c7; border-radius: 6px; box-sizing: border-box; }
        textarea { resize: vertical; height: 80px; }
        button { width: 100%; padding: 12px; background-color: #3498db; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background-color: #2980b9; }
        #hasil-box { margin-top: 25px; padding: 15px; border-radius: 6px; display: none; text-align: center; }
        .feedback-list { text-align: left; font-size: 14px; margin-top: 10px; background: #f8f9fa; padding: 10px; border-radius: 5px;}
    </style>
</head>
<body>

    <div class="container">
        <h2>💻 Tech Interview Test</h2>
        
        <div class="form-group">
            <label>Nama Kandidat:</label>
            <input type="text" id="inputNama" placeholder="Masukkan nama Anda">
        </div>

        <div class="form-group">
            <label>Soal 1: Apa kepanjangan dari API?</label>
            <textarea id="jawaban1" placeholder="Ketik jawaban Anda di sini..."></textarea>
        </div>

        <div class="form-group">
            <label>Soal 2: Sebutkan minimal 2 bahasa pemrograman untuk Backend!</label>
            <textarea id="jawaban2" placeholder="Contoh: HTML, CSS (Itu frontend ya, jangan dijawab itu)"></textarea>
        </div>

        <button onclick="kirimJawaban()">Kirim Jawaban ke AI</button>

        <div id="hasil-box">
            <h3 id="hasil-nama"></h3>
            <h1 id="hasil-skor"></h1>
            <h3 id="hasil-status"></h3>
            <div class="feedback-list" id="hasil-feedback"></div>
        </div>
    </div>

    <!-- JAVASCRIPT: Mengirim jawaban ke API Backend -->
    <script>
        function kirimJawaban() {
            let nama = document.getElementById("inputNama").value;
            let j1 = document.getElementById("jawaban1").value;
            let j2 = document.getElementById("jawaban2").value;
            
            let btn = document.querySelector("button");
            btn.innerText = "Mengevaluasi... Tunggu sebentar";
            btn.disabled = true;

            // Tembak API Backend
            fetch('/api/submit_test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nama_kandidat: nama, jawaban1: j1, jawaban2: j2 })
            })
            .then(response => response.json())
            .then(data => {
                // Tampilkan Hasil
                document.getElementById("hasil-box").style.display = "block";
                
                let warna = data.skor_akhir >= 80 ? "#27ae60" : "#e74c3c";
                document.getElementById("hasil-box").style.border = `2px solid ${warna}`;
                
                document.getElementById("hasil-nama").innerText = `Kandidat: ${data.kandidat}`;
                document.getElementById("hasil-skor").innerText = `Skor: ${data.skor_akhir} / 100`;
                document.getElementById("hasil-skor").style.color = warna;
                document.getElementById("hasil-status").innerText = `Status: ${data.status}`;
                document.getElementById("hasil-status").style.color = warna;
                
                // Menampilkan evaluasi per soal
                document.getElementById("hasil-feedback").innerHTML = 
                    `<b>Evaluasi AI:</b><br> 👉 ${data.feedback_soal1} <br><br> 👉 ${data.feedback_soal2}`;

                // Kembalikan tombol
                btn.innerText = "Kirim Jawaban ke AI";
                btn.disabled = false;
            });
        }
    </script>
</body>
</html>
"""

# ==========================================
# 2. BACKEND (API) - Otak Penilai (Rules Engine)
# ==========================================

@app.route('/', methods=['GET'])
def home():
    return render_template_string(TAMPILAN_UI)

@app.route('/api/submit_test', methods=['POST'])
def evaluate_test():
    data = request.get_json()
    nama = data.get("nama_kandidat", "Anonim")
    
    # Ambil jawaban dan ubah jadi huruf kecil semua untuk memudahkan pengecekan
    j1 = data.get("jawaban1", "").lower()
    j2 = data.get("jawaban2", "").lower()

    skor = 0
    feedback1 = ""
    feedback2 = ""

    # --- LOGIKA SOAL 1 (Nilai maks: 50) ---
    if "application programming interface" in j1:
        skor += 50
        feedback1 = "Soal 1: Sempurna! (+50 poin)"
    else:
        feedback1 = "Soal 1: Salah. Kunci jawaban adalah 'Application Programming Interface'."

    # --- LOGIKA SOAL 2 (Nilai maks: 50) ---
    bahasa_backend = ["python", "java", "php", "javascript", "node", "go", "ruby", "c#", "golang"]
    
    # Hitung berapa bahasa backend yang dia sebutkan
    bahasa_ditemukan = [lang for lang in bahasa_backend if lang in j2]
    
    if len(bahasa_ditemukan) >= 2:
        skor += 50
        feedback2 = f"Soal 2: Hebat! Kamu menyebutkan {', '.join(bahasa_ditemukan)} (+50 poin)"
    elif len(bahasa_ditemukan) == 1:
        skor += 25
        feedback2 = f"Soal 2: Kurang lengkap. Kamu hanya menyebutkan {bahasa_ditemukan[0]} (+25 poin)"
    else:
        feedback2 = "Soal 2: Salah. Jawaban tidak mengandung bahasa backend yang valid."

    # --- PENENTUAN STATUS ---
    status = "Lulus Tahap 1" if skor >= 75 else "Gagal / Belum Memenuhi Standar"

    # --- KEMBALIKAN DATA KE UI ---
    return jsonify({
        "kandidat": nama,
        "skor_akhir": skor,
        "status": status,
        "feedback_soal1": feedback1,
        "feedback_soal2": feedback2
    })

if __name__ == '__main__':
    app.run(debug=True)