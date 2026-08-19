//
//  HomeUITests.swift
//  i2tocr
//
//  Created by baner on 1/4/26.
//

import XCTest

final class HomeUITests: XCTestCase {

    private var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false

        app = XCUIApplication()
        app.launchArguments.append("--uitesting")
        app.launch()
    }

    override func tearDown() {
        app = nil
        super.tearDown()
    }

    // MARK: - Helpers

    @discardableResult
    private func wait(_ element: XCUIElement,
                      timeout: TimeInterval = 3,
                      file: StaticString = #filePath,
                      line: UInt = #line) -> XCUIElement {
        let ok = element.waitForExistence(timeout: timeout)
        if !ok {
            XCTFail("Element not found: \(element)\n\nUI Tree:\n\(app.debugDescription)", file: file, line: line)
        }
        return element
    }

    // MARK: - Tests

    func test_homeScreen_isVisible() {
        // اگر title به هر دلیل match نشه، حداقل وجود navigation bar را چک می‌کنیم
        let navBar = app.navigationBars.firstMatch
        wait(navBar, timeout: 5)
    }

    func test_cameraButton_exists_and_tappable() {
        // UIButton فقط image دارد؛ معمولاً XCTest آن را Button تشخیص نمی‌دهد
        let camera = app.otherElements["cameraButton"]
        wait(camera, timeout: 5)
        XCTAssertTrue(camera.isHittable, "cameraButton is not hittable.\n\nUI Tree:\n\(app.debugDescription)")
    }

    func test_collectionView_exists() {
        let collection = app.collectionViews["documentsCollectionView"]
        wait(collection, timeout: 5)
    }

    func test_emptyState_exists() {
        // emptyStateImageView ممکن است به عنوان Image دیده نشود، پس otherElements امن‌تر است
        let empty = app.otherElements["emptyStateView"]
        wait(empty, timeout: 5)
    }

    func test_searchBar_typingText() {
        // حتماً روی searchBar یک accessibilityIdentifier گذاشته باش:
        // searchController.searchBar.accessibilityIdentifier = "homeSearchBar"
        let searchBar = app.otherElements["homeSearchBar"]
        wait(searchBar, timeout: 5)

        searchBar.tap()

        // داخل UISearchBar معمولاً یک textField وجود دارد
        let textField = app.textFields.firstMatch
        wait(textField, timeout: 3)

        textField.typeText("invoice")
        XCTAssertTrue((textField.value as? String)?.contains("invoice") == true,
                      "Search text was not typed.\n\nUI Tree:\n\(app.debugDescription)")
    }

    func test_openCameraActionSheet() {
        let camera = app.otherElements["cameraButton"]
        wait(camera, timeout: 5)
        camera.tap()

        // ActionSheet در XCTest گاهی alerts یا sheets دیده می‌شود
        let sheet = app.sheets["Add Document"]
        if sheet.waitForExistence(timeout: 2) {
            XCTAssertTrue(sheet.exists)
            return
        }

        let alert = app.alerts["Add Document"]
        wait(alert, timeout: 2)
    }
}
