import streamlit as st
from datetime import datetime
import json

class EmotionMeasurementSystem:
    def __init__(self):
        self.emotion_scale = {
            1: "Sangat Tenang/Bahagia",
            2: "Tenang",
            3: "Santai",
            4: "Netral",
            5: "Sedikit Cemas",
            6: "Cemas",
            7: "Sangat Cemas",
            8: "Stres",
            9: "Sangat Stres",
            10: "Ekstrem Stres"
        }
        self.history = []

    def calculate_final_score(self, measurements):
        weights = [0.4, 0.3, 0.3]  # Bobot untuk setiap jenis pengukuran
        return sum(m * w for m, w in zip(measurements, weights))

    def get_emotion_description(self, score):
        rounded_score = round(score)
        return self.emotion_scale.get(rounded_score, "Tidak dapat menentukan emosi")

    def save_measurement(self, score, description):
        self.history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'score': score,
            'description': description
        })

    def get_history(self):
        return self.history

system = EmotionMeasurementSystem()

st.title("Sistem Pengukuran Emosi")
st.write("Aplikasi ini membantu Anda mengukur tingkat emosi Anda saat ini.")

# Pengukuran Verbal
st.header("1. Penilaian Verbal")
verbal_questions = [
    "Seberapa tenang atau gelisah perasaan Anda saat ini? (1-10)",
    "Seberapa mudah Anda berkonsentrasi saat ini? (1-10)",
    "Bagaimana tingkat energi Anda saat ini? (1-10)",
    "Seberapa nyaman Anda dengan lingkungan sekitar? (1-10)",
    "Bagaimana kualitas tidur Anda tadi malam? (1-10)"
]
verbal_scores = []
weights = [0.3, 0.2, 0.2, 0.15, 0.15]

for question in verbal_questions:
    score = st.slider(question, 1, 10, 5)
    verbal_scores.append(score)

verbal_result = sum(v * w for v, w in zip(verbal_scores, weights))

# Checklist Perilaku
st.header("2. Checklist Perilaku")
behavioral_items = [
    "Gelisah atau tidak bisa diam",
    "Sulit berkonsentrasi",
    "Ketegangan otot",
    "Perubahan nafsu makan",
    "Perubahan pola tidur",
    "Mudah tersinggung",
    "Keringat berlebih",
    "Jantung berdebar",
    "Tangan gemetar",
    "Nafas pendek"
]
behavioral_responses = []
for item in behavioral_items:
    response = st.checkbox(item)
    behavioral_responses.append(response)

behavioral_score = (sum(behavioral_responses) / len(behavioral_items)) * 10

# Gejala Fisik
st.header("3. Gejala Fisik")
physical_symptoms = [
    "Sakit kepala",
    "Ketegangan otot",
    "Kelelahan",
    "Masalah pencernaan",
    "Kesulitan tidur"
]
physical_scores = []
for symptom in physical_symptoms:
    score = st.radio(symptom, [0, 1, 2, 3], index=0, horizontal=True)
    physical_scores.append(score)

physical_result = (sum(physical_scores) / (len(physical_symptoms) * 3)) * 10

# Hasil Pengukuran
if st.button("Lihat Hasil"):
    final_score = system.calculate_final_score([verbal_result, behavioral_score, physical_result])
    emotion_desc = system.get_emotion_description(final_score)
    system.save_measurement(final_score, emotion_desc)

    st.subheader("Hasil Pengukuran Anda")
    st.write(f"**Skor Anda:** {final_score:.1f}/10")
    st.write(f"**Status Emosi:** {emotion_desc}")
    
    if final_score > 7:
        st.warning("⚠️ Rekomendasi: Lakukan teknik relaksasi dan pertimbangkan konsultasi profesional.")
    elif final_score > 4:
        st.info("💡 Rekomendasi: Luangkan waktu untuk istirahat dan lakukan aktivitas menenangkan.")
    else:
        st.success("🌟 Rekomendasi: Pertahankan kondisi positif ini!")

# Riwayat Pengukuran
if st.button("Tampilkan Riwayat"):
    history = system.get_history()
    if history:
        st.write("### Riwayat Pengukuran")
        for record in history:
            st.write(f"- {record['timestamp']}: Skor {record['score']:.1f} - {record['description']}")
    else:
        st.write("Belum ada riwayat pengukuran.")
