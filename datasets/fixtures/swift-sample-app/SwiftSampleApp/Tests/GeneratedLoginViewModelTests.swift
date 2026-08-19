import XCTest
@testable import SwiftSampleApp

@MainActor
final class GeneratedLoginViewModelTests: XCTestCase {

    func testLoginSuccess() async {

        let mockUseCase = GeneratedMockLoginUseCase()

        let viewModel = LoginViewModel(
            loginUseCase: mockUseCase
        )

        await viewModel.login()

        XCTAssertNotNil(viewModel.user)
    }
}


final class GeneratedMockLoginUseCase: LoginUseCase {

    func execute(
        username: String,
        password: String
    ) async throws -> User {

        return User(
            id: "1",
            name: username
        )
    }
}
