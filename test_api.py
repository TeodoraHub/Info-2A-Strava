#!/usr/bin/env python3
"""
Script de test pour l'API Striv

Ce script teste l'endpoint de test complet de l'API.
"""

import json
import sys

import requests
from requests.auth import HTTPBasicAuth


def test_health():
    """Test de l'endpoint health check"""
    print("🔍 Test de l'endpoint /health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check réussi!")
            print(f"   Réponse: {response.json()}")
            return True
        else:
            print(f"❌ Health check échoué: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API. Est-elle lancée?")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_me(username, password):
    """Test de l'endpoint /me"""
    print(f"\n🔍 Test de l'endpoint /me avec {username}...")
    try:
        response = requests.get(
            "http://localhost:8000/me", auth=HTTPBasicAuth(username, password), timeout=5
        )
        if response.status_code == 200:
            print("✅ Authentification réussie!")
            print(f"   Utilisateur: {response.json()}")
            return True
        else:
            print(f"❌ Authentification échouée: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_complete_workflow(username, password):
    """Test de l'endpoint de test complet"""
    print(f"\n🔍 Test de l'endpoint /test/complete-workflow avec {username}...")
    try:
        response = requests.get(
            "http://localhost:8000/test/complete-workflow",
            auth=HTTPBasicAuth(username, password),
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Test complet exécuté!")
            print("\n📊 Résumé des tests:")
            print(f"   Utilisateur testé: {result['user_tested']}")
            print(f"   Total de tests: {result['summary']['total_tests']}")
            print(f"   Réussis: {result['summary']['successful']}")
            print(f"   Échoués: {result['summary']['failed']}")
            print(f"   Taux de réussite: {result['summary']['success_rate']}")

            print("\n📝 Détails des tests:")
            for test_name, test_result in result["tests"].items():
                status_emoji = "✅" if test_result["status"] == "SUCCESS" else "❌"
                print(f"   {status_emoji} {test_name}: {test_result['status']}")
                if test_result["status"] == "FAILED":
                    print(f"      Erreur: {test_result.get('error', 'Unknown')}")

            # Afficher le JSON complet si demandé
            if "--json" in sys.argv:
                print("\n📄 Réponse JSON complète:")
                print(json.dumps(result, indent=2))

            return result["summary"]["failed"] == 0
        else:
            print(f"❌ Test échoué: {response.status_code}")
            print(f"   Message: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print("=" * 70)
    print("🧪 Test de l'API Striv")
    print("=" * 70)

    # Test 1: Health check
    if not test_health():
        print("\n⚠️  L'API ne semble pas être lancée.")
        print("   Veuillez lancer l'API avec: python main.py")
        sys.exit(1)

    # Test 2: Authentification et endpoint /me
    users_to_test = [("alice", "wonderland"), ("bob", "builder")]

    for username, password in users_to_test:
        if not test_me(username, password):
            print(f"\n⚠️  Échec de l'authentification pour {username}")
            continue

        # Test 3: Workflow complet
        test_complete_workflow(username, password)

    print("\n" + "=" * 70)
    print("✨ Tests terminés!")
    print("=" * 70)
    print("\nPour voir la documentation complète de l'API:")
    print("  http://localhost:8000/docs")


if __name__ == "__main__":
    main()
