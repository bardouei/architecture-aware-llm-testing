//
//  OCRRepository.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation
import SwiftData
import SwiftUI

@ModelActor
actor OCRRepository: OCRRepositoryProtocol {

    // MARK: - Save
    func save(item: OCRItem) async throws {
        let model = OCRItemModel(
            id: item.id,
            createdAt: item.createdAt,
            extractedText: item.extractedText,
            ocrType: item.ocrType.rawValue,
            imageData: item.imageData
        )
        modelContext.insert(model)
        try modelContext.save()
    }

    // MARK: - Fetch All
    func fetchAll() async throws -> [OCRItem] {
        let descriptor = FetchDescriptor<OCRItemModel>(
            sortBy: [SortDescriptor(\.createdAt, order: .reverse)]
        )
        let models = try modelContext.fetch(descriptor)
        return models.map { model in
            OCRItem(
                id: model.id,
                createdAt: model.createdAt,
                extractedText: model.extractedText,
                ocrType: OCRItem.OCRType(rawValue: model.ocrType) ?? .vision,
                imageData: model.imageData
            )
        }
    }

    // MARK: - Delete
    func delete(id: UUID) async throws {
        let descriptor = FetchDescriptor<OCRItemModel>(
            predicate: #Predicate { $0.id == id }
        )
        let models = try modelContext.fetch(descriptor)
        for model in models {
            modelContext.delete(model)
        }
        try modelContext.save()
    }
}
