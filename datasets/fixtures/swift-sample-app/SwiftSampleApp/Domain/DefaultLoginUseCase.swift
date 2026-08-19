//
//  DefaultLoginUseCase.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import Foundation

final class DefaultLoginUseCase: LoginUseCase {

    private let repository: UserRepository

    init(repository: UserRepository) {
        self.repository = repository
    }

    func execute(username: String, password: String) async throws -> User {
        try await repository.login(
            username: username,
            password: password
        )
    }
}
