//
//  SceneDelegate.swift
//  i2tocr-iOS
//
//  Created by bardouei on 7/12/24.
//

import UIKit
import SwiftUI
import SwiftData

class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        guard let windowScene = scene as? UIWindowScene else { return }

        let container = DIContainer.shared
        let router = AppState.shared.router
        
        print("🔵 SceneDelegate - Current route: \(router.currentRoute)")

        let rootView = RootView()
            .environmentObject(container)
            .environmentObject(router)
            .modelContainer(container.modelContainer)

        let window = UIWindow(windowScene: windowScene)
        window.rootViewController = UIHostingController(rootView: rootView)
        self.window = window
        window.makeKeyAndVisible()
    }

    func sceneDidDisconnect(_ scene: UIScene) {}
    func sceneDidBecomeActive(_ scene: UIScene) {}
    func sceneWillResignActive(_ scene: UIScene) {}
    func sceneWillEnterForeground(_ scene: UIScene) {}
    func sceneDidEnterBackground(_ scene: UIScene) {}
}
