import streamlit as st
import baremes as b
from PIL import Image

def clear_form():
    st.session_state["pr"] = "Île-de-France"
    st.session_state["n1"] = ""
    st.session_state["n2"] = ""

image = Image.open('./images/logo.png')
st.image(image, use_column_width='auto')
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

with st.form("myform"):
    c1, c2 = st.columns([1, 2])
    c1.text("Region:")
    c2.radio("Region", options=['Île-de-France', 'Province'], key="pr", horizontal=True, label_visibility="collapsed")
    c1, c2 = st.columns([1, 2])
    c1.text("Numéro fiscal:")
    c2.text_input("Numéro fiscal:", key="n1", label_visibility="collapsed")
    c1, c2 = st.columns([1, 2])
    c1.text("Référence de l'avis:")
    c2.text_input("Référence de l'avis:", key="n2", label_visibility="collapsed")
    error_n1 = st.empty()
    error_n1.write("&nbsp;", unsafe_allow_html=True)
    c1, c2 = st.columns([4, 1])
    with c1:
        submit = st.form_submit_button(label="Valider", help="Vérifier les informations d'avis")
    with c2:
        clear = st.form_submit_button(label="Réinitialiser", on_click=clear_form)

if submit:
    st.session_state.ok = 1
    if st.session_state["n1"] == '':
        st.session_state.ok = 0
    if st.session_state["n2"] == '':
        st.session_state.ok = 0
    if st.session_state.ok:
        with st.spinner('Wait for it...'):
            res = b.checkEligibility(st.session_state.pr, st.session_state.n1, st.session_state.n2)
        if res['is_ok'] == 1:
            with st.expander("Results", expanded=True):
                c1, c2 = st.columns(2)
                c1.metric("ANAH", value=res['ANAH'])
                c2.metric("CNAV", value=res['CNAV'])
                if res['var']['ANAH'] >= 50 and res['var']['CNAV'] >=37:
                    st.markdown('<h3 style="color:#456BA5">Félicitations! Vous êtes éligible à une prise en charge intégrale de votre aménagement de salle de bains. 😄</h3>', unsafe_allow_html=True)
                    st.balloons()
        else:
            error_n1.markdown(f":red[{res['error']}]")

        with st.expander('Details'):
            st.write(res)
    else:
        error_n1.markdown(":red[La saisie de toutes les zones est obligatoire]")

if clear:
    st.session_state.ok = 0
