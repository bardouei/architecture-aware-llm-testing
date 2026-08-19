//
//  OCRService.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation
import SwiftUI
import Vision

enum OCRError: LocalizedError {
    case imageConversionFailed
    case noTextFound
    case networkError(String)
    case serverError(String)

    var errorDescription: String? {
        switch self {
        case .imageConversionFailed: return "Image conversion failed"
        case .noTextFound: return "No text found in the image"
        case .networkError(let msg): return "Network error: \(msg)"
        case .serverError(let msg): return "Server error: \(msg)"
        }
    }
}

final class OCRService: OCRServiceProtocol {

    // MARK: - Vision OCR (Apple built-in)
    func extractTextVision(from image: UIImage) async throws -> String {
        guard let cgImage = image.cgImage else {
            throw OCRError.imageConversionFailed
        }

        return try await withCheckedThrowingContinuation { continuation in
            let request = VNRecognizeTextRequest { request, error in
                if let error {
                    continuation.resume(throwing: OCRError.networkError(error.localizedDescription))
                    return
                }

                let observations = request.results as? [VNRecognizedTextObservation] ?? []
                let text = observations
                    .compactMap { $0.topCandidates(1).first?.string }
                    .joined(separator: "\n")

                if text.isEmpty {
                    continuation.resume(throwing: OCRError.noTextFound)
                } else {
                    continuation.resume(returning: text)
                }
            }

            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = true
            request.recognitionLanguages = ["fa", "en", "ar"]

            let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
            do {
                try handler.perform([request])
            } catch {
                continuation.resume(throwing: OCRError.networkError(error.localizedDescription))
            }
        }
    }

    // MARK: - Server OCR
    func extractTextServer(from image: UIImage) async throws -> String {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            throw OCRError.imageConversionFailed
        }

        let url = URL(string: "https://i2tocr.com/ocr")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        let lineBreak = "\r\n"

        // Image field
        body.append("--\(boundary)\(lineBreak)".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\(lineBreak)".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\(lineBreak)\(lineBreak)".data(using: .utf8)!)
        body.append(imageData)
        body.append(lineBreak.data(using: .utf8)!)

        // Language field
        body.append("--\(boundary)\(lineBreak)".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"language\"\(lineBreak)\(lineBreak)".data(using: .utf8)!)
        body.append("eng".data(using: .utf8)!)
        body.append(lineBreak.data(using: .utf8)!)

        body.append("--\(boundary)--\(lineBreak)".data(using: .utf8)!)
        request.httpBody = body

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw OCRError.serverError("Invalid HTTP status")
        }

        let serverResponse = try JSONDecoder().decode(ServerResponse.self, from: data)

        guard serverResponse.status == "success" else {
            throw OCRError.serverError("Server did not return a successful response")
        }

        let text = serverResponse.data.text
        if text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            throw OCRError.noTextFound
        }
        return text
    }
}
