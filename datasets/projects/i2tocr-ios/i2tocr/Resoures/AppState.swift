//
//  AppState.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI
import SwiftData

@MainActor
final class AppState {
    static let shared = AppState()
    let router = AppRouter()
    private init() {}
}

// MARK: - App Router
enum AppRoute: Equatable {
    case onboarding
    case biometricAuth
    case home
}

@MainActor
final class AppRouter: ObservableObject {
    @Published var currentRoute: AppRoute

    init() {
        let seen = UserDefaults.standard.bool(forKey: "hasSeenOnboarding")
        print("🔵 AppRouter init - hasSeenOnboarding: \(seen)")
        currentRoute = seen ? .biometricAuth : .onboarding
        print("🔵 Current route set to: \(currentRoute)")
    }

    func finishOnboarding() {
        print("🔵 finishOnboarding called")
        UserDefaults.standard.set(true, forKey: "hasSeenOnboarding")
        DispatchQueue.main.async {
            withAnimation(.easeInOut(duration: 0.5)) {
                self.currentRoute = .biometricAuth
                print("🔵 Route changed to: \(self.currentRoute)")
            }
        }
    }

    func authenticationSuccess() {
        print("🔵 authenticationSuccess called - current route: \(currentRoute)")
        DispatchQueue.main.async {
            withAnimation(.easeInOut(duration: 0.4)) {
                self.currentRoute = .home
                print("🔵 Route changed to: \(self.currentRoute)")
            }
        }
    }
}
