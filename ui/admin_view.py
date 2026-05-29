import streamlit as st

from services.auth import load_admin_users
from services.ttl_store import (
    append_ttl_block,
    load_ttl_text,
    normalize_id,
    parse_roles_from_ttl,
    parse_skills_from_ttl,
    remove_subject_blocks,
    save_ttl_text,
    subject_exists,
)


def render_admin_view(theme):
    st.sidebar.markdown("### Admin Login")
    username = st.sidebar.text_input("Username", value=st.session_state.admin_user)
    password = st.sidebar.text_input("Password", type="password")
    login_clicked = st.sidebar.button("Login")
    if login_clicked:
        admins = load_admin_users()
        if admins.get(username) == password:
            st.session_state.authenticated = True
            st.session_state.admin_user = username
        else:
            st.session_state.authenticated = False
            st.sidebar.error("Username atau password salah.")

    if st.session_state.authenticated:
        st.sidebar.success(f"Masuk sebagai {st.session_state.admin_user}.")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.admin_user = ""
    else:
        st.sidebar.info("Gunakan admin yang sudah disiapkan di environment: ADMIN_USERS.")

    st.markdown(
        f"""
        <div style="border-radius: 22px; padding: 22px; background: {theme['card']}; box-shadow: {theme['shadow']}; border: 1px solid {theme['border']}; margin-bottom: 20px;">
            <div style="font-size: 0.9rem; color: {theme['muted']}; text-transform: uppercase; letter-spacing: 0.18em; margin-bottom: 8px;">Admin Studio</div>
            <h1 style="margin: 0; font-family: 'Fraunces', serif; font-size: 2.2rem; color: {theme['text']};">Kelola Data Turtle</h1>
            <p style="margin-top: 10px; color: {theme['muted']};">Tambah dan hapus skill atau career role langsung ke file Turtle.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.authenticated:
        st.warning("Silakan login admin untuk mengakses panel ini.")
        st.stop()

    ttl_text = load_ttl_text()
    ttl_skills = parse_skills_from_ttl(ttl_text)
    ttl_roles = parse_roles_from_ttl(ttl_text)

    summary_left, summary_right = st.columns(2)
    summary_left.metric("Total Skill", len(ttl_skills))
    summary_right.metric("Total Role", len(ttl_roles))

    st.markdown("### Tambah Skill")
    with st.form("add_skill_form"):
        new_skill_id = st.text_input("Skill ID (tanpa spasi, contoh: DataOps)")
        new_skill_name = st.text_input("Skill Name (tampilan)")
        preview_skill = st.checkbox("Tampilkan preview Turtle", value=True)
        if preview_skill and new_skill_id and new_skill_name:
            preview_id = normalize_id(new_skill_id)
            st.markdown(
                f"```turtle\n:{preview_id} a :Skill ; :skillName \"{new_skill_name.strip()}\" .\n```"
            )
        add_skill_submit = st.form_submit_button("Tambah Skill")
        if add_skill_submit:
            skill_id = normalize_id(new_skill_id)
            if not skill_id or not new_skill_name.strip():
                st.error("Skill ID dan Skill Name wajib diisi.")
            elif subject_exists(ttl_text, skill_id):
                st.error("Skill ID sudah ada di Turtle.")
            else:
                block = f":{skill_id} a :Skill ; :skillName \"{new_skill_name.strip()}\" ."
                ttl_text = append_ttl_block(ttl_text, block)
                save_ttl_text(ttl_text)
                st.success("Skill baru berhasil ditambahkan.")
                st.rerun()

    st.markdown("### Tambah Career Role")
    with st.form("add_role_form"):
        new_role_id = st.text_input("Role ID (tanpa spasi, contoh: DataEngineer)")
        new_role_name = st.text_input("Role Name (tampilan)")
        required_skills = st.multiselect("Pilih skill yang dibutuhkan", ttl_skills)
        preview_role = st.checkbox("Tampilkan preview Turtle", value=True)
        if preview_role and new_role_id and new_role_name and required_skills:
            preview_id = normalize_id(new_role_id)
            preview_skills = ", ".join([f":{skill}" for skill in required_skills])
            st.markdown(
                "```turtle\n"
                + f":{preview_id} rdf:type :CareerRole ;\n"
                + f"    :roleName \"{new_role_name.strip()}\" ;\n"
                + f"    :requiresSkill {preview_skills} .\n"
                + "```"
            )
        add_role_submit = st.form_submit_button("Tambah Role")
        if add_role_submit:
            role_id = normalize_id(new_role_id)
            if not role_id or not new_role_name.strip() or not required_skills:
                st.error("Role ID, Role Name, dan skill wajib diisi.")
            elif subject_exists(ttl_text, role_id):
                st.error("Role ID sudah ada di Turtle.")
            else:
                skills_line = ", ".join([f":{skill}" for skill in required_skills])
                block = (
                    f":{role_id} rdf:type :CareerRole ;\n"
                    f"    :roleName \"{new_role_name.strip()}\" ;\n"
                    f"    :requiresSkill {skills_line} ."
                )
                ttl_text = append_ttl_block(ttl_text, block)
                save_ttl_text(ttl_text)
                st.success("Career role baru berhasil ditambahkan.")
                st.rerun()

    st.markdown("### Hapus Data")
    with st.form("delete_form"):
        skills_to_delete = st.multiselect("Pilih Skill untuk dihapus", ttl_skills)
        roles_to_delete = st.multiselect("Pilih Role untuk dihapus", ttl_roles)
        confirm_delete = st.checkbox("Saya paham data yang dihapus tidak bisa dikembalikan")
        delete_submit = st.form_submit_button("Hapus Data")
        if delete_submit:
            if not skills_to_delete and not roles_to_delete:
                st.warning("Pilih minimal satu skill atau role untuk dihapus.")
            elif not confirm_delete:
                st.error("Centang konfirmasi sebelum menghapus data.")
            else:
                ttl_text = remove_subject_blocks(ttl_text, skills_to_delete + roles_to_delete)
                save_ttl_text(ttl_text)
                st.success("Data berhasil dihapus dari Turtle.")
                st.rerun()

    st.info("Setelah update Turtle, reload dataset di Fuseki agar query langsung membaca data terbaru.")
