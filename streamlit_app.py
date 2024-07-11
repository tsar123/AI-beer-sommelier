import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('Beer AI assistant')
st.write(
    "Время приключений! Хватай с собой друзей"
)



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

df2 = pd.read_csv('https://raw.githubusercontent.com/Riddars/BeerProjectForEng/main/beer_data_set.csv', encoding='ISO-8859-1')
df = pd.DataFrame(df2)

# Удаление ненужных столбцов
df = df.drop(['Name', 'key', 'Brewery', 'Description', 'Style', 'Ave Rating'], axis=1)

# Разделение данных на признаки и целевую переменную
X = df.drop('Style Key', axis=1)
y = df['Style Key']
# Разделение на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# best_params = {
#      'bootstrap': True, 'max_depth': 40, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 300
# }

#rf = RandomForestClassifier()
# best_rf_model = RandomForestClassifier(n_estimators=100, param_distributions=best_params, random_state=42)
best_rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
best_rf_model.fit(X_train, y_train)
#random_search = RandomizedSearchCV(estimator=rf, param_distributions=best_params, n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)

# Поиск лучших параметров
# random_search.fit(X_train, y_train)

# best_rf_model = random_search.best_estimator_

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Обучение модели RandomForest на всем датасете
# best_rf_model.fit(X_scaled, y)
# best_rf_model.fit(X, y)

# Создание словаря для быстрого доступа к рецептам по Style Key
style_recipes = {style: df2[df2['Style Key'] == style].index.tolist() for style in df2['Style Key'].unique()}

styles_and_keys = df2.groupby('Style').agg({'Style Key': 'unique'}).reset_index()
styles_and_keys.columns = ['Style Name', 'Style Key']

input_data = {
    'abv': [abv],
    'min_ibu': [min_ibu],
    'max_ibu': [max_ibu],
    'astringency': [astringency],
    'body': [body],
    'alcohol': [alcohol],
    'bitter': [bitter],
    'sweet': [sweet],
    'sour': [sour],
    'salty': [salty],
    'fruits': [fruits],
    'hoppy': [hoppy],
    'spices': [spices],
    'malty': [malty]
    }

if st.button('Подобрать пиво'):
    input_data_df = pd.DataFrame([input_data])

    input_data_scaled = scaler.transform(input_data_df)
    predicted_style = best_rf_model.predict(input_data_scaled)[0] #Предсказываем стиль пива на основе введенных характеристик
    style_name = styles_and_keys.loc[styles_and_keys['Style Key'] == predicted_style, 'Style Name'].values[0]


    style_indices = style_recipes[predicted_style]
    # Создаем выборку рецептов предсказанного стиля
    X_style = X.iloc[style_indices]
    """
    Тут мы создаем "подвыборку" из нашей базы данных,
    включающую только рецепты предсказанного стиля пива.
    Это как если бы мы открыли книгу рецептов на разделе с конкретным стилем пива.
    """

    # Применяем метод ближайших соседей к выборке рецептов предсказанного стиля
    neighbors_style = NearestNeighbors(n_neighbors=1)
    neighbors_style.fit(X_style)

    distance, index = neighbors_style.kneighbors(input_data)
    closest_recipe_index = style_indices[index[0][0]]
    closest_recipe = X.iloc[closest_recipe_index]
    """
    Этот блок кода ищет рецепт, который наиболее похож на характеристики,
    введенные пользователем, но только среди рецептов предсказанного стиля. Это похоже на то,
    как если бы мы искали в книге рецептов тот, который наиболее близок к тому, что хочет пользователь.
    """
    # Формируем сообщение о ближайшем рецепте и предсказании
    output = f'Предсказанный стиль пива: {style_name}'
    closest_recipe_name = df2.loc[closest_recipe_index, 'Name']
    output_label = f'\nПохожий на ваше описание рецепт: {closest_recipe_name}'
    """
    Здесь мы просто выводим результаты нашего анализа:
    какой стиль пива мы предсказали и какой конкретный рецепт наиболее похож на то, что хотел пользователь.
    """

    # # Формируем сообщение о ближайшем рецепте и его характеристиках
    # output = 'Ближайший реальный рецепт имеет следующие характеристики:\n'
    # for feature in X.columns:
    #     output += f'{feature}: {closest_recipe[feature]}\n'


    # Выводим сообщение с характеристиками ближайшего рецепта
    st.write(output)
    st.write(output_label)
