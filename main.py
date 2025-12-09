#!/usr/bin/env python3
"""
Main entry point pour l'application Striv API

Ce fichier permet de lancer facilement l'application FastAPI avec uvicorn.

Usage:
    python main.py

Pour le développement avec rechargement automatique:
    python main.py --dev
"""

import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ajouter le dossier src au PYTHONPATH

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from routers import activities, auth, comments, feed, followers, likes, stats, predictions  # NOQA

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routeurs
app.include_router(auth.router)
app.include_router(activities.router)
app.include_router(stats.router)
app.include_router(comments.router)
app.include_router(followers.router)
app.include_router(likes.router)
app.include_router(feed.router)
app.include_router(predictions.router)  # ✅ AJOUTER CETTE LIGNE


def main():
    """Lance le serveur uvicorn avec l'application FastAPI"""

    # Vérifier si mode développement
    dev_mode = "--dev" in sys.argv or "-d" in sys.argv

    print("=" * 60)
    print("🚀 Lancement de Striv API")
    print("=" * 60)
    print(f"Mode: {'Développement' if dev_mode else 'Production'}")
    print("URL: http://localhost:5000")
    print("Documentation: http://localhost:5000/docs")
    print("ReDoc: http://localhost:5000/redoc")
    print("=" * 60)
    print("\nUtilisateurs de test disponibles:")
    print("  - alice / wonderland (admin)")
    print("  - bob / builder (user)")
    print("=" * 60)
    print("\nEndpoints de test disponibles:")
    print("  - GET /health - Vérifier l'état de santé de l'API")
    print("  - GET /test/complete-workflow - Tester toutes les fonctionnalités")
    print("  - GET /me - Obtenir les informations de l'utilisateur connecté")
    print("=" * 60)
    print("\nPour arrêter le serveur: Ctrl+C")
    print("=" * 60)
    print()

    # Configuration uvicorn
    config = {
        "app": "API:app",
        "host": "0.0.0.0",
        "port": 5000,
    }

    # Options supplémentaires en mode développement
    if dev_mode:
        config.update(
            {
                "reload": True,
                "log_level": "debug",
            }
        )

    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur...")
        print("✨ Au revoir!")


if __name__ == "__main__":
    main()
