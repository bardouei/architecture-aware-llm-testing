from abc import ABC, abstractmethod



class LLMClient(ABC):


    @abstractmethod
    def generate(
        self,
        prompt
    ):
        pass





class MockLLMClient(LLMClient):


    def generate(
        self,
        prompt
    ):


        return """
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
"""