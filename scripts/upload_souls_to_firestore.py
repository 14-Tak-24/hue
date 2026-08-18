"""
Upload Souls Data to Firestore
Script to upload the 28 souls entities to Firebase Firestore
"""

import sys
import os
from pathlib import Path
import json

# Add the src directory to the path for package imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def upload_souls_to_firestore():
    """Upload souls data to Firestore using Firebase Admin SDK"""
    
    try:
        # Import Firebase Admin SDK
        import firebase_admin
        from firebase_admin import credentials, firestore
        from modules.souls_manager import SoulsManager
        
        print("🔥 Uploading Souls Data to Firestore...")
        
        # Initialize Firebase Admin with service account
        service_account_path = Path(__file__).parent / "tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json"
        
        if not service_account_path.exists():
            print(f"❌ Service account file not found: {service_account_path}")
            return False
        
        cred = credentials.Certificate(str(service_account_path))
        firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        db = firestore.client()
        
        # Load souls data
        data_path = Path(__file__).parent / "src" / "data" / "souls_entities.json"
        souls_manager = SoulsManager(str(data_path))
        all_souls = souls_manager.get_all_souls()
        
        print(f"📚 Loaded {len(all_souls)} souls from local data")
        
        # Upload each soul to Firestore
        batch = db.batch()
        souls_collection = db.collection('souls')
        
        uploaded_count = 0
        for soul in all_souls:
            # Create soul document
            soul_ref = souls_collection.document(soul.id)
            
            soul_data = {
                'id': soul.id,
                'name': soul.name,
                'gender': soul.gender,
                'archetype': soul.archetype,
                'bio': soul.bio,
                'sensory': soul.sensory,
                'voice': soul.voice,
                'hooks': soul.hooks,
                'desires': soul.desires,
                'kinks': soul.kinks,
                'tribute_impact': soul.tribute_impact,
                'shadow_practice': soul.shadow_practice,
                'email': soul.email,
                'image': soul.image,
                'rarity': soul.rarity,
                'platforms': soul.platforms,
                'tier': soul.tier,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            batch.set(soul_ref, soul_data)
            uploaded_count += 1
            
            # Commit batch every 10 souls to avoid batch size limits
            if uploaded_count % 10 == 0:
                batch.commit()
                print(f"✅ Uploaded {uploaded_count}/{len(all_souls)} souls...")
                batch = db.batch()
        
        # Commit remaining souls
        batch.commit()
        
        print(f"🎉 Successfully uploaded {uploaded_count} souls to Firestore!")
        
        # Verify upload
        print("🔍 Verifying upload...")
        souls_ref = db.collection('souls')
        docs = souls_ref.stream()
        verified_count = sum(1 for doc in docs)
        
        print(f"✅ Verification complete: {verified_count} souls in Firestore")
        
        # Upload metadata
        metadata_collection = db.collection('config')
        metadata_ref = metadata_collection.document('souls_metadata')
        
        metadata_data = {
            'total_souls': len(all_souls),
            'last_updated': firestore.SERVER_TIMESTAMP,
            'version': '1.0',
            'archetypes': souls_manager.get_metadata().get('archetypes', []),
            'rarity_distribution': souls_manager.get_metadata().get('rarity_distribution', {}),
            'platforms': souls_manager.get_platforms()
        }
        
        metadata_ref.set(metadata_data)
        print("✅ Souls metadata uploaded to config collection")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading souls to Firestore: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution function"""
    print("=" * 60)
    print("Tiapma'atzu Platform - Souls Data Upload to Firestore")
    print("=" * 60)
    
    success = upload_souls_to_firestore()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Upload completed successfully!")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("1. Visit Firebase Console to verify souls data")
        print("2. Test Firestore queries from your application")
        print("3. Set up real-time sync for client applications")
        print("\n🔗 Firebase Console:")
        print("https://console.firebase.google.com/project/tiapmaatzu/firestore")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ Upload failed. Please check the errors above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())