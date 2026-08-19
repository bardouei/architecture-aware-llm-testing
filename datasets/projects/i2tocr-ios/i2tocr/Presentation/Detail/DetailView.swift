//
//  DetailView.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI

@MainActor
final class DetailViewModel: ObservableObject {
    @Published var isCopied = false

    let item: OCRItem

    init(item: OCRItem) {
        self.item = item
    }

    func copyText() {
        UIPasteboard.general.string = item.extractedText
        withAnimation(.spring(duration: 0.3)) {
            isCopied = true
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            withAnimation {
                self.isCopied = false
            }
        }
    }

    func shareText() {
        let activityVC = UIActivityViewController(
            activityItems: [item.extractedText],
            applicationActivities: nil
        )
        if let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
           let rootVC = windowScene.windows.first?.rootViewController {
            rootVC.present(activityVC, animated: true)
        }
    }
}

struct DetailView: View {
    let item: OCRItem
    @StateObject private var viewModel: DetailViewModel
    @Environment(\.dismiss) private var dismiss
    @State private var imageScale: CGFloat = 1.0
    @State private var showFullImage = false

    init(item: OCRItem) {
        self.item = item
        _viewModel = StateObject(wrappedValue: DetailViewModel(item: item))
    }

    var body: some View {
        ZStack {
            Color.tlBackground.ignoresSafeArea()

            ScrollView {
                VStack(spacing: 0) {
                    // Image Section
                    imageSection

                    // Content
                    VStack(alignment: .leading, spacing: 20) {
                        // Meta info
                        metaInfo

                        Divider()
                            .background(Color.tlSurface2)

                        // Extracted text
                        textSection
                    }
                    .padding(20)
                }
            }

            // Full screen image overlay
            if showFullImage, let imageData = item.imageData, let uiImage = UIImage(data: imageData) {
                Color.black.opacity(0.95)
                    .ignoresSafeArea()
                    .onTapGesture { withAnimation { showFullImage = false } }

                Image(uiImage: uiImage)
                    .resizable()
                    .scaledToFit()
                    .padding(20)
                    .transition(.scale)
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .navigationTitle("Extracted Text")
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                Button {
                    viewModel.shareText()
                } label: {
                    Image(systemName: "square.and.arrow.up")
                        .foregroundStyle(Color.tlPrimaryLight)
                }
            }
        }
        .environment(\.layoutDirection, .rightToLeft)
    }

    // MARK: - Image Section
    private var imageSection: some View {
        ZStack(alignment: .bottomTrailing) {
            if let imageData = item.imageData, let uiImage = UIImage(data: imageData) {
                Image(uiImage: uiImage)
                    .resizable()
                    .scaledToFill()
                    .frame(maxWidth: .infinity)
                    .frame(height: 260)
                    .clipped()
                    .onTapGesture {
                        withAnimation(.spring(duration: 0.4)) {
                            showFullImage = true
                        }
                    }
            } else {
                Rectangle()
                    .fill(Color.tlSurface2)
                    .frame(height: 260)
                    .overlay(
                        Image(systemName: "photo")
                            .font(.system(size: 44))
                            .foregroundStyle(Color.tlTextSecondary.opacity(0.3))
                    )
            }

            // Expand hint
            Label("Zoom", systemImage: "arrow.up.left.and.arrow.down.right")
                .font(TLFont.body(11))
                .foregroundStyle(Color.white)
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .background(Color.black.opacity(0.55), in: Capsule())
                .padding(14)
        }
        .frame(height: 260)
    }

    // MARK: - Meta Info
    private var metaInfo: some View {
        HStack(spacing: 12) {
            // OCR Type badge
            HStack(spacing: 6) {
                Image(systemName: item.ocrType == .vision ? "eye.fill" : "server.rack")
                    .font(.system(size: 12))
                Text(item.ocrType == .vision ? "Vision AI" : "Cloud OCR")
                    .font(TLFont.body(13))
            }
            .foregroundStyle(Color.tlPrimaryLight)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(Color.tlPrimary.opacity(0.15), in: Capsule())

            Spacer()

            // Date
            Label(item.createdAt.formatted(date: .abbreviated, time: .shortened), systemImage: "clock")
                .font(TLFont.body(12))
                .foregroundStyle(Color.tlTextSecondary)
        }
    }

    // MARK: - Text Section
    private var textSection: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                Label("Extracted Text", systemImage: "text.alignleft")
                    .font(TLFont.heading(16))
                    .foregroundStyle(Color.tlText)

                Spacer()

                // Copy button
                Button {
                    viewModel.copyText()
                } label: {
                    HStack(spacing: 5) {
                        Image(systemName: viewModel.isCopied ? "checkmark" : "doc.on.doc")
                            .font(.system(size: 13))
                        Text(viewModel.isCopied ? "Copied" : "Copy")
                            .font(TLFont.body(13))
                    }
                    .foregroundStyle(viewModel.isCopied ? Color.tlSuccess : Color.tlPrimaryLight)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(
                        (viewModel.isCopied ? Color.tlSuccess : Color.tlPrimary).opacity(0.12),
                        in: Capsule()
                    )
                }
                .buttonStyle(.plain)
            }

            // Text content
            Text(item.extractedText)
                .font(TLFont.mono(14))
                .foregroundStyle(Color.tlText)
                .lineSpacing(6)
                .textSelection(.enabled)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(16)
                .glassCard()

            // Char count
            Text("\(item.extractedText.count) characters · \(item.extractedText.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }.count) words")
                .font(TLFont.body(12))
                .foregroundStyle(Color.tlTextSecondary.opacity(0.6))
        }
    }
}
