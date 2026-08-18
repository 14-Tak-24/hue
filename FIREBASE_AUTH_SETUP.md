# Firebase Authentication Setup Guide (Free Tier)

Since Firebase Cloud Functions require the Blaze plan, this guide shows how to set up Firebase Authentication manually through the Firebase Console (available on the free Spark plan).

## Prerequisites

- Firebase project: `tiapmaatzu`
- Firebase Console access: https://console.firebase.google.com/project/tiapmaatzu/overview
- Project already has Firestore and Hosting configured

## Step-by-Step Setup

### 1. Enable Authentication

1. Go to Firebase Console: https://console.firebase.google.com/project/tiapmaatzu/overview
2. Click on **Build** → **Authentication** in the left sidebar
3. Click **Get Started**
4. Select your authentication method(s)

### 2. Enable Sign-in Providers

#### Email/Password Authentication
1. In the **Sign-in method** tab
2. Click on **Email/Password**
3. Enable **Email/password** toggle
4. Click **Save**

#### Google Sign-in
1. In the **Sign-in method** tab
2. Click on **Google**
3. Enable **Google** toggle
4. Enter a **Project support email**: `mac.nazarene@HueMan-i-Terryleaders.com`
5. Enter **Project public-facing name**: `Tiapma'atzu Platform`
6. Add **Authorized domains**:
   - `tiapmaatzu.web.app`
   - `localhost` (for development)
7. Click **Save**

#### Anonymous Authentication (Optional)
1. In the **Sign-in method** tab
2. Click on **Anonymous**
3. Enable **Anonymous** toggle
4. Click **Save**

### 3. Configure Authorized Redirect URIs

1. In the **Google** sign-in method settings
2. Under **Authorized redirect URIs**, add:
   - `https://tiapmaatzu.web.app/__/auth/handler`
   - `http://localhost:5000/__/auth/handler` (for development)

### 4. Set Up User Management

You can manage users through the Firebase Console:

1. Go to **Build** → **Authentication** → **Users** tab
2. Click **Add user** to manually create users
3. Or enable user registration through your API/ frontend

### 5. Configure Firestore Security Rules for Auth

Update your `firestore.rules` to use authentication:

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

Deploy the updated rules:
```bash
firebase deploy --only firestore:rules
```

## Using Firebase Auth with the Python API Server

### Client-Side Integration

Your frontend can use the Firebase Client SDK to authenticate users:

```html
<!-- Add Firebase SDKs -->
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

  // Email/Password Sign Up
  async function signUp(email, password) {
    try {
      const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
      const token = await userCredential.user.getIdToken();
      // Use token with your Python API
      return token;
    } catch (error) {
      console.error(error);
    }
  }

  // Email/Password Sign In
  async function signIn(email, password) {
    try {
      const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
      const token = await userCredential.user.getIdToken();
      // Use token with your Python API
      return token;
    } catch (error) {
      console.error(error);
    }
  }

  // Google Sign In
  async function signInWithGoogle() {
    try {
      const provider = new firebase.auth.GoogleAuthProvider();
      const userCredential = await firebase.auth().signInWithPopup(provider);
      const token = await userCredential.user.getIdToken();
      // Use token with your Python API
      return token;
    } catch (error) {
      console.error(error);
    }
  }
</script>
```

### Server-Side Token Verification

Update your Python API server to verify Firebase tokens:

```python
from firebase_admin import auth

@app.route('/api/protected', methods=['GET'])
def protected_endpoint():
    """Protected endpoint requiring authentication"""
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'No token provided'}), 401
    
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        # User is authenticated, proceed with request
        return jsonify({
            'message': 'Success',
            'user_id': uid
        })
        
    except auth.InvalidIdTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Testing Authentication

### Test Email/Password Auth

1. Go to Firebase Console → Authentication → Users
2. Click **Add user**
3. Enter email and password
4. Test sign-in using the client SDK

### Test Google Auth

1. Ensure your Google OAuth consent screen is configured
2. Test sign-in using the Google provider

## Migration from Cloud Functions

Since we're using the Python API server instead of Cloud Functions:

1. **User Management**: Use Firebase Console or Admin SDK via Python
2. **Custom Claims**: Use Firebase Admin SDK in Python
3. **Trigger Functions**: Implement as scheduled jobs in Python
4. **Callable Functions**: Implement as REST API endpoints

## Cost Comparison

| Feature | Cloud Functions (Blaze) | Python API Server (Free) |
|---------|------------------------|---------------------------|
| Authentication | ✅ Free | ✅ Free |
| Firestore | ✅ Free tier | ✅ Free tier |
| Hosting | ✅ Free tier | ✅ Free tier |
| Custom Backend | ❌ Requires Blaze | ✅ Free (any server) |
| Scheduled Tasks | ❌ Requires Blaze | ✅ Free (cron/systemd) |
| Webhooks | ❌ Requires Blaze | ✅ Free (Flask) |

## Next Steps

1. Set up authentication providers in Firebase Console
2. Update Firestore security rules to use auth
3. Add token verification to your Python API endpoints
4. Implement client-side authentication in your frontend
5. Test the authentication flow end-to-end

## Troubleshooting

### "Unauthorized domain" error
- Add your domain to authorized domains in Google sign-in settings
- Ensure redirect URIs are correctly configured

### Token verification fails
- Ensure Firebase Admin SDK is initialized with correct credentials
- Check that the token hasn't expired
- Verify the token is being sent correctly in the Authorization header

### Firestore rules blocking access
- Test rules in Firebase Console Rules Playground
- Ensure rules allow authenticated users to read/write
- Check that auth condition is correctly implemented

## Support

For Firebase-specific issues:
- Firebase Console: https://console.firebase.google.com
- Firebase Documentation: https://firebase.google.com/docs/auth

For Tiapma'atzu platform support:
- Check `PROJECT_STATUS.md` for current platform status
- Review API documentation in `api_server.py`
