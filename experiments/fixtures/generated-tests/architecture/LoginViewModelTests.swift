
import XCTest

@MainActor
final class LoginViewModelTests: XCTestCase {


    func testLoginSuccess() async {

        let mockUseCase = MockLoginUseCase()

        let viewModel = LoginViewModel(
            loginUseCase: mockUseCase
        )


        await viewModel.login()


        XCTAssertNotNil(
            viewModel.user
        )

    }


}


final class MockLoginUseCase: LoginUseCase {


    func execute(
        username: String,
        password: String
    ) async throws -> User {

        return User()

    }

}
