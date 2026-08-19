//
//  BiometricAuthView.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI
@preconcurrency import LocalAuthentication

// MARK: - ViewModel
@MainActor
final class BiometricAuthViewModel: ObservableObject {
    @Published var isAuthenticating = false
    @Published var authError: String?
    @Published var biometricType: LABiometryType = .none
    @Published var showRetryButton = false

    private let context = LAContext()

    init() {
        detectBiometricType()
    }

    private func detectBiometricType() {
        var error: NSError?
        if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            biometricType = context.biometryType
        }
    }

    var biometricIconName: String {
        switch biometricType {
        case .faceID:   return "faceid"
        case .touchID:  return "touchid"
        default:        return "lock.shield.fill"
        }
    }

    var biometricLabel: String {
        switch biometricType {
        case .faceID:  return "Face ID"
        case .touchID: return "Touch ID"
        default:       return "Password"
        }
    }

    func startAuthentication(onSuccess: @escaping @MainActor () -> Void) {
        isAuthenticating = true
        authError = nil
        showRetryButton = false

        let freshContext = LAContext()
        var error: NSError?

        if freshContext.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            authenticateWithBiometrics(context: freshContext, onSuccess: onSuccess)
        } else {
            authenticateWithPasscode(context: freshContext, onSuccess: onSuccess)
        }
    }

    private func authenticateWithBiometrics(context: LAContext, onSuccess: @escaping @MainActor () -> Void) {
        let reason = "Please verify your identity to access the app"

        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { [weak self] success, error in
            Task { @MainActor [weak self] in
                self?.isAuthenticating = false
                if success {
                    onSuccess()
                } else if let error = error as? LAError {
                    self?.handleBiometricError(error, context: context, onSuccess: onSuccess)
                } else {
                    self?.authenticateWithPasscode(context: context, onSuccess: onSuccess)
                }
            }
        }
    }

    private func authenticateWithPasscode(context: LAContext, onSuccess: @escaping @MainActor () -> Void) {
        let reason = "Please enter your device passcode to access the app"
        
        context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: reason) { [weak self] success, error in
            DispatchQueue.main.async {
                self?.isAuthenticating = false
                if success {
                    print("🟢 Passcode authentication SUCCESS")
                    Task { @MainActor in
                        onSuccess()
                    }
                } else {
                    print("🟢 Passcode authentication FAILED")
                    self?.authError = "Authentication failed"
                    self?.showRetryButton = true
                }
            }
        }
    }

    private func handleBiometricError(_ error: LAError, context: LAContext, onSuccess: @escaping @MainActor () -> Void) {
        switch error.code {
        case .userCancel, .systemCancel, .appCancel:
            authError = "Authentication cancelled"
            showRetryButton = true

        case .userFallback:
            authenticateWithPasscode(context: context, onSuccess: onSuccess)

        case .authenticationFailed:
            authError = "Authentication failed. Please try again"
            showRetryButton = true

        case .biometryLockout:
            authError = "Biometric lockout activated. Use your device passcode"
            authenticateWithPasscode(context: context, onSuccess: onSuccess)

        case .biometryNotAvailable, .biometryNotEnrolled:
            authenticateWithPasscode(context: context, onSuccess: onSuccess)

        case .passcodeNotSet:
            authError = "Device passcode not set. Please set a passcode in settings"
            showRetryButton = false

        default:
            authenticateWithPasscode(context: context, onSuccess: onSuccess)
        }
    }
}

// MARK: - View
struct BiometricAuthView: View {
    @StateObject private var viewModel = BiometricAuthViewModel()
    @EnvironmentObject var router: AppRouter
    @State private var pulseAnimation = false
    @State private var iconScale = false

    var body: some View {
        ZStack {
            // Background
            Color.tlBackground.ignoresSafeArea()

            // Background gradient blob
            RadialGradient(
                colors: [Color.tlPrimary.opacity(0.25), Color.clear],
                center: .center,
                startRadius: 10,
                endRadius: 350
            )
            .ignoresSafeArea()

            VStack(spacing: 0) {
                Spacer()

                // App Logo area
                VStack(spacing: 16) {
                    Image(systemName: "doc.viewfinder")
                        .font(.system(size: 44, weight: .light))
                        .foregroundStyle(Color.tlPrimaryLight)

                    Text("I2TOCR")
                        .font(TLFont.display(32))
                        .foregroundStyle(Color.tlText)
                }
                .padding(.bottom, 64)

                // Biometric Icon
                ZStack {
                    // Pulse rings
                    ForEach(0..<3, id: \.self) { i in
                        Circle()
                            .stroke(Color.tlPrimary.opacity(0.15 - Double(i) * 0.04), lineWidth: 1)
                            .frame(
                                width: CGFloat(100 + i * 40),
                                height: CGFloat(100 + i * 40)
                            )
                            .scaleEffect(pulseAnimation ? 1.1 : 1.0)
                            .animation(
                                .easeInOut(duration: 1.5)
                                .repeatForever(autoreverses: true)
                                .delay(Double(i) * 0.2),
                                value: pulseAnimation
                            )
                    }

                    // Icon background
                    Circle()
                        .fill(Color.tlSurface2)
                        .frame(width: 96, height: 96)
                        .overlay(
                            Circle()
                                .stroke(
                                    LinearGradient(
                                        colors: [Color.tlPrimary, Color.tlPrimaryLight.opacity(0.4)],
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    ),
                                    lineWidth: 1.5
                                )
                        )

                    Image(systemName: viewModel.biometricIconName)
                        .font(.system(size: 40))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [Color.tlPrimaryLight, Color.tlPrimary],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .scaleEffect(iconScale ? 1.1 : 1.0)
                        .animation(.spring(duration: 0.3), value: iconScale)
                }
                .padding(.bottom, 40)

                // Title & subtitle
                VStack(spacing: 10) {
                    Text("Login to App")
                        .font(TLFont.display(24))
                        .foregroundStyle(Color.tlText)

                    Text("Verify your identity with \(viewModel.biometricLabel)")
                        .font(TLFont.body(15))
                        .foregroundStyle(Color.tlTextSecondary)
                        .multilineTextAlignment(.center)
                }
                .padding(.bottom, 32)

                // Error message
                if let error = viewModel.authError {
                    HStack(spacing: 8) {
                        Image(systemName: "exclamationmark.triangle.fill")
                            .foregroundStyle(Color.tlError)
                        Text(error)
                            .font(TLFont.body(14))
                            .foregroundStyle(Color.tlError)
                    }
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .glassCard()
                    .padding(.horizontal, 32)
                    .padding(.bottom, 20)
                    .transition(.scale.combined(with: .opacity))
                }

                // Loading or Retry
                if viewModel.isAuthenticating {
                    ProgressView()
                        .tint(Color.tlPrimaryLight)
                        .scaleEffect(1.3)
                        .padding(.bottom, 20)
                }

                if viewModel.showRetryButton {
                    Button {
                        iconScale = true
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                            iconScale = false
                        }
                        viewModel.startAuthentication {
                            router.authenticationSuccess()
                        }
                    } label: {
                        Label("Try Again", systemImage: "arrow.clockwise")
                    }
                    .buttonStyle(PrimaryButtonStyle())
                    .padding(.horizontal, 48)
                }

                Spacer()
            }
        }
        .environment(\.layoutDirection, .rightToLeft)
        .onAppear {
            pulseAnimation = true
            Task { @MainActor in
                try? await Task.sleep(for: .milliseconds(600))
                viewModel.startAuthentication { router.authenticationSuccess() }
            }
        }
    }
}
