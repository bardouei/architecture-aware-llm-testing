//
//  RootView.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI

struct RootView: View {
    @EnvironmentObject var router: AppRouter
    
    var body: some View {
        ZStack {
            switch router.currentRoute {
            case .onboarding:
                OnboardingView()
                    .transition(.opacity)
            case .biometricAuth:
                BiometricAuthView()
                    .transition(.opacity)
            case .home:
                HomeView()
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing),
                        removal: .opacity
                    ))
            }
        }
        .animation(.easeInOut(duration: 0.4), value: router.currentRoute)
    }
}
