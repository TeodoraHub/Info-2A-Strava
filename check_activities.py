#!/usr/bin/env python3
"""Vérifier les activités dans la base de données"""

from dotenv import load_dotenv
load_dotenv()

from dao.db_connection import DBConnection

try:
    conn = DBConnection().connection
    cursor = conn.cursor()
    
    # Lister toutes les activités
    cursor.execute("SELECT id, titre, sport, date_activite, id_user FROM activite ORDER BY id;")
    activities = cursor.fetchall()
    
    print("\n" + "=" * 70)
    print("🏃 ACTIVITÉS DANS LA BASE DE DONNÉES")
    print("=" * 70)
    
    if activities:
        for act in activities:
            print(f"\n📌 ID: {act['id']}")
            print(f"   Titre: {act['titre']}")
            print(f"   Sport: {act['sport']}")
            print(f"   Date: {act['date_activite']}")
            print(f"   User ID: {act['id_user']}")
    else:
        print("\n⚠️  Aucune activité trouvée!")
        print("💡 Réinitialisez la base : python src/utils/reset_database.py")
    
    print("\n" + "=" * 70)
    cursor.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
