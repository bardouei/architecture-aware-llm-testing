
import XCTest
@testable import SwiftSampleApp

@MainActor
final class LoginViewModelTests: XCTestCase {

    func testLoginSuccess() async {

        let mockUseCase = GeneratedMockLoginUseCase()

        let viewModel = LoginViewModel(
            loginUseCase: mockUseCase
        )


        await viewModel.login()


        XCTAssertNotNil(
            viewModel.user
        )

    }
}
