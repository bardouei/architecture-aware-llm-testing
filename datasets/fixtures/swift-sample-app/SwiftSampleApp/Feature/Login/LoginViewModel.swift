//
//  LoginViewModel.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import Foundation
import Combine

@MainActor
final class LoginViewModel: ObservableObject {
    
    @Published var username = ""
    @Published var password = ""
    @Published var user: User?
    
    private let loginUseCase: LoginUseCase
    
    init(loginUseCase: LoginUseCase) {
        self.loginUseCase = loginUseCase
    }
    
    func login() async {
        do {
            user = try await loginUseCase.execute(username: username, password: password)
        } catch {
            user = nil
        }
    }
}
