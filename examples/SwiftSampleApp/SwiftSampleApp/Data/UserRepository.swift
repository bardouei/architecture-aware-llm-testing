//
//  UserRepository.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import Foundation

public protocol UserRepository {
    func login(username: String, password: String) async throws -> User
}
