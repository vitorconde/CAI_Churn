# Operationalizing Churn Analytics with Cloudera AI Workbench

## Using Cloudera AI

<details>
  <summary><strong>Seção: Português (PT)</strong></summary>

## Visão Geral

Este projeto demonstra como construir um modelo de previsão de churn utilizando Python, scikit-learn e FastAPI, e como realizar o deploy no Cloudera AI Workbench. O pipeline inclui pré-processamento, treinamento, serialização do modelo e disponibilização via API.

---

### Explicação dos Códigos

- **Modelagem.ipynb**: Notebook que cria um pipeline de machine learning para prever churn. Utiliza dados fictícios, faz o pré-processamento (padronização e one-hot encoding), treina um modelo de regressão logística e salva o pipeline (`model.joblib`).
- **model_server.py**: Script que carrega o pipeline treinado e expõe uma função `predict` para servir o modelo via API. Recebe dados em formato JSON, faz a predição e retorna a probabilidade de churn e a classificação.
- **build.sh**: Script para instalar as dependências necessárias no ambiente do deploy.

---

### Processo de Deploy no Cloudera AI Workbench

**(Espaço para imagens do processo de deploy)**

1. Na aba dos projetos, escolha seu projeto que será feito o deploy.
2. Clique em **New Deploy** neste projeto.
3. Selecione **New Model**.
4. Configure os campos:
   - **Nome do Deploy**: Escolha um nome para o seu modelo.
   - **Build Script Path**: `build.sh`
   - **File**: `model_server.py`
   - **Scoring Function Name**: `predict`
   - **Exemplo de Input**:
     ```json
     {
       "records": {
         "idade": 30,
         "genero": "M",
         "tempo_de_contrato_meses": 10,
         "gasto_mensal": 100
       }
     }
     ```
   - **Exemplo de Output**:
     ```json
     {
       "results": [
         {
           "churn_probability": 0.30353036311804166,
           "prediction": 0
         }
       ]
     }
     ```
   - **Runtime**: Kernel Python

**(Espaço para imagens da configuração do deploy)**

5. Acompanhe o status do deploy, de **Deploying** para **Deployed**.
6. Após o status ser **Deployed**, teste a chamada da API para realizar a escoragem.

</details>

---

<details>
  <summary><strong>Section: English (ENG)</strong></summary>

### Overview

This project demonstrates how to build a churn prediction model using Python, scikit-learn, and FastAPI, and how to deploy it on Cloudera AI Workbench. The pipeline covers preprocessing, training, model serialization, and serving via API.

---

### Code Explanation

- **Modelagem.ipynb**: Notebook that creates a machine learning pipeline for churn prediction. Uses sample data, applies preprocessing (scaling and one-hot encoding), trains a logistic regression model, and saves the pipeline (`model.joblib`).
- **model_server.py**: Script that loads the trained pipeline and exposes a `predict` function to serve the model via API. Accepts JSON input, makes predictions, and returns churn probability and classification.
- **build.sh**: Script to install required dependencies in the deployment environment.

---

### Deploy Process on Cloudera AI Workbench

**(Space for deployment process images)**

1. In the projects tab, select your project for deployment.
2. Click **New Deploy** in this project.
3. Choose **New Model**.
4. Configure the fields:
   - **Deploy Name**: Choose a name for your model.
   - **Build Script Path**: `build.sh`
   - **File**: `model_server.py`
   - **Scoring Function Name**: `predict`
   - **Input Example**:
     ```json
     {
       "records": {
         "idade": 30,
         "genero": "M",
         "tempo_de_contrato_meses": 10,
         "gasto_mensal": 100
       }
     }
     ```
   - **Output Example**:
     ```json
     {
       "results": [
         {
           "churn_probability": 0.30353036311804166,
           "prediction": 0
         }
       ]
     }
     ```
   - **Runtime**: Kernel Python

**(Space for deployment configuration images)**

5. Monitor the deploy status, from **Deploying** to **Deployed**.
6. Once the status is **Deployed**, test the API call to score new data.

</details>

---