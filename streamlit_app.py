import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

st.title('Beer AI assistant')

abv = st.slider('Выберите градус алкоголя', 0, 57, 10)
min_ibu = st.slider('Выберите мин. горкость', 0, 65, 10)
max_ibu = st.slider('Выберите макс. горкость', 0, 100, 10)
astringency = st.slider('Выберите терпкость', 0, 83, 10)
body = st.slider('Выберите плотность', 0, 197, 10)
alcohol = st.slider('Выберите алкогольность', 0, 139, 10)
bitter = st.slider('Выберите горечь', 0, 150, 10)
sweet = st.slider('Выберите сладость', 0, 263, 10)
sour = st.slider('Выберите кислость', 0, 323, 10)
salty = st.slider('Выберите солености', 0, 66, 10)
fruits = st.slider('Выберите фруктовость', 0, 222, 10)
hoppy = st.slider('Выберите хмельность', 0, 193, 10)
spices = st.slider('Выберите пряность', 0, 184, 10)
malty = st.slider('Выберите солодость', 0, 304, 10)

if st.button('Подобрать пиво'):
    result = f"Данные обработаны:"
    st.write(result)
