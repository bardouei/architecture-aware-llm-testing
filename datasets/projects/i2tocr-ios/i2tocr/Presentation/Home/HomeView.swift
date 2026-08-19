//
//  HomeView.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI
import PhotosUI

struct HomeView: View {
    @EnvironmentObject var container: DIContainer
    @StateObject private var viewModel: HomeViewModel
    @State private var cameraImage: UIImage?
    @State private var showCamera = false
    @State private var showFABMenu = false

    init() {
        // Will be replaced in body using container
        _viewModel = StateObject(wrappedValue: HomeViewModel(container: DIContainer.shared))
    }

    private let columns = [
        GridItem(.flexible(), spacing: 12),
        GridItem(.flexible(), spacing: 12)
    ]
    
    var body: some View {
        NavigationStack {
            ZStack {
                Color.tlBackground.ignoresSafeArea()

                // Main content
                VStack(spacing: 0) {
                    // Navigation Bar
                    navBar

                    // Content
                    if viewModel.items.isEmpty && !viewModel.isLoading {
                        emptyStateView
                    } else {
                        gridContent
                    }
                }

                // Loading overlay
                if viewModel.isLoading {
                    loadingOverlay
                }

                // FAB
                fabButton

                // Side Menu (on top)
                SideMenuView(
                    isOpen: $viewModel.showSideMenu,
                    ocrMode: $viewModel.ocrMode
                )
            }
            .environment(\.layoutDirection, .rightToLeft)
            .task { await viewModel.loadItems() }
            .alert("Error", isPresented: .init(
                get: { viewModel.errorMessage != nil },
                set: { if !$0 { viewModel.errorMessage = nil } }
            )) {
                Button("Ok") { viewModel.errorMessage = nil }
            } message: {
                Text(viewModel.errorMessage ?? "")
            }
            .sheet(isPresented: $showCamera) {
                CameraPickerView { image in
                    if let image {
                        Task { await viewModel.processCameraImage(image) }
                    }
                    showCamera = false
                }
            }
            .photosPicker(
                isPresented: $viewModel.showImagePicker,
                selection: $viewModel.selectedPhotoItem,
                matching: .images
            )
            // Add this modifier to HomeView body (after .photosPicker)
            .fileImporter(
                isPresented: $viewModel.showFilePicker,
                allowedContentTypes: [.image],
                allowsMultipleSelection: false
            ) { result in
                switch result {
                case .success(let urls):
                    guard let url = urls.first else { return }
                    Task { await viewModel.processSelectedFile(url) }
                case .failure(let error):
                    viewModel.errorMessage = error.localizedDescription
                }
            }
            .onChange(of: viewModel.selectedPhotoItem) { _, newItem in
                Task { await viewModel.processSelectedPhoto(newItem) }
            }
            .navigationDestination(isPresented: Binding(
                get: { viewModel.navigateToDetail != nil },
                set: { if !$0 { viewModel.navigateToDetail = nil } }
            )) {
                if let item = viewModel.navigateToDetail {
                    DetailView(item: item)
                }
            }
        }
    }

