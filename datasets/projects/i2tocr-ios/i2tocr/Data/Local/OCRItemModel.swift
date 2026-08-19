//
//  OCRItemModel.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import SwiftData
import Foundation

@Model
final class OCRItemModel {
    @Attribute(.unique) var id: UUID
    var createdAt: Date
    var extractedText: String
    var ocrType: String
    var imageData: Data?

    init(
        id: UUID = UUID(),
        createdAt: Date = Date(),
        extractedText: String,
        ocrType: String,
        imageData: Data? = nil
    ) {
        self.id = id
        self.createdAt = createdAt
        self.extractedText = extractedText
        self.ocrType = ocrType
        self.imageData = imageData
    }
}


