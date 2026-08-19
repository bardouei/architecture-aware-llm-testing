import XCTest
@testable import SwiftSampleApp

@MainActor
final class ArchitectureAwareLoginViewModelTests: XCTestCase {

    func testLogin_whenUseCaseSucceeds_setsReturnedUser() async {
        let expectedUser = User(id: "user-1", name: "Jane Appleseed")
        let mockUseCase = MockLoginUseCase(result: .success(expectedUser))
        let viewModel = LoginViewModel(loginUseCase: mockUseCase)
        viewModel.username = "jane@example.com"
        viewModel.password = "secure-password"

        await viewModel.login()

        XCTAssertEqual(viewModel.user?.id, expectedUser.id)
        XCTAssertEqual(viewModel.user?.name, expectedUser.name)
    }

    func testLogin_whenUseCaseFails_clearsUser() async {
        let mockUseCase = MockLoginUseCase(result: .failure(LoginUseCaseMockError.invalidCredentials))
        let viewModel = LoginViewModel(loginUseCase: mockUseCase)
        viewModel.username = "jane@example.com"
        viewModel.password = "wrong-password"
        viewModel.user = User(id: "stale-user", name: "Stale User")

        await viewModel.login()

        XCTAssertNil(viewModel.user)
    }

    func testLogin_passesCredentialsToUseCaseExactlyOnce() async {
        let mockUseCase = MockLoginUseCase(result: .success(User(id: "user-1", name: "Jane Appleseed")))
        let viewModel = LoginViewModel(loginUseCase: mockUseCase)
        viewModel.username = "jane@example.com"
        viewModel.password = "secure-password"

        await viewModel.login()

        XCTAssertEqual(mockUseCase.executeCallCount, 1)
        XCTAssertEqual(mockUseCase.receivedUsername, "jane@example.com")
        XCTAssertEqual(mockUseCase.receivedPassword, "secure-password")
    }
}

private enum LoginUseCaseMockError: Error {
    case invalidCredentials
}

private final class MockLoginUseCase: LoginUseCase {
    private let result: Result<User, Error>
    private(set) var executeCallCount = 0
    private(set) var receivedUsername: String?
    private(set) var receivedPassword: String?

    init(result: Result<User, Error>) {
        self.result = result
    }

    func execute(username: String, password: String) async throws -> User {
        executeCallCount += 1
        receivedUsername = username
        receivedPassword = password
        return try result.get()
    }
}
