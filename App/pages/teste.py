import streamlit as st

# Caminho da imagem (pode ser local ou por URL)
background_image = "https://images.unsplash.com/photo-1503264116251-35a269479413"

# Insere o CSS com a imagem de fundo
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Minha página com imagem de fundo!")
st.write("Conteúdo vai aqui.")
