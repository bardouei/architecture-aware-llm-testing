//
//  OCRRepositoryProtocol.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation
import SwiftUI

protocol OCRRepositoryProtocol: Sendable {
    func save(item: OCRItem) async throws
    func fetchAll() async throws -> [OCRItem]
    func delete(id: UUID) async throws
}

protocol OCRServiceProtocol: Sendable {
    func extractTextVision(from image: UIImage) async throws -> String
    func extractTextServer(from image: UIImage) async throws -> String
}
