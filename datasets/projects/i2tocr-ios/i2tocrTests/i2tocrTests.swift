//
//  i2tocrTests.swift
//  i2tocrTests
//
//  Created by bardouei on 7/12/24.
//

import XCTest
import Foundation
@testable import i2tocr

final class i2tocrTests: XCTestCase {
    func testUppercaseConversion() throws {
        // 1️⃣ Arrange
        let input = "hello"
        let expectedOutput = "HELLO"

        // 2️⃣ Act
        let result = StringHelper.uppercase(input)

        // 3️⃣ Assert
        XCTAssertEqual(result, expectedOutput, "uppercase() should convert text to upper case")
    }
}

struct StringHelper {
    static func uppercase(_ value: String) -> String {
        return value.uppercased()
    }
}
