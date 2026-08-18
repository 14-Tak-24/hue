# Firebase Authentication Configuration Guide

## Overview
This guide provides step-by-step instructions for configuring Firebase Authentication for the Tiapma'atzu platform using the Firebase Console (free tier).

## API Server Authentication Integration
The Python API server now includes Firebase Authentication middleware:

- **Token Verification**: `/api/auth/verify` endpoint for testing tokens
- **Protected Endpoints**: Write operations require authentication (`@require_auth` decorator)
- **Error Handling**: Comprehensive token validation and error responses

## Console Configuration Steps

### 1. Access Firebase Console
1. Go to: https://console.firebase.google.com/project/tiapmaatzu/overview
2. Navigate to **Build** → **Authentication**

### 2. Enable Authentication
1. Click **Get Started** button
2. Select authentication providers to enable

### 3. Configure Sign-in Providers

#### Email/Password (Recommended)
1. Click on **Email/Password** in Sign-in method tab
2. Enable **Email/password** toggle
3. Click **Save**

#### Google Sign-in (Recommended)
1. Click on **Google** in Sign-in method tab
2. Enable **Google** toggle
3. Configure project details:
   - **Project support email**: `mac.nazarene@HueMan-i-Terryleaders.com`
   - **Project public-facing name**: `Tiapma'atzu Platform`
4. Add **Authorized domains**:
   - `tiapmaatzu.web.app`
   - `localhost` (for development)
   - Your API server domain (when deployed)
5. Add **Authorized redirect URIs**:
   - `https://tiapmaatzu.web.app/__/auth/handler`
   - `http://localhost:5000/__/auth/handler` (for development)
6. Click **Save**

#### Anonymous Authentication (Optional)
1. Click on **Anonymous** in Sign-in method tab
2. Enable **Anonymous** toggle
3. Click **Save**

### 4. Update Firestore Security Rules
Update your `firestore.rules` to require authentication for write operations:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Souls collection - public read, authenticated write
    match /souls/{soulId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Tributes collection - authenticated read/write
    match /tributes/{tributeId} {
      allow read, write: if request.auth != null;
    }
    
    // Financial data - authenticated read/write
    match /financial/{docId} {
      allow read, write: if request.auth != null;
    }
    
    // Analytics - public read, authenticated write
    match /analytics/{docId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

Deploy updated rules:
```bash
firebase deploy --only firestore:rules
```

## Testing Authentication

### 1. Create Test User
1. Go to Firebase Console → Authentication → Users
2. Click **Add user**
3. Enter test email and password
4. Click **Create user**

### 2. Test Token Verification
Use the Firebase Client SDK to obtain a token, then test with the API:

```bash
# Test token verification endpoint
curl -X POST http://localhost:5000/api/auth/verify \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -H "Content-Type: application/json"
```

### 3. Test Protected Endpoints
```bash
# Test adding tribute (requires auth)
curl -X POST http://localhost:5000/api/financial/tributes \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "soul_id": "soul_001",
    "amount": 100.0,
    "impact_area": "content",
    "platform": "twitter"
  }'
```

## Client-Side Integration

### Firebase SDK Setup
```html
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-auth-compat.js"></script>

<script>
  const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "tiapmaatzu.firebaseapp.com",
    projectId: "tiapmaatzu",
    storageBucket: "tiapmaatzu.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
  };

  firebase.initializeApp(firebaseConfig);
</script>
```

### Authentication Functions
```javascript
// Email/Password Sign Up
async function signUp(email, password) {
  try {
    const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
    const token = await userCredential.user.getIdToken();
    return token;
  } catch (error) {
    console.error('Sign up error:', error);
    throw error;
  }
}

// Email/Password Sign In
async function signIn(email, password) {
  try {
    const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
    const token = await userCredential.user.getIdToken();
    return token;
  } catch (error) {
    console.error('Sign in error:', error);
    throw error;
  }
}

// Google Sign In
async function signInWithGoogle() {
  try {
    const provider = new firebase.auth.GoogleAuthProvider();
    const userCredential = await firebase.auth().signInWithPopup(provider);
    const token = await userCredential.user.getIdToken();
    return token;
  } catch (error) {
    console.error('Google sign in error:', error);
    throw error;
  }
}

// Sign Out
async function signOut() {
  try {
    await firebase.auth().signOut();
  } catch (error) {
    console.error('Sign out error:', error);
    throw error;
  }
}

// Make Authenticated API Call
async function authenticatedApiCall(endpoint, data = {}) {
  const user = firebase.auth().currentUser;
  if (!user) {
    throw new Error('No authenticated user');
  }
  
  const token = await user.getIdToken();
  
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
}
```

## Protected Endpoints

The following API endpoints now require authentication:

### Write Operations
- `POST /api/financial/tributes` - Add tribute transaction
- `POST /api/firestore/sync` - Sync souls to Firestore

### Read Operations (Public)
- `GET /api/souls` - Get all souls
- `GET /api/financial/summary` - Get financial summary
- `GET /api/analytics/*` - All analytics endpoints

### Authentication Endpoints
- `POST /api/auth/verify` - Verify Firebase token
- `GET /health` - Health check (public)

## Security Best Practices

1. **Token Storage**: Store tokens securely (httpOnly cookies or secure storage)
2. **Token Refresh**: Implement automatic token refresh
3. **HTTPS**: Always use HTTPS in production
4. **Token Expiration**: Handle token expiration gracefully
5. **Error Handling**: Provide clear error messages for auth failures
6. **Rate Limiting**: Implement rate limiting on auth endpoints

## Troubleshooting

### "Unauthorized domain" error
- Add your domain to authorized domains in Google sign-in settings
- Ensure redirect URIs are correctly configured

### Token verification fails
- Ensure Firebase Admin SDK is initialized with correct credentials
- Check that the token hasn't expired (tokens expire in 1 hour)
- Verify the token is being sent correctly in the Authorization header

### Firestore rules blocking access
- Test rules in Firebase Console Rules Playground
- Ensure rules allow authenticated users to read/write
- Check that auth condition is correctly implemented

### "No authorization header provided"
- Ensure you're sending the Authorization header
- Format should be: `Authorization: Bearer <token>`

## Next Steps

1. ✅ **Configure Authentication Providers** - Follow console setup steps
2. ✅ **Update Firestore Rules** - Deploy updated security rules
3. ✅ **Test Authentication Flow** - Create test user and verify tokens
4. ✅ **Implement Client-Side Auth** - Add Firebase SDK to your frontend
5. ✅ **Deploy API Server** - Use deployment guide for production setup

## Support

- Firebase Console: https://console.firebase.google.com
- Firebase Auth Documentation: https://firebase.google.com/docs/auth
- API Deployment Guide: See `deploy/API_DEPLOYMENT_GUIDE.md`