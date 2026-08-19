//
//  LoginUseCase.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import Foundation

public protocol LoginUseCase {
    func execute(
        username: String,
        password: String
    ) async throws -> User
}

public struct User: Codable {
    public let id: String
    public let name: String
}
