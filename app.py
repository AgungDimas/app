from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# ==========================================
# INI ADALAH BAGIAN FRONTEND (UI) - HTML & CSS
# ==========================================
TAMPILAN_UI = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>AI Wawancara R&D</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1); width: 400px; margin: auto; }
        input { padding: 10px; width: 80%; margin-bottom: 15px; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        #hasil { margin-top: 20px; font-weight: bold; font-size: 1.2em; color: #333; }
    </style>
</head>
<body>

    <div class="card">
        <h2>🤖 AI Interview by BungDimas</h2>
        <p>Masukkan nama untuk tes wawancara</p>
        
        <input type="text" id="inputNama" placeholder="Ketik nama kandidat...">
        <br>
        <button onclick="mintaSkorKeBackend()">Minta Penilaian AI</button>

        <div id="hasil"></div>
    </div>

    <!-- INI JAVASCRIPT UNTUK MENGHUBUNGKAN UI KE API BACKEND -->
    <script>
        function mintaSkorKeBackend() {
            // 1. Ambil nama dari kotak input
            let namaKandidat = document.getElementById("inputNama").value;
            let divHasil = document.getElementById("hasil");
            
            divHasil.innerHTML = "Memproses...";

            // 2. Tembak API Backend (Sama seperti CURL/Postman tadi)
            fetch('/api/score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nama_kandidat: namaKandidat })
            })
            .then(response => response.json()) // Tunggu balasan server
            .then(data => {
                // 3. Tampilkan data dari Backend ke layar UI
                let warna = data.status === "Lolos" ? "green" : "red";
                divHasil.innerHTML = `
                    <hr>
                    <p>Kandidat: <b>${data.kandidat}</b></p>
                    <p>Skor AI: <span style="color: ${warna}; font-size: 1.5em;">${data.skor_wawancara}</span></p>
                    <p>Status: <b style="color: ${warna};">${data.status}</b></p>
                `;
            });
        }
    </script>

</body>
</html>
"""

# ==========================================
# INI ADALAH BAGIAN BACKEND (API / ROUTE)
# ==========================================

# Route GET: Sekarang tidak membalas JSON, tapi menampilkan halaman Web (UI)
@app.route('/', methods=['GET'])
def home():
    return render_template_string(TAMPILAN_UI)

# Route POST: Tetap sama seperti punya Anda sebelumnya (Mesin Penilai)
@app.route('/api/score', methods=['POST'])
def score_candidate():
    data = request.get_json()
    nama = data.get("nama_kandidat", "Anonim")
    skor_ai = random.randint(60, 100)
    
    return jsonify({
        "kandidat": nama,
        "skor_wawancara": skor_ai,
        "status": "Lolos" if skor_ai >= 80 else "Gagal",
        "catatan": "Diproses oleh Flask API"
    })

if __name__ == '__main__':
    app.run(debug=True)