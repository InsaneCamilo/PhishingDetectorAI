
# PhishingDetectorAI

PhishingDetectorAI es una aplicación web que permite analizar una URL y determinar si puede ser legítima o un posible caso de phishing mediante un modelo de Machine Learning.

El usuario ingresa una URL y el sistema muestra su clasificación, el porcentaje estimado de phishing y una recomendación según el resultado obtenido.

## 1. Tecnologías utilizadas

- Python
- Pandas y NumPy
- Scikit-learn
- Streamlit
- Joblib
- Matplotlib y Seaborn
- HTML y CSS
- Google Colab
- Git y GitHub

## 2. Dataset

Para el entrenamiento utilizamos el dataset PhiUSIIL Phishing URL del repositorio UCI Machine Learning.

https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset

El dataset cuenta inicialmente con 235.795 registros. Después de realizar la limpieza de los datos quedaron 235.370 registros, distribuidos de la siguiente manera:

| Tipo de URL | Cantidad |
|---|---:|
| Legítimas | 134.850 |
| Phishing | 100.520 |
| Total | 235.370 |

Para este proyecto decidi trabajar únicamente con el texto de las URLs como entrada del modelo, ya que se busca que el usuario pueda analizar un enlace sin necesidad de acceder a la página.

También modifique las etiquetas originales del dataset para representar las URLs legítimas con 0 y las de phishing con 1.

## 3. Entrenamiento del modelo

El entrenamiento se realizó en Google Colab. Durante este proceso se realizó la limpieza de los datos, la separación de los conjuntos de entrenamiento, validación y prueba, y la comparación de dos modelos:

- Naive Bayes.
- Regresión Logística.

Utilizamos TF-IDF para transformar el texto de las URLs en valores numéricos que puedan ser procesados por los modelos.

Finalmente seleccionamos Regresión Logística, ya que obtuvo mejores resultados durante la validación.

## 4. Resultados obtenidos

Los resultados del modelo seleccionado sobre el conjunto de prueba fueron los siguientes:

| Métrica | Resultado |
|---|---:|
| Accuracy | 99,62 % |
| Precision | 100 % |
| Recall | 99,10 % |
| F1-score | 99,55 % |
| ROC-AUC | 99,89 % |

El conjunto de prueba estuvo compuesto por 47.074 URLs, de las cuales 46.894 fueron clasificadas correctamente y 180 fueron clasificadas de forma incorrecta.

Aunque los resultados fueron buenos, el modelo puede cometer errores al analizar URLs nuevas.

## 5. Funcionamiento de la aplicación

La aplicación fue desarrollada utilizando Streamlit. También utilice HTML y CSS para personalizar su diseño y darle una apariencia similar a las herramientas de análisis de seguridad web.

Su funcionamiento es el siguiente:

1. El usuario ingresa una URL.
2. El sistema verifica que la entrada sea válida.
3. La URL es procesada por el modelo entrenado.
4. El modelo realiza la predicción.
5. La aplicación muestra el resultado y los porcentajes obtenidos.
6. Se presenta una recomendación según el riesgo estimado.

El modelo se carga desde un archivo .joblib, por lo que no es necesario volver a entrenarlo cada vez que se inicia la aplicación.

## 6. Estructura del proyecto

```text
PhishingDetectorAI/
├── .streamlit/
│   └── config.toml
├── app/
│   ├── app.py
│   └── predictor.py
├── models/
│   └── phishing_detector.joblib
├── notebooks/
│   └── ModeloPhishing.ipynb
├── reports/
│   └── diagramas/
├── tests/
│   └── test_predictor.py
├── .gitignore
├── requirements.txt
└── README.md
```

- app: contiene la interfaz y la lógica de predicción.
- models: contiene el modelo entrenado.
- notebooks: contiene el proceso de entrenamiento y evaluación.
- reports: contiene los diagramas del proyecto.
- tests: contiene las pruebas unitarias.
- .streamlit: contiene la configuración visual de la aplicación.

## 7. Ejecución local

Para ejecutar el proyecto es necesario tener Python instalado.

Clonar el repositorio:

```bash
git clone https://github.com/InsaneCamilo/PhishingDetectorAI.git
cd PhishingDetectorAI
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python -m streamlit run app/app.py
```

La aplicación estará disponible en:

http://localhost:8501



## 8. Pruebas realizadas

Para comprobar el funcionamiento del sistema realizamos cinco pruebas unitarias:

- Agregar HTTPS cuando la URL no contiene un esquema.
- Conservar HTTPS cuando ya está presente.
- Rechazar entradas vacías.
- Rechazar URLs con espacios.
- Rechazar URLs sin un dominio válido.

Para ejecutar las pruebas:

```bash
python -m unittest discover -s tests -v
```

Las cinco pruebas se ejecutaron correctamente.

También realizamos pruebas directamente desde la interfaz:

| Entrada | Resultado obtenido |
|---|---|
| https://www.google.com/ | 96 % de probabilidad de legítima |
| http://verify-payment.example.test/update | 99,98 % de probabilidad de phishing |
| Campo vacío | Mensaje de validación |
| https:/// | Mensaje de URL inválida |

La segunda URL corresponde a un ejemplo creado para realizar pruebas y no a una página de phishing real verificada.

## 9. Despliegue

La plataforma seleccionada para el despliegue del proyecto es Streamlit Community Cloud.

Para realizar el despliegue se debe conectar el repositorio de GitHub con Streamlit y seleccionar app/app.py como archivo principal.

El modelo entrenado debe estar incluido en la carpeta models para que la aplicación pueda realizar las predicciones.

## 10. Limitaciones

- El modelo analiza únicamente el texto de la URL.
- No accede al contenido de las páginas web.
- No consulta certificados, DNS ni bases de datos de amenazas en tiempo real.
- Puede clasificar incorrectamente algunas URLs.
- Los resultados dependen de los datos utilizados durante el entrenamiento.
- Pueden existir dominios relacionados entre los conjuntos de entrenamiento y prueba, lo que puede influir en las métricas obtenidas.

Una URL clasificada como legítima no significa que sea completamente segura.

## 11. Conclusiones

Durante el desarrollo de este proyecto pude aplicar los conocimientos adquiridos sobre Machine Learning, preparación de datos, entrenamiento de modelos e integración con una aplicación web.

Los resultados obtenidos muestran que es posible identificar patrones asociados al phishing utilizando únicamente el texto de una URL.

Sin embargo, considero que esta herramienta debe utilizarse como un apoyo para identificar enlaces sospechosos y no como un reemplazo de otras herramientas de seguridad.

