//
//  OCRUseCases.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation
import SwiftUI

// MARK: - Extract Text UseCase
struct ExtractTextUseCase: Sendable {
    private let ocrService: any OCRServiceProtocol

    init(ocrService: any OCRServiceProtocol) {
        self.ocrService = ocrService
    }

    func execute(image: UIImage, type: OCRItem.OCRType) async throws -> String {
        switch type {
        case .vision:
            return try await ocrService.extractTextVision(from: image)
        case .server:
            return try await ocrService.extractTextServer(from: image)
        }
    }
}

// MARK: - Save OCR Item UseCase
struct SaveOCRItemUseCase: Sendable {
    private let repository: any OCRRepositoryProtocol

    init(repository: any OCRRepositoryProtocol) {
        self.repository = repository
    }

    func execute(text: String, image: UIImage, type: OCRItem.OCRType) async throws -> OCRItem {
        let imageData = image.jpegData(compressionQuality: 0.8)
        let item = OCRItem(
            id: UUID(),
            createdAt: Date(),
            extractedText: text,
            ocrType: type,
            imageData: imageData
        )
        try await repository.save(item: item)
        return item
    }
}

// MARK: - Fetch All Items UseCase
struct FetchAllItemsUseCase: Sendable {
    private let repository: any OCRRepositoryProtocol

    init(repository: any OCRRepositoryProtocol) {
        self.repository = repository
    }

    func execute() async throws -> [OCRItem] {
        try await repository.fetchAll()
    }
}

// MARK: - Delete Item UseCase
struct DeleteItemUseCase: Sendable {
    private let repository: any OCRRepositoryProtocol

    init(repository: any OCRRepositoryProtocol) {
        self.repository = repository
    }

    func execute(id: UUID) async throws {
        try await repository.delete(id: id)
    }
}
