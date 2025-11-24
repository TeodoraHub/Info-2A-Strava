# Striv: Connected Sports App

## Introduction

**Striv** (Breton word meaning 'effort') is an application developed for monitoring and sharing sports activities.

Our goal is to create an accessible **free alternative** to the existing major platforms. Striv allows users to analyze their performance, share their activities and interact within a sports social network.

---

## Key Features

The application is built around endurance activities (running, cycling, hiking, swimming) and offers the following features:

* **Activity Creation** : Users can upload their activities via a **GPX** file.
* **Performance Analysis**: Access to personalized statistics on performance (number of activities, distance, duration per week/sport).
* **Social Network**: Consultation of a **news feed** listing the activities of followed users.
* **Interaction** : Ability to **like and comment** shared activities.

---

## Development Team

This project was carried out by a team of students from **ENSAI**.

* Abel CORNET-CARLOS
* Victor GAUTIER
* Téodora MOLDOVAN
* Grégoire WEBER
* Anicet Marius YABOYA

Under the direction of Samuel GOUTIN

## To launch the application
python -m uvicorn src.API:app --host 0.0.0.0 --port 5000 --reload

## To launch the streamlit (in another terminal)
streamlit run src/app_streamlit.py --server.port=5001 --server.address=0.0.0.0
