//
//  DefaultUserRepository.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import Foundation

final class DefaultUserRepository: UserRepository {
    func login(username: String, password: String) async throws -> User {
        return User(
            id: "1",
            name: "Sadegh"
        )
    }
}