    // MARK: - Nav Bar
    private var navBar: some View {
        HStack {
            // Menu button (right side in RTL)
            Button {
                withAnimation(.spring(duration: 0.4)) {
                    viewModel.showSideMenu = true
                }
            } label: {
                ZStack {
                    Circle()
                        .fill(Color.tlSurface2)
                        .frame(width: 42, height: 42)
                    Image(systemName: "line.3.horizontal")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(Color.tlText)
                }
            }

            Spacer()

            VStack(spacing: 2) {
                Text("I2TOCR")
                    .font(TLFont.display(20))
                    .foregroundStyle(Color.tlText)

                // OCR Mode badge
                HStack(spacing: 4) {
                    Image(systemName: viewModel.ocrMode.icon)
                        .font(.system(size: 10))
                    Text(viewModel.ocrMode.label)
                        .font(TLFont.body(11))
                }
                .foregroundStyle(Color.tlPrimaryLight)
                .padding(.horizontal, 8)
                .padding(.vertical, 2)
                .background(Color.tlPrimary.opacity(0.2), in: Capsule())
            }

            Spacer()

            // Invisible spacer for balance
            Circle()
                .fill(Color.clear)
                .frame(width: 42, height: 42)
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .background(Color.tlBackground.opacity(0.95))
    }

    // MARK: - Grid Content
    private var gridContent: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 12) {
                ForEach(viewModel.items) { item in
                    OCRGridItemView(item: item)
                        .onTapGesture {
                            viewModel.navigateToDetail = item
                        }
                        .contextMenu {
                            Button(role: .destructive) {
                                Task { await viewModel.deleteItem(item) }
                            } label: {
                                Label("Delete", systemImage: "trash")
                            }
                        }
                }
            }
            .padding(.horizontal, 16)
            .padding(.top, 16)
            .padding(.bottom, 100)
        }
    }

    // MARK: - Empty State
    private var emptyStateView: some View {
        VStack(spacing: 20) {
            Spacer()

            Image(systemName: "doc.viewfinder")
                .font(.system(size: 60, weight: .ultraLight))
                .foregroundStyle(Color.tlTextSecondary.opacity(0.4))

            VStack(spacing: 8) {
                Text("Not Found")
                    .font(TLFont.heading(18))
                    .foregroundStyle(Color.tlTextSecondary)

                Text("Chosse an image to start")
                    .font(TLFont.body(14))
                    .foregroundStyle(Color.tlTextSecondary.opacity(0.6))
                    .multilineTextAlignment(.center)
            }

            Spacer()
        }
    }

    // MARK: - Loading Overlay
    private var loadingOverlay: some View {
        ZStack {
            Color.black.opacity(0.6).ignoresSafeArea()

            VStack(spacing: 20) {
                ProgressView()
                    .tint(Color.tlPrimaryLight)
                    .scaleEffect(1.5)

                Text("OCR ...")
                    .font(TLFont.body(15))
                    .foregroundStyle(Color.tlText)
            }
            .padding(32)
            .glassCard(cornerRadius: 20)
        }
    }

    // MARK: - FAB
    // MARK: - FAB
    private var fabButton: some View {
        VStack {
            Spacer()
            HStack {
                ZStack(alignment: .bottomTrailing) {
                    // FAB sub-menu
                    if showFABMenu {
                        VStack(spacing: 12) {
                            FABMenuItem(
                                icon: "folder.fill",
                                label: "File",
                                color: Color(hex: "#FFB347")
                            ) {
                                showFABMenu = false
                                // Add file picker logic here
                                viewModel.showFilePicker = true
                            }
                            
                            FABMenuItem(
                                icon: "photo.fill",
                                label: "Gallery",
                                color: Color.tlAccent
                            ) {
                                showFABMenu = false
                                viewModel.showImagePicker = true
                            }

                            FABMenuItem(
                                icon: "camera.fill",
                                label: "Camera",
                                color: Color.tlPrimaryLight
                            ) {
                                showFABMenu = false
                                showCamera = true
                            }
                        }
                        .padding(.bottom, 80)
                        .transition(.scale(scale: 0.8, anchor: .bottomTrailing).combined(with: .opacity))
                    }

                    // Main FAB
                    Button {
                        withAnimation(.spring(duration: 0.35, bounce: 0.3)) {
                            showFABMenu.toggle()
                        }
                    } label: {
                        ZStack {
                            Circle()
                                .fill(
                                    LinearGradient(
                                        colors: [Color.tlPrimary, Color.tlPrimaryDark],
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .frame(width: 60, height: 60)
                                .shadow(color: Color.tlPrimary.opacity(0.5), radius: 16, x: 0, y: 8)

                            Image(systemName: showFABMenu ? "xmark" : "plus")
                                .font(.system(size: 22, weight: .medium))
                                .foregroundStyle(Color.white)
                                .rotationEffect(.degrees(showFABMenu ? 45 : 0))
                                .animation(.spring(duration: 0.3), value: showFABMenu)
                        }
                    }
                }
                .padding(.leading, 24)
                .padding(.bottom, 40)
                
                Spacer()
            }
        }
    }
}

// MARK: - FAB Menu Item
struct FABMenuItem: View {
    let icon: String
    let label: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 10) {
                Text(label)
                    .font(TLFont.body(14))
                    .foregroundStyle(Color.tlText)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(Color.tlSurface2, in: Capsule())

                Circle()
                    .fill(color.opacity(0.2))
                    .frame(width: 44, height: 44)
                    .overlay(
                        Image(systemName: icon)
                            .font(.system(size: 18))
                            .foregroundStyle(color)
                    )
                    .overlay(
                        Circle()
                            .stroke(color.opacity(0.4), lineWidth: 1)
                    )
            }
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Grid Item View
struct OCRGridItemView: View {
    let item: OCRItem

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Image thumbnail
            ZStack {
                if let imageData = item.imageData, let uiImage = UIImage(data: imageData) {
                    Image(uiImage: uiImage)
                        .resizable()
                        .scaledToFit()
                        .frame(height: 130)
                        .clipped()
                } else {
                    Rectangle()
                        .fill(Color.tlSurface2)
                        .frame(height: 130)
                        .overlay(
                            Image(systemName: "photo")
                                .font(.system(size: 28))
                                .foregroundStyle(Color.tlTextSecondary.opacity(0.4))
                        )
                }

                // OCR type badge
                VStack {
                    HStack {
                        Spacer()
                        HStack(spacing: 4) {
                            Image(systemName: item.ocrType == .vision ? "eye.fill" : "server.rack")
                                .font(.system(size: 9))
                            Text(item.ocrType == .vision ? "Vision" : "OCR")
                                .font(TLFont.body(10))
                        }
                        .padding(.horizontal, 7)
                        .padding(.vertical, 4)
                        .background(Color.tlPrimary.opacity(0.85), in: Capsule())
                        .foregroundStyle(Color.white)
                        .padding(8)
                    }
                    Spacer()
                }
            }
            .frame(height: 130)
            .clipShape(UnevenRoundedRectangle(topLeadingRadius: 12, topTrailingRadius: 12))

            // Text preview
            VStack(alignment: .leading, spacing: 6) {
                Text(item.extractedText)
                    .font(TLFont.mono(12))
                    .foregroundStyle(Color.tlTextSecondary)
                    .lineLimit(3)
                    .multilineTextAlignment(.leading)

                Text(item.createdAt.formatted(date: .abbreviated, time: .shortened))
                    .font(TLFont.body(10))
                    .foregroundStyle(Color.tlTextSecondary.opacity(0.5))
            }
            .padding(10)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color.tlSurface2)
            .clipShape(UnevenRoundedRectangle(bottomLeadingRadius: 12, bottomTrailingRadius: 12))
        }
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.tlPrimary.opacity(0.15), lineWidth: 1)
        )
    }
}
