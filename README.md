# Firebase Project - tiapmaatzu

This directory contains the Firebase configuration for the tiapmaatzu project.

## Setup Status

✅ **Firebase Hosting**: Deployed and available at https://tiapmaatzu.web.app
✅ **Cloud Firestore**: Deployed with security rules and indexes
⚠️ **Realtime Database**: Requires manual setup in Firebase Console

## Project Configuration

- **Project ID**: tiapmaatzu
- **Project Number**: 942886003749
- **Auth Domain**: tiapmaatzu.firebaseapp.com
- **Storage Bucket**: tiapmaatzu.firebasestorage.app

## Services Configured

### 1. Firebase Hosting
- **Public Directory**: `public/`
- **URL**: https://tiapmaatzu.web.app
- **Status**: Active and deployed

### 2. Cloud Firestore
- **Rules File**: `firestore.rules`
- **Indexes File**: `firestore.indexes.json`
- **Status**: Active and deployed
- **Current Rules**: All reads/writes disabled (for security)

### 3. Realtime Database
- **Rules File**: `database.rules.json`
- **Status**: Requires setup in Firebase Console
- **Current Rules**: All reads/writes disabled (for security)

## Firebase Configuration

Web app configuration is available in `public/firebase-config.js`:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyAP8jWmqSHUVtJXXMqikXtKh1MJOTuuPoY",
  authDomain: "tiapmaatzu.firebaseapp.com",
  projectId: "tiapmaatzu",
  storageBucket: "tiapmaatzu.firebasestorage.app",
  messagingSenderId: "942886003749",
  appId: "1:942886003749:web:9e8aec27fb70313e6acbcc",
  measurementId: "G-QYCB24W7HP"
};
```

## Next Steps

### For Realtime Database Setup:
1. Visit Firebase Console: https://console.firebase.google.com/project/tiapmaatzu
2. Navigate to Realtime Database
3. Click "Create Database"
4. Select your preferred location
5. Start in test mode or locked mode
6. The security rules will be automatically deployed from `database.rules.json`

### For Customizing Security Rules:
- **Firestore**: Edit `firestore.rules` and run `firebase deploy --only firestore`
- **Realtime Database**: Edit `database.rules.json` and run `firebase deploy --only database`

### For Adding Firebase to Your Web App:
```javascript
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
import { getDatabase } from "firebase/database";

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const firestore = getFirestore(app);
const realtimeDatabase = getDatabase(app);
```

## Service Account

The service account key file has been moved to this directory for admin SDK access:
- `tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json`

⚠️ **Security Note**: Keep this file secure and never commit it to version control.

## Deployment Commands

```bash
# Deploy all services
firebase deploy

# Deploy specific services
firebase deploy --only hosting
firebase deploy --only firestore
firebase deploy --only database

# View current deployment
firebase hosting:info
```

## Project Console

- **Firebase Console**: https://console.firebase.google.com/project/tiapmaatzu/overview
- **Hosting URL**: https://tiapmaatzu.web.app
