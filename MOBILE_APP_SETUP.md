# Flutter Mobile App Setup for Tiapma'atzu Platform

## Overview
This document outlines the setup and development plan for the Flutter mobile application for the Tiapma'atzu platform.

## Prerequisites
- Flutter SDK installed
- Android Studio / Xcode for mobile development
- Firebase project configured for mobile

## Project Structure
```
mobile/
├── lib/
│   ├── main.dart
│   ├── models/
│   │   ├── soul.dart
│   │   ├── user.dart
│   │   └── analytics.dart
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── signup_screen.dart
│   │   ├── souls/
│   │   │   ├── souls_list_screen.dart
│   │   │   ├── soul_detail_screen.dart
│   │   │   └── soul_search_screen.dart
│   │   ├── analytics/
│   │   │   ├── dashboard_screen.dart
│   │   │   └── platform_analytics_screen.dart
│   │   └── financial/
│   │       ├── financial_summary_screen.dart
│   │       └── tribute_screen.dart
│   ├── services/
│   │   ├── firebase_service.dart
│   │   ├── souls_service.dart
│   │   ├── auth_service.dart
│   │   └── analytics_service.dart
│   └── widgets/
│       ├── soul_card.dart
│       ├── platform_tag.dart
│       └── analytics_card.dart
├── android/
├── ios/
├── test/
└── pubspec.yaml
```

## Core Features

### 1. Authentication
- Email/password login
- Google Sign-In
- Anonymous guest access
- User profile management

### 2. Souls Management
- Browse all 28 souls
- Search and filter souls
- View detailed soul profiles
- Soul compatibility analysis
- Platform-specific content viewing

### 3. Analytics Dashboard
- Platform usage metrics
- Financial health overview
- Soul performance tracking
- Trending platforms display
- Real-time data updates

### 4. Financial Features
- Tribute recording
- Financial impact tracking
- Transaction history
- Budget monitoring

### 5. Content Integration
- AI-generated content viewing
- Platform-specific content
- Soul personality-based content
- Content scheduling

## Firebase Integration

### Required Dependencies
```yaml
dependencies:
  flutter:
    sdk: flutter
  firebase_core: ^2.24.2
  firebase_auth: ^4.16.0
  cloud_firestore: ^4.14.0
  firebase_analytics: ^10.7.4
  firebase_storage: ^11.6.0
```

### Configuration
1. Add `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
2. Configure Firebase in `main.dart`
3. Set up authentication providers
4. Configure Firestore security rules

## Development Plan

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Flutter project structure
- [ ] Configure Firebase integration
- [ ] Implement authentication flow
- [ ] Create basic navigation structure

### Phase 2: Core Features (Week 3-4)
- [ ] Implement souls listing and search
- [ ] Create soul detail views
- [ ] Add platform filtering
- [ ] Implement soul compatibility features

### Phase 3: Analytics (Week 5-6)
- [ ] Build analytics dashboard
- [ ] Add platform usage metrics
- [ ] Implement financial tracking
- [ ] Create soul performance views

### Phase 4: Advanced Features (Week 7-8)
- [ ] AI content integration
- [ ] Push notifications
- [ ] Offline support
- [ ] Performance optimization

## Testing Strategy
- Unit tests for business logic
- Widget tests for UI components
- Integration tests for Firebase services
- E2E tests for critical user flows

## Deployment
- Android: Google Play Store
- iOS: Apple App Store
- CI/CD pipeline setup
- Crashlytics integration
- Performance monitoring

## Next Steps
1. Install Flutter SDK
2. Create Flutter project: `flutter create tiapmaatzu_mobile`
3. Add Firebase dependencies
4. Configure platform-specific files
5. Implement authentication first
6. Build out core features incrementally

## Notes
- Follow Clean Architecture principles
- Implement proper state management (Provider/Riverpod)
- Ensure responsive design for different screen sizes
- Test on both iOS and Android platforms
- Maintain consistency with web platform design