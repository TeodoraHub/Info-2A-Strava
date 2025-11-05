#!/usr/bin/env python3
"""
Main entry point pour l'application Striv API

Ce fichier permet de lancer facilement l'application FastAPI avec uvicorn.

Usage:
    python main.py

Pour le développement avec rechargement automatique:
    python main.py --dev
"""

import sys
from pathlib import Path

import uvicorn

# Ajouter le dossier src au PYTHONPATH
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main():
    """Lance le serveur uvicorn avec l'application FastAPI"""

    # Vérifier si mode développement
    dev_mode = "--dev" in sys.argv or "-d" in sys.argv

    print("=" * 60)
    print("🚀 Lancement de Striv API")
    print("=" * 60)
    print(f"Mode: {'Développement' if dev_mode else 'Production'}")
    print("URL: http://localhost:8000")
    print("Documentation: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
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
        "port": 8000,
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
