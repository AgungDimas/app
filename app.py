from flask import Flask, request, jsonify
import random # Untuk membuat skor acak

# 1. Menyiapkan aplikasi Flask
app = Flask(__name__)

# 2. Membuat Route GET (Hanya untuk ngecek API hidup atau mati)
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Halo! API sudah berjalan BungDimas"
    })

# 3. Membuat Route POST (Menerima data kandidat, membalas dengan skor)
@app.route('/api/score', methods=['POST'])
def score_candidate():
    # Mengambil data JSON yang dikirim oleh Postman/User
    data = request.get_json()
    
    # Mengambil nama kandidat dari data
    nama = data.get("nama_kandidat", "Anonim")
    
    # Membuat skor AI bohongan (acak dari 70 sampai 100)
    skor_ai = random.randint(70, 100)
    
    # Server membalas (Return) dalam bentuk JSON
    return jsonify({
        "kandidat": nama,
        "skor_wawancara": skor_ai,
        "status": "Lolos" if skor_ai >= 80 else "Gagal",
        "catatan": "Diproses oleh Flask API"
    })

# 4. Menjalankan Server
if __name__ == '__main__':
    # debug=True artinya server akan otomatis refresh kalau kode diubah
    app.run(debug=True)