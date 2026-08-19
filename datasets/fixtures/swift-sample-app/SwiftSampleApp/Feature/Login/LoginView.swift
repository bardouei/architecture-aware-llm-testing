//
//  LoginView.swift
//  SwiftSampleApp
//
//  Created by sadeq on 8/18/26.
//

import SwiftUI


struct LoginView: View {
    
    @StateObject
    private var viewModel: LoginViewModel
    
    init(viewModel: LoginViewModel) {
        _viewModel = StateObject( wrappedValue: viewModel)
    }
    
    var body: some View {
        
        VStack {
            TextField("Username", text: $viewModel.username)
            
            SecureField("Password", text: $viewModel.password)
            
            Button("Login") {
                Task {
                    await viewModel.login()
                    
                }
            }
        }
        .padding()
    }
}
