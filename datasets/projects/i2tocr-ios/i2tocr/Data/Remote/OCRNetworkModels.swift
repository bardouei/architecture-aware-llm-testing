//
//  OCRNetworkModels.swift
//  i2tocr
//
//  Created by baner on 5/14/26.
//

import Foundation

struct OCRResult: Decodable, Sendable {
    let language: String
    let config: String
    let text: String
}

struct ServerResponse: Decodable, Sendable {
    let status: String
    let data: OCRResult
    let detail: String
    let task_id: String
}
