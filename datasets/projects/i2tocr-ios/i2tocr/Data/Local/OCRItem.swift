//
//  Local.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation

struct OCRItem: Identifiable, Sendable {
    let id: UUID
    let createdAt: Date
    let extractedText: String
    let ocrType: OCRType
    let imageData: Data?

    enum OCRType: String, Sendable {
        case vision = "vision"
        case server = "server"
    }
}
