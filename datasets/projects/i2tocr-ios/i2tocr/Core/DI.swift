//
//  DI.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation
import SwiftData

@MainActor
final class DIContainer: ObservableObject {
    static let shared = DIContainer()

    let modelContainer: ModelContainer
    private let ocrService: any OCRServiceProtocol

    // Use Cases
    let extractTextUseCase: ExtractTextUseCase
    let saveOCRItemUseCase: SaveOCRItemUseCase
    let fetchAllItemsUseCase: FetchAllItemsUseCase
    let deleteItemUseCase: DeleteItemUseCase

    private init() {
        // SwiftData container
        let schema = Schema([OCRItemModel.self])
        let config = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)
        do {
            modelContainer = try ModelContainer(for: schema, configurations: [config])
        } catch {
            fatalError("SwiftData ModelContainer ایجاد نشد: \(error)")
        }

        // Services
        ocrService = OCRService()

        // Repository
        let repository = OCRRepository(modelContainer: modelContainer)

        // Use Cases
        extractTextUseCase = ExtractTextUseCase(ocrService: ocrService)
        saveOCRItemUseCase = SaveOCRItemUseCase(repository: repository)
        fetchAllItemsUseCase = FetchAllItemsUseCase(repository: repository)
        deleteItemUseCase = DeleteItemUseCase(repository: repository)
    }
}
