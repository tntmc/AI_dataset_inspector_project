def build_dataset_quality_prompt(reasoning_result, retrieve_context: str = "") -> str:

    # insights = "\n".join(f"- {i}" for i in reasoning_result.insights)
    # recs = "\n".join(f"- {r}" for r in reasoning_result.recommendations)

    # Cek apakah input berupa dictionary atau object class agar kode lebih robust
    if isinstance(reasoning_result, dict):
        insights_list = reasoning_result.get("insights", [])
        recs_list = reasoning_result.get("recommendations", [])
        risk_val = reasoning_result.get("risk_levels", reasoning_result.get("risk_levels", "Unknown"))
    else:
        insights_list = reasoning_result.insights
        recs_list = reasoning_result.recommendations
        risk_val = reasoning_result.risk_levels

    insights = "\n".join(f"- {index}" for index in insights_list)
    recs = "\n".join(f"- {recommendation}" for recommendation in recs_list)

    recs = "\n".join(f"- {recommendation}" for recommendation in recs_list)

    return f"""
  Anda adalah Senior Data Scientist dan Quality Assurance Specialist.
  Tugas Anda adalah memberikan penjelasan yang mendalam dan edukatif mengenai kualitas dataset pengguna, bukan sekadar jawaban singkat.

  KONTEKS DATASET:
  - Risk Level: {risk_val}

  TEMUAN MASALAH (INSIGHTS):
  {insights}

  REKOMENDASI PERBAIKAN:
  {recs}

  INFORMASI TAMBAHAN (RAG):
  {retrieve_context}

  PANDUAN MENJAWAB:
  1. **Analisis Dampak**: Jelaskan mengapa masalah yang ditemukan (misal: missing values, duplikasi) berbahaya bagi analisis atau model machine learning.
  2. **Solusi Teknis**: Berikan saran konkret cara memperbaikinya. Jika relevan, sebutkan metode Pandas/Python (contoh: `.fillna()`, `.drop_duplicates()`).
  3. **Edukasi**: Gunakan bahasa yang profesional namun mudah dimengerti untuk mengedukasi pengguna.
  4. **Jangan Malas**: Hindari jawaban satu kalimat. Uraikan penjelasan Anda secara rinci.
  5. **Fakta**: Hanya gunakan informasi dari konteks di atas. Jangan mengarang kolom atau data yang tidak ada.

  Jawablah pertanyaan pengguna berikut ini dengan detail berdasarkan panduan di atas:
  """

  #   return f"""
