import datetime
import streamlit as st
import sparql_client
from services.ai_client import decode_user_input_to_skills


def extract_skills_from_text(text, skill_keyword_map):
    normalized = text.lower()
    found = []
    for phrase, skill in skill_keyword_map.items():
        if phrase in normalized and skill not in found:
            found.append(skill)
    return found


def render_user_view(theme, skill_keyword_map, skill_options):
    st.markdown(
        f"""
        <div style="border-radius: 26px; padding: 30px; background: {theme['card']}; box-shadow: {theme['shadow']}; margin-bottom: 24px; border: 1px solid {theme['border']};">
            <div style="display: flex; flex-wrap: wrap; gap: 28px; justify-content: space-between; align-items: flex-start;">
                <div style="max-width: 720px;">
                    <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.22em; color: {theme['muted']}; margin-bottom: 12px;">SkillMap Studio</div>
                    <h1 style="margin: 0; font-family: 'Fraunces', serif; font-size: 2.8rem; line-height: 1.06; color: {theme['text']};">Peta Karier, Versi Kamu</h1>
                    <p style="margin-top: 16px; font-size: 1.02rem; color: {theme['muted']}; max-width: 680px;">Tulis skill dan minatmu dengan bahasa sehari-hari. Sistem ini mencari kecocokan dari graf semantik supaya rekomendasi terasa nyambung, bukan sekadar cocok kata.</p>
                </div>
                <div style="min-width: 220px; display: grid; gap: 14px;">
                    <div style="background: {theme['panel']}; padding: 20px; border-radius: 18px; border: 1px solid {theme['border']}; transform: rotate(-1deg);">
                        <div style="font-size: 0.85rem; color: {theme['muted']}; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 8px;">Catatan kecil</div>
                        <div style="font-size: 1.05rem; color: {theme['text']}; font-weight: 600; margin-bottom: 8px;">Campur hard + soft skill</div>
                        <div style="color: {theme['muted']}; line-height: 1.6;">Misalnya Python + Communication, atau Figma + User Research.</div>
                    </div>
                    <div style="background: #fff1c7; padding: 16px; border-radius: 14px; border: 1px solid #efd9a8; box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08); transform: rotate(1.8deg);">
                        <div style="font-size: 0.85rem; color: #7c5b1c; font-weight: 600;">Note dari admin</div>
                        <div style="margin-top: 6px; color: #8a6a28;">Tambahkan role baru kalau skill baru sudah disiapkan.</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.8, 1.2], gap="large")

    with left:
        st.markdown("### 1. Beri tahu Skill dan Minatmu")
        with st.form(key="skill_form"):
            selected_skills = st.multiselect(
                "Pilih skill populer (opsional)",
                skill_options,
                help="Gunakan skill populer sebagai shortcut jika kamu ingin cepat memulai.",
            )
            user_input = st.text_area(
                "Tuliskan skill, pengalaman, atau minatmu",
                placeholder="Contoh: Aku mahir Python, suka membuat dashboard, dan tertarik ke product management.",
                height=150,
            )
            # Add toggle for OR/AND logic
            search_mode = st.radio(
                "Mode pencarian:",
                options=["Toleran", "Ketat"],
                index=1,  # Default to Ketat (AND)
                help="Toleran: Job hanya perlu memiliki salah satu skill. Ketat: Job harus memiliki semua skill yang dipilih.",
            )
            submit_button = st.form_submit_button("Cari Jobs")

    with right:
        st.markdown("### Cara kerja aplikasi")
        st.markdown(
            f"""
            <div style='padding: 18px; border-radius: 20px; background: {theme['card']}; box-shadow: 0 12px 34px rgba(15, 23, 42, 0.08); border: 1px solid {theme['border']}'>
                <ul style='margin: 0; padding-left: 18px; color: {theme['muted']}; line-height: 1.8;'>
                    <li><strong>1.</strong> Pilih skill populer atau tuliskan skill sendiri.</li>
                    <li><strong>2.</strong> Sistem menghubungkan skill dengan career role di graf semantik.</li>
                    <li><strong>3.</strong> Dapatkan rekomendasi peran yang sesuai, dengan konteks skill + industry.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if submit_button:
        st.divider()
        with st.spinner("Mencari jobs..."):
            extracted_skills = extract_skills_from_text(user_input or "", skill_keyword_map)
            for skill in selected_skills:
                if skill not in extracted_skills:
                    extracted_skills.append(skill)

            if user_input and user_input.strip():
                try:
                    decoded_skills = decode_user_input_to_skills(user_input, skill_keyword_map)
                    for skill in decoded_skills:
                        if skill not in extracted_skills:
                            extracted_skills.append(skill)
                except Exception as exc:
                    st.info("AI decoding tidak tersedia: " + str(exc))

        if extracted_skills:
            st.markdown(
                f"<div style='padding:18px; border-radius:20px; background:{theme['card']}; box-shadow:{theme['shadow']}; margin-bottom:18px; border: 1px solid {theme['border']}'>"
                + f"<h2 style='margin:0 0 10px; color:{theme['text']};'>Skill terdeteksi</h2>"
                + f"<p style='margin:0; color:{theme['muted']};'>Kami menemukan skill berikut dari inputmu: <strong>{', '.join(extracted_skills)}</strong>.</p>"
                + "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.warning(
                "Skill tidak terdeteksi dari input. Coba tambahkan kata kunci seperti Python, Excel, React, atau Figma agar pencarian lebih akurat."
            )

        st.subheader("2. Hasil Matching Jobs")
        try:
            matched_jobs = []
            if extracted_skills:
                # Determine if we should use AND (Ketat) or OR (Toleran) logic
                use_and = "Ketat" in search_mode
                matched_jobs = sparql_client.get_jobs_by_skills(extracted_skills, use_and=use_and)

            if not matched_jobs:
                st.warning(
                    "Fuseki terhubung, tetapi kami tidak menemukan job posting yang cocok untuk kombinasi skill ini. Coba tambahkan lebih banyak skill atau variasi soft skill."
                )
                record = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "skills": extracted_skills,
                    "jobs": matched_jobs,
                    "status": "Tidak ditemukan",
                }
            else:
                col1, col2 = st.columns(2, gap="large")
                for index, job in enumerate(matched_jobs):
                    target_col = col1 if index % 2 == 0 else col2
                    skill_tags = "".join(
                        [
                            f"<span style='padding:4px 10px; border-radius:999px; background:{theme['accent_soft']}; color:{theme['accent']}; font-weight:600; font-size:0.8rem; margin-right:6px; display:inline-block; margin-bottom:6px;'>{skill}</span>"
                            for skill in job.get("skills", [])
                        ]
                    )
                    target_col.markdown(
                        f"<div style='padding:20px; margin-bottom:18px; border-radius:22px; background:{theme['card']}; box-shadow:{theme['shadow']}; border: 1px solid {theme['border']}'>"
                        + f"<div style='font-size:0.9rem; color:{theme['accent']}; margin-bottom:8px; text-transform: uppercase; letter-spacing: 0.12em;'>Job Recommendation</div>"
                        + f"<h3 style='margin:0; color:{theme['text']};'>{job['jobTitle']}</h3>"
                        + f"<div style='margin-bottom:8px; color:{theme['accent']};'>{job.get('company', 'Perusahaan Terdaftar')}</div>"
                        + f"<p style='color:{theme['muted']}; margin-top:10px;'>{job.get('description', 'Tidak ada deskripsi tersedia.')}</p>"
                        + f"<div style='margin-top:10px; color:{theme['muted']};'><strong>Vacancy:</strong> {job.get('vacancy', '0')}</div>"
                        + f"<div style='margin-top:12px;'>{skill_tags}</div>"
                        + "</div>",
                        unsafe_allow_html=True,
                    )
                record = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "skills": extracted_skills,
                    "jobs": [job["jobTitle"] for job in matched_jobs],
                    "status": "Ditemukan",
                }
            st.session_state.history.insert(0, record)
            if len(st.session_state.history) > 8:
                st.session_state.history = st.session_state.history[:8]

        except ConnectionError as e:
            st.error(
                "Fuseki tidak berjalan atau tidak bisa dihubungi. Pastikan Apache Jena Fuseki sudah aktif dan dataset 'skillmap' telah dimuat."
            )
            st.markdown(f"<pre style='color:#7c3aed;'>{e}</pre>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(
            f"<div style='border-radius:20px; padding:18px; background:{theme['panel']}; color:{theme['text']}; border: 1px solid {theme['border']}'>"
            + "<strong>Ingin lebih banyak hasil?</strong> Tambahkan skill teknis dan soft skill bersama-sama, misalnya Python + Communication, atau Figma + User Research."
            + "</div>",
            unsafe_allow_html=True,
        )

        with st.expander("Hasil Sebelumnya"):
            if st.session_state.history:
                for item in st.session_state.history:
                    previous_jobs = item.get("jobs") or item.get("roles", [])
                    job_text = ", ".join(previous_jobs) if previous_jobs else "-"
                    st.markdown(
                        f"<div style='margin-bottom:14px; padding:16px; border-radius:18px; background:{theme['card']}; color:{theme['text']}; box-shadow: {theme['shadow']}; border: 1px solid {theme['border']}'>"
                        + f"<div style='font-size:0.85rem; color: {theme['muted']};'>Waktu: {item['timestamp']} · Status: {item['status']}</div>"
                        + f"<div style='margin-top:8px;'><strong>Skill:</strong> {', '.join(item['skills']) or '-'}</div>"
                        + f"<div style='margin-top:6px;'><strong>Job:</strong> {job_text}</div>"
                        + "</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("Belum ada hasil pencarian sebelumnya. Coba jalankan pencarian sekali.")

    st.markdown(
        f"<div style='margin-top: 26px; text-align: center; color: {theme['muted']}; font-size: 0.9rem;'>"
        + "Dibuat dengan rasa ingin tahu dan kopi hangat · SkillMap Studio"
        + "</div>",
        unsafe_allow_html=True,
    )


def render_jobs_view(theme, skill_options):
    st.markdown(
        f"""
        <div style="border-radius: 26px; padding: 28px; background: {theme['card']}; box-shadow: {theme['shadow']}; margin-bottom: 22px; border: 1px solid {theme['border']};">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.22em; color: {theme['muted']}; margin-bottom: 10px;">Role Atlas</div>
            <h1 style="margin: 0; font-family: 'Fraunces', serif; font-size: 2.6rem; line-height: 1.06; color: {theme['text']};">Jelajahi Career Role</h1>
            <p style="margin-top: 14px; font-size: 1.02rem; color: {theme['muted']}; max-width: 740px;">Semua role yang tersimpan di database tampil di sini, lengkap dengan skill yang dibutuhkan untuk membangun jalur kariermu.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filter_left, filter_right = st.columns([2.2, 1], gap="large")
    with filter_left:
        search_text = st.text_input("Cari role", placeholder="Contoh: Data Engineer")
        skill_filter = st.multiselect("Filter berdasarkan skill", skill_options)
        # Add toggle for OR/AND logic
        filter_mode = "Ketat"  # Default to AND (Ketat)
        if skill_filter:  # Only show toggle if skills are selected
            filter_mode = st.radio(
                "Mode filter skill:",
                options=["Toleran", "Ketat"],
                index=1,  # Default to Ketat (AND)
                key="jobs_filter_mode",  # Unique key to avoid conflicts
                help="Toleran: Role memiliki salah satu skill. Ketat: Role memiliki semua skill yang dipilih.",
            )
    with filter_right:
        st.markdown(
            f"<div style='padding:16px; border-radius:18px; background:{theme['panel']}; border:1px solid {theme['border']};'>"
            + "Gunakan filter untuk melihat role yang paling relevan dengan skillmu."
            + "</div>",
            unsafe_allow_html=True,
        )

    try:
        roles = sparql_client.get_all_roles_with_skills()
    except ConnectionError as exc:
        roles = []
        st.error("Fuseki belum terhubung. Pastikan server menyala dan dataset tersedia.")
        st.markdown(f"<pre style='color:#7c3aed;'>{exc}</pre>", unsafe_allow_html=True)

    if search_text:
        roles = [
            role for role in roles
            if search_text.lower() in role["role"].lower()
        ]

    if skill_filter:
        selected = {skill.lower() for skill in skill_filter}
        
        # Check if Ketat (AND) mode is selected
        # filter_mode is defined in the radio button above
        use_and = "Ketat" in filter_mode if 'filter_mode' in dir() else True
        
        if use_and:
            # AND logic: role must have ALL selected skills
            roles = [
                role for role in roles
                if selected.issubset({skill.lower() for skill in role["skills"]})
            ]
        else:
            # OR logic: role can have ANY of the selected skills
            roles = [
                role for role in roles
                if any(skill.lower() in {s.lower() for s in role["skills"]} for skill in selected)
            ]

    if not roles:
        st.warning("Belum ada role yang cocok dengan filtermu atau database masih kosong.")
        return

    st.markdown(
        f"<div style='margin-bottom: 14px; font-family: Fraunces, serif; font-size: 1.8rem; color: {theme['text']}; font-weight: 700;'>Koleksi Role</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(2, gap="large")
    for index, role in enumerate(roles):
        target = cols[index % 2]
        skill_tags = "".join(
            [
                f"<span style='padding:4px 10px; border-radius:999px; background:{theme['accent_soft']}; color:{theme['accent']}; font-weight:600; font-size:0.8rem; margin-right:6px; display:inline-block; margin-bottom:6px;'>{skill}</span>"
                for skill in role["skills"]
            ]
        )
        target.markdown(
            f"""
            <div style="padding:20px; margin-top:16px; border-radius:22px; background:{theme['card']}; box-shadow:{theme['shadow']}; border:1px solid {theme['border']}; height:100%; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="font-size:0.8rem; letter-spacing:0.16em; color:{theme['muted']}; text-transform:uppercase;">Job Posting</div>
                    <h3 style="margin:10px 0 4px; color:{theme['text']};">{role['role']}</h3>
                    <div style="font-size:0.9rem; color:{theme['accent']}; margin-bottom:10px;">{role.get('company', 'Perusahaan Terdaftar')}</div>
                    <div style="margin-bottom:12px; color:{theme['muted']}; font-size:0.95rem;">{role.get('description', 'Tidak ada deskripsi tersedia.')}</div>
                    <div style="margin-bottom:10px; color:{theme['muted']};">Skill utama yang dibutuhkan:</div>
                    <div>{skill_tags}</div>
                </div>
                <div style="margin-top:18px; display:flex; justify-content:space-between; align-items:center; font-size:0.88rem; color:{theme['muted']};">
                    <div><strong>Vacancy</strong>: {role.get('vacancy', '0')}</div>
                    <div style="color:{theme['accent']}; font-weight:600;">{role.get('vacancy', '0')} open</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_ai_assistant_view(theme, skill_keyword_map):
    st.markdown(
        f"""
        <div style="border-radius: 26px; padding: 28px; background: {theme['card']}; box-shadow: {theme['shadow']}; margin-bottom: 22px; border: 1px solid {theme['border']};">
            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.22em; color: {theme['muted']}; margin-bottom: 10px;">Assistant Lab</div>
            <h1 style="margin: 0; font-family: 'Fraunces', serif; font-size: 2.6rem; line-height: 1.06; color: {theme['text']};">AI Assistant</h1>
            <p style="margin-top: 14px; font-size: 1.02rem; color: {theme['muted']}; max-width: 740px;">Bicara tentang apa yang kamu sukai, apa yang membuatmu bersemangat, dan bagaimana itu bisa menjadi jalur karier. Ini bukan sekadar pencarian, melainkan refleksi untuk menemukan arah yang cocok untukmu.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "ai_chat" not in st.session_state:
        st.session_state.ai_chat = [
            {
                "role": "assistant",
                "content": "Halo! Ceritakan apa yang kamu sukai, pengalaman yang membuatmu semangat, atau aktivitas yang ingin kamu lakukan setiap hari. Saya akan membantu merangkainya menjadi gambaran skill dan jalur karier yang bisa kamu pertimbangkan.",
            }
        ]

    for message in st.session_state.ai_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ceritakan apa yang membuatmu bersemangat, kegemaranmu, atau pengalaman kerja yang paling kamu nikmati...")
    if prompt:
        st.session_state.ai_chat.append({"role": "user", "content": prompt})

        with st.spinner("Memahami apa yang kamu sukai..."):
            decoded_skills = []
            jobs = []
            error_message = None
            try:
                decoded_skills = decode_user_input_to_skills(prompt, skill_keyword_map)
                if decoded_skills:
                    jobs = sparql_client.get_jobs_by_skills(decoded_skills)
            except Exception as exc:
                error_message = str(exc)

        if error_message:
            assistant_text = (
                "Saat ini AI tidak tersedia. Ayo teruskan ceritamu dengan kata-kata yang kamu sukai, seperti jenis tugas, kolaborasi, atau hasil kerja yang membuatmu bangga."
            )
        elif not decoded_skills:
            assistant_text = (
                "Saya mendengar kamu sedang membahas sesuatu yang penting, tetapi saya belum bisa menautkannya ke skill spesifik. "
                "Coba ceritakan lagi dengan mencontohkan aktivitas seperti membuat desain, menulis kode, memimpin tim, atau menyusun strategi."
            )
        else:
            skills_text = ", ".join(decoded_skills)
            if not jobs:
                assistant_text = (
                    f"Dari cerita kamu, saya mendeteksi skill: {skills_text}. "
                    "Itu menunjukkan area yang bisa kamu dalami, seperti proyek kreatif, analisis data, atau kolaborasi tim. "
                    "Jika kamu mau, saya bisa bantu merangkum lagi dengan fokus pada apa yang paling membuatmu bersemangat."
                )
            else:
                roles = ", ".join({job['jobTitle'] for job in jobs[:3]})
                assistant_text = (
                    f"Dari cerita kamu, saya mendeteksi skill: {skills_text}. "
                    f"Area ini biasanya cocok dengan peran seperti {roles}. "
                    "Ini bukan daftar yang pasti, tapi bisa jadi inspirasi untuk jalur karier yang selaras dengan apa yang kamu sukai. "
                    "Kalau kamu ingin, kita bisa menggali apa yang membuat setiap peran itu menarik bagi kamu."
                )

        st.session_state.ai_chat.append({"role": "assistant", "content": assistant_text})
        st.rerun()
