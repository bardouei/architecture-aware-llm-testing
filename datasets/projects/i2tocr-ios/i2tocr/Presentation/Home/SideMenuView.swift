//
//  SideMenuView.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI

struct SideMenuView: View {
    @Binding var isOpen: Bool
    @Binding var ocrMode: OCRMode

    var body: some View {
        ZStack(alignment: .trailing) {
            // Backdrop
            if isOpen {
                Color.black.opacity(0.5)
                    .ignoresSafeArea()
                    .onTapGesture { close() }
                    .transition(.opacity)
            }

            // Menu Panel
            if isOpen {
                HStack {
                    Spacer()
                    menuPanel
                        .frame(width: 280)
                        .transition(.move(edge: .trailing))
                }
            }
        }
        .animation(.spring(duration: 0.4, bounce: 0.1), value: isOpen)
        .environment(\.layoutDirection, .rightToLeft)
    }

    private var menuPanel: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header
            VStack(alignment: .leading, spacing: 6) {
                Image(systemName: "doc.viewfinder")
                    .font(.system(size: 36, weight: .light))
                    .foregroundStyle(Color.tlPrimaryLight)

                Text("I2TOCR")
                    .font(TLFont.display(22))
                    .foregroundStyle(Color.tlText)

                Text("Setting")
                    .font(TLFont.body(13))
                    .foregroundStyle(Color.tlTextSecondary)
            }
            .padding(.top, 70)
            .padding(.horizontal, 24)
            .padding(.bottom, 32)

            Divider()
                .background(Color.tlSurface2)
                .padding(.horizontal, 16)
                .padding(.bottom, 24)

            // OCR Mode Section
            VStack(alignment: .leading, spacing: 12) {
                Text("Chosse How to OCR")
                    .font(TLFont.body(12))
                    .foregroundStyle(Color.tlTextSecondary)
                    .tracking(1)
                    .padding(.horizontal, 24)

                ForEach(OCRMode.allCases, id: \.self) { mode in
                    OCRModeRow(
                        mode: mode,
                        isSelected: ocrMode == mode
                    ) {
                        withAnimation(.spring(duration: 0.3)) {
                            ocrMode = mode
                        }
                    }
                }
            }

            Spacer()

            // Version
            Text("V 1.0.0")
                .font(TLFont.body(12))
                .foregroundStyle(Color.tlTextSecondary.opacity(0.5))
                .padding(.horizontal, 24)
                .padding(.bottom, 40)
        }
        .frame(maxHeight: .infinity)
        .background(Color.tlSurface)
        .ignoresSafeArea()
    }

    private func close() {
        withAnimation(.spring(duration: 0.4)) {
            isOpen = false
        }
    }
}

// MARK: - OCR Mode Row
struct OCRModeRow: View {
    let mode: OCRMode
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 14) {
                ZStack {
                    RoundedRectangle(cornerRadius: 10)
                        .fill(isSelected ? Color.tlPrimary : Color.tlSurface2)
                        .frame(width: 40, height: 40)

                    Image(systemName: mode.icon)
                        .font(.system(size: 17))
                        .foregroundStyle(isSelected ? Color.white : Color.tlTextSecondary)
                }

                VStack(alignment: .leading, spacing: 2) {
                    Text(mode.label)
                        .font(TLFont.heading(15))
                        .foregroundStyle(isSelected ? Color.tlText : Color.tlTextSecondary)

                    Text(mode == .vision ? "Vision" : "OCR")
                        .font(TLFont.body(12))
                        .foregroundStyle(Color.tlTextSecondary.opacity(0.7))
                }

                Spacer()

                if isSelected {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(Color.tlPrimary)
                        .font(.system(size: 18))
                }
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 10)
        }
        .buttonStyle(.plain)
    }
}
