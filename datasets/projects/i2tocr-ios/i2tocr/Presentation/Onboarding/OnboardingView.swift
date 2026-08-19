//
//  OnboardingView.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI

// MARK: - Model
struct OnboardingPage: Identifiable {
    let id = UUID()
    let systemIcon: String
    let iconColor: Color
    let title: String
    let subtitle: String
    let description: String
}

// MARK: - ViewModel
@MainActor
final class OnboardingViewModel: ObservableObject {
    @Published var currentPage = 0

    let pages: [OnboardingPage] = [
        OnboardingPage(
            systemIcon: "doc.viewfinder.fill",
            iconColor: .tlPrimary,
            title: "Smart Text Reader",
            subtitle: "I2TOCR",
            description: "Using artificial intelligence, extract text from any image in less than a few seconds"
        ),
        OnboardingPage(
            systemIcon: "eye.fill",
            iconColor: .tlAccent,
            title: "Vision AI",
            subtitle: "Local Processing",
            description: "With Apple's Vision technology, process texts directly on your device without needing an internet connection"
        ),
        OnboardingPage(
            systemIcon: "server.rack",
            iconColor: Color(hex: "#FD79A8"),
            title: "Cloud OCR",
            subtitle: "High Accuracy",
            description: "Extract even handwritten notes and complex texts with exceptional accuracy using advanced OCR server"
        )
    ]

    var isLastPage: Bool {
        currentPage == pages.count - 1
    }

    func nextPage() {
        if !isLastPage {
            withAnimation(.spring(duration: 0.5)) {
                currentPage += 1
            }
        }
    }
}

// MARK: - View
struct OnboardingView: View {
    @StateObject private var viewModel = OnboardingViewModel()
    @EnvironmentObject var router: AppRouter

    var body: some View {
        ZStack {
            // Background
            Color.tlBackground.ignoresSafeArea()

            // Animated background blobs
            GeometryReader { geo in
                Circle()
                    .fill(Color.tlPrimary.opacity(0.15))
                    .frame(width: 300, height: 300)
                    .blur(radius: 80)
                    .offset(
                        x: CGFloat(viewModel.currentPage) * -60,
                        y: -100
                    )
                    .animation(.easeInOut(duration: 0.8), value: viewModel.currentPage)
                    .frame(width: geo.size.width, alignment: .trailing)

                Circle()
                    .fill(Color.tlAccent.opacity(0.12))
                    .frame(width: 250, height: 250)
                    .blur(radius: 70)
                    .offset(
                        x: CGFloat(viewModel.currentPage) * 50,
                        y: 200
                    )
                    .animation(.easeInOut(duration: 0.8), value: viewModel.currentPage)
                    .frame(width: geo.size.width, alignment: .leading)
            }

            VStack(spacing: 0) {
                // Skip button
                HStack {
                    Spacer()
                    Button("Skip") {
                        router.finishOnboarding()
                    }
                    .font(TLFont.body(15))
                    .foregroundStyle(Color.tlTextSecondary)
                    .padding(.horizontal, 24)
                    .padding(.top, 16)
                }

                // Pages
                TabView(selection: $viewModel.currentPage) {
                    ForEach(Array(viewModel.pages.enumerated()), id: \.element.id) { index, page in
                        OnboardingPageView(page: page)
                            .tag(index)
                    }
                }
                .tabViewStyle(.page(indexDisplayMode: .never))
                .animation(.spring(duration: 0.5), value: viewModel.currentPage)

                // Bottom controls
                VStack(spacing: 24) {
                    // Page dots
                    HStack(spacing: 8) {
                        ForEach(0..<viewModel.pages.count, id: \.self) { index in
                            Capsule()
                                .fill(index == viewModel.currentPage ? Color.tlPrimary : Color.tlTextSecondary.opacity(0.3))
                                .frame(
                                    width: index == viewModel.currentPage ? 28 : 8,
                                    height: 8
                                )
                                .animation(.spring(duration: 0.4), value: viewModel.currentPage)
                        }
                    }

                    // Action button
                    Button {
                        if viewModel.isLastPage {
                            router.finishOnboarding()
                        } else {
                            viewModel.nextPage()
                        }
                    } label: {
                        HStack(spacing: 10) {
                            Text(viewModel.isLastPage ? "Get Started" : "Next")
                            Image(systemName: viewModel.isLastPage ? "arrow.right.circle.fill" : "chevron.left")
                        }
                    }
                    .buttonStyle(PrimaryButtonStyle())
                    .padding(.horizontal, 32)
                }
                .padding(.bottom, 48)
            }
        }
        .environment(\.layoutDirection, .rightToLeft)
    }
}

// MARK: - Page Content View
struct OnboardingPageView: View {
    let page: OnboardingPage
    @State private var appeared = false

    var body: some View {
        VStack(spacing: 32) {
            Spacer()

            // Icon
            ZStack {
                Circle()
                    .fill(page.iconColor.opacity(0.15))
                    .frame(width: 140, height: 140)

                Circle()
                    .fill(page.iconColor.opacity(0.1))
                    .frame(width: 110, height: 110)

                Image(systemName: page.systemIcon)
                    .font(.system(size: 52))
                    .foregroundStyle(page.iconColor)
                    .symbolEffect(.bounce, value: appeared)
            }
            .scaleEffect(appeared ? 1 : 0.6)
            .opacity(appeared ? 1 : 0)
            .animation(.spring(duration: 0.7, bounce: 0.4), value: appeared)

            // Text
            VStack(spacing: 12) {
                Text(page.subtitle)
                    .font(TLFont.body(14))
                    .foregroundStyle(page.iconColor)
                    .tracking(2)
                    .textCase(.uppercase)

                Text(page.title)
                    .font(TLFont.display(30))
                    .foregroundStyle(Color.tlText)
                    .multilineTextAlignment(.center)

                Text(page.description)
                    .font(TLFont.body(16))
                    .foregroundStyle(Color.tlTextSecondary)
                    .multilineTextAlignment(.center)
                    .lineSpacing(6)
                    .padding(.horizontal, 32)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .offset(y: appeared ? 0 : 30)
            .opacity(appeared ? 1 : 0)
            .animation(.easeOut(duration: 0.6).delay(0.2), value: appeared)

            Spacer()
        }
        .onAppear {
            appeared = true
        }
        .onDisappear {
            appeared = false
        }
    }
}
