//
//  HomeViewModel.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftUI
import PhotosUI
import PDFKit

enum OCRMode: String, CaseIterable {
    case vision = "vision"
    case server = "server"

    var label: String {
        switch self {
        case .vision: return "Vision AI"
        case .server: return "OCR"
        }
    }

    var icon: String {
        switch self {
        case .vision: return "eye.fill"
        case .server: return "server.rack"
        }
    }
}

enum ImageSourceType {
    case camera, photoLibrary, file
}

@MainActor
final class HomeViewModel: ObservableObject {
    // MARK: - Published State
    @Published var items: [OCRItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var ocrMode: OCRMode = .vision
    @Published var showSideMenu = false
    @Published var showSourcePicker = false
    @Published var showImagePicker = false
    @Published var imageSourceType: ImageSourceType = .photoLibrary
    @Published var selectedPhotoItem: PhotosPickerItem?
    @Published var navigateToDetail: OCRItem?
    
    @Published var showFilePicker = false
    @Published var selectedFileURL: URL?

    // MARK: - Dependencies
    private let extractTextUseCase: ExtractTextUseCase
    private let saveOCRItemUseCase: SaveOCRItemUseCase
    private let fetchAllItemsUseCase: FetchAllItemsUseCase
    private let deleteItemUseCase: DeleteItemUseCase

    init(container: DIContainer) {
        self.extractTextUseCase  = container.extractTextUseCase
        self.saveOCRItemUseCase  = container.saveOCRItemUseCase
        self.fetchAllItemsUseCase = container.fetchAllItemsUseCase
        self.deleteItemUseCase   = container.deleteItemUseCase
    }

    // MARK: - Load Items
    func loadItems() async {
        do {
            items = try await fetchAllItemsUseCase.execute()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
    
    func processSelectedFile(_ url: URL?) async {
        guard let url else { return }
        isLoading = true
        errorMessage = nil
        imageSourceType = .file
        
        do {
            // Check if file is an image
            let imageData = try Data(contentsOf: url)
            guard let image = UIImage(data: imageData) else {
                throw OCRError.imageConversionFailed
            }
            
            await processImage(image)
        } catch {
            isLoading = false
            errorMessage = error.localizedDescription
        }
    }

    // MARK: - Process Selected Photo
    func processSelectedPhoto(_ item: PhotosPickerItem?) async {
        guard let item else { return }
        isLoading = true
        errorMessage = nil
        imageSourceType = .photoLibrary

        do {
            guard let data = try await item.loadTransferable(type: Data.self),
                  let image = UIImage(data: data) else {
                throw OCRError.imageConversionFailed
            }
            await processImage(image)
        } catch {
            isLoading = false
            errorMessage = error.localizedDescription
        }
    }

    // MARK: - Process Camera Image
    func processCameraImage(_ image: UIImage) async {
        isLoading = true
        errorMessage = nil
        imageSourceType = .camera 
        await processImage(image)
    }

    private func processImage(_ image: UIImage) async {
        do {
            let type = OCRItem.OCRType(rawValue: ocrMode.rawValue) ?? .vision
            let text = try await extractTextUseCase.execute(image: image, type: type)
            let newItem = try await saveOCRItemUseCase.execute(text: text, image: image, type: type)
            items.insert(newItem, at: 0)
            isLoading = false
            navigateToDetail = newItem
        } catch {
            isLoading = false
            errorMessage = error.localizedDescription
        }
    }

    // MARK: - Delete
    func deleteItem(_ item: OCRItem) async {
        do {
            try await deleteItemUseCase.execute(id: item.id)
            items.removeAll { $0.id == item.id }
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
