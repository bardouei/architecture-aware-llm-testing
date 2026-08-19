// Compile-only validation fixture for the shared TCA 1.26 XCTest API contract.
// This file is never included in an LLM prompt or a measured generated suite.

import ComposableArchitecture
@testable import FeatureSplash
import XCTest

@MainActor
final class TCAFrameworkContractSmokeTests: XCTestCase {
    func testVerifiedClockAndTestStoreAPI() async {
        let clock = TestClock()
        let store = TestStore(initialState: SplashFeature.State()) {
            SplashFeature()
        } withDependencies: {
            $0.continuousClock = clock
        }

        await store.send(.onAppear)
        await clock.advance(by: .seconds(2))
        await store.receive(.finished)
    }
}
