import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Первый заголовок сайта
st.title('Beer AI assistant')
st.write(
    "Время приключений! Хватай с собой друзей"
)

# Создание ползунков выбора характеристик
abv = st.slider('Выберите градус алкоголя', 0, 57, 0)
min_ibu = st.slider('Выберите мин. горкость', 0, 65, 0)
max_ibu = st.slider('Выберите макс. горкость', 0, 100, 0)
astringency = st.slider('Выберите терпкость', 0, 83, 0)
body = st.slider('Выберите плотность', 0, 197, 0)
alcohol = st.slider('Выберите алкогольность', 0, 139, 0)
bitter = st.slider('Выберите горечь', 0, 150, 0)
sweet = st.slider('Выберите сладость', 0, 263, 0)
sour = st.slider('Выберите кислость', 0, 323, 0)
salty = st.slider('Выберите солености', 0, 66, 0)
fruits = st.slider('Выберите фруктовость', 0, 222, 0)
hoppy = st.slider('Выберите хмельность', 0, 193, 0)
spices = st.slider('Выберите пряность', 0, 184, 0)
malty = st.slider('Выберите солодовость', 0, 304, 0)

# Импорт датасета
df2 = pd.read_csv('beer_data_set.csv', encoding='ISO-8859-1')
df = pd.DataFrame(df2)

# Удаление строк с пустыми значениями
df = df.dropna()

# Удаление ненужных столбцов
df = df.drop(['Name', 'key', 'Brewery', 'Description', 'Style', 'Ave Rating'], axis=1)

# Разделение данных на признаки и целевую переменную
X = df.drop('Style Key', axis=1)
y = df['Style Key']

# Разделение на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

best_params = {
     'bootstrap': True, 'max_depth': 40, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 300
}

# Обучение модели RandomForest на датасете
# best_rf_model = RandomForestClassifier(n_estimators=300, max_depth=30, random_state=42, max_features='auto', min_samples_leaf=1, min_samples_split=2)
best_rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
best_rf_model.fit(X_train, y_train)

# Масштабирование признаков
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Применяем метод ближайших соседей к выборке рецептов предсказанного стиля
neighbors_style = NearestNeighbors(n_neighbors=1)
neighbors_style.fit(X)

# Создание словаря для быстрого доступа к рецептам по Style Key
style_recipes = {style: df2[df2['Style Key'] == style].index.tolist() for style in df2['Style Key'].unique()}
styles_and_keys = df2.groupby('Style').agg({'Style Key': 'unique'}).reset_index()
styles_and_keys.columns = ['Style Name', 'Style Key']

# Сохранение выбранных характеристик пива
input_data = {
  "ABV": abv,
  "Min IBU": min_ibu,
  "Max IBU": max_ibu,
  "Astringency": astringency,
  "Body": body,
  "Alcohol": alcohol,
  "Bitter": bitter,
  "Sweet": sweet,
  "Sour": sour,
  "Salty": salty,
  "Fruits": fruits,
  "Hoppy": hoppy,
  "Spices": spices,
  "Malty": malty
}


# Кнопка подбора пива
if st.button('Подобрать пиво'):
    input_data_df = pd.DataFrame([input_data])
    input_data_scaled = scaler.transform(input_data_df.values)

    # Предсказываем стиль пива на основе введенных характеристик
    predicted_style = best_rf_model.predict(input_data_scaled)[0]
    style_name = styles_and_keys.loc[styles_and_keys['Style Key'] == predicted_style, 'Style Name'].values[0]

    distance, index = neighbors_style.kneighbors(input_data_df)
    closest_recipe = X.iloc[index[0][0]]

    # Формируем сообщение о ближайшем рецепте и предсказании
    output = f'Предсказанный стиль пива: {style_name}'
    closest_recipe_name = df2.loc[index[0][0], 'Name']
    output_label = f'\nПохожий на ваше описание рецепт: {closest_recipe_name}'
    st.write(output)
    st.write(output_label)

    # Формируем сообщение о ближайшем рецепте и его характеристиках
    output_recept = 'Ближайший реальный рецепт имеет следующие характеристики:\n'
    st.write(output_recept)
    output_recept_har = ''
    for feature in X.columns:
        output_recept_har = f'{feature}: {closest_recipe[feature]}\n'
        st.write(output_recept_har)


    # Создание графика сравнения характеристик
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # График для пользовательского ввода
    axs[0].bar(X.columns, input_data_df.values.flatten(), color='blue', label='Пользовательский выбор')
    axs[0].set_title('Выбранные характеристики')
    axs[0].set_ylabel('Значения')
    axs[0].legend()

    # График для предсказанного рецепта
    axs[1].bar(X.columns, closest_recipe.values, color='red', label='Предсказанный рецепт')
    axs[1].set_title('Предсказанные характеристики')
    axs[1].set_ylabel('Значения')
    axs[1].legend()

    # Отображение графика
    st.pyplot(fig)
