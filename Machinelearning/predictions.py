import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import numpy as np

file_path = "GDI_1990_2021.csv"
gdi_data = pd.read_csv(file_path)


gdi_melted = gdi_data.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='GDI', value_vars=gdi_data.columns[7:])
gdi_melted['Year'] = gdi_melted['Year'].str.extract('(\d+)').astype(int)
gdi_melted.dropna(subset=['GDI'], inplace=True)


country_predictions = {}
country_mse = {}
years_to_predict = np.array(range(2022, 2041)).reshape(-1, 1)

for country in gdi_melted['Country'].unique():
    country_data = gdi_melted[gdi_melted['Country'] == country]
    X = country_data[['Year']]
    y = country_data['GDI']

    
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    if len(X) > 5:  
        #premières années pour l'entraînement et les dernières pour le test
        split_index = int(len(X) * 0.7)  # 70% pour l'entraînement, 30% pour le test
        X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
        y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]



    # Linear Regression with Cross-Validation
    lin_reg = LinearRegression()
    cross_val_scores = cross_val_score(lin_reg, X_train, y_train, cv=5)
    lin_reg.fit(X_train, y_train)
    y_pred_lin_reg = lin_reg.predict(years_to_predict)

    # Ridge Regression
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    y_pred_ridge = ridge.predict(years_to_predict)

    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(years_to_predict)

    # K-Nearest Neighbors (KNN)
    min_neighbors = min(5, len(X_train) - 1)  
    knn = KNeighborsRegressor(n_neighbors=min_neighbors)
    knn.fit(X_train, y_train)
    y_pred_knn = knn.predict(years_to_predict)

    # Support Vector Regression (SVR)
    svr = SVR(kernel='rbf')
    svr.fit(X_train, y_train)
    y_pred_svr = svr.predict(years_to_predict)

    
    mse_scores = {
        'Linear Regression': mean_squared_error(y_test, lin_reg.predict(X_test)),
        'Ridge Regression': mean_squared_error(y_test, ridge.predict(X_test)),
        'Random Forest': mean_squared_error(y_test, rf.predict(X_test)),
        'KNN': mean_squared_error(y_test, knn.predict(X_test)),
        'SVR': mean_squared_error(y_test, svr.predict(X_test))
    }

   
    country_predictions[country] = {
        'Linear Regression': y_pred_lin_reg,
        'Ridge Regression': y_pred_ridge,
        'Random Forest': y_pred_rf,
        'KNN': y_pred_knn,
        'SVR': y_pred_svr
    }
    country_mse[country] = mse_scores

def get_predictions(country):
    return country_predictions.get(country, {}) 

def get_mse(country):
    return country_mse.get(country, {})  

def get_actual_gdi(country):
    """
    Renvoie les valeurs réelles du GDI pour un pays spécifié.
    """
    country_data = gdi_melted[gdi_melted['Country'] == country]
    return country_data[['Year', 'GDI']]

def get_predictions_and_actual_gdi(country):
    """
    Renvoie les prédictions et les valeurs réelles du GDI pour un pays spécifié.
    """
    predictions = country_predictions.get(country, {})
    actual_gdi = get_actual_gdi(country)
    return predictions, actual_gdi

def get_available_countries():
    """
    Renvoie la liste des pays disponibles dans le jeu de données.
    """
    return gdi_melted['Country'].unique().tolist()



example_country = list(country_predictions.keys())[0]
example_predictions = country_predictions[example_country]
example_mse = country_mse[example_country]

example_country, example_predictions, example_mse
