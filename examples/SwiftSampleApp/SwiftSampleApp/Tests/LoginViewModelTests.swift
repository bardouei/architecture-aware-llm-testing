//
//  LoginViewModelTests.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import XCTest
@testable import SwiftSampleApp


@MainActor
final class LoginViewModelTests: XCTestCase {


    func testLoginSuccess() async throws {

        let repository = MockUserRepository()

        let useCase = DefaultLoginUseCase(repository: repository)

        let vm = LoginViewModel(loginUseCase: useCase)
        
        await vm.login()

        XCTAssertNotNil(vm.user)
    }
}


final class MockUserRepository: UserRepository {

    func login(
        username: String,
        password: String
    ) async throws -> User {

        User(
            id: "1",
            name: "Test"
        )
    }
}
