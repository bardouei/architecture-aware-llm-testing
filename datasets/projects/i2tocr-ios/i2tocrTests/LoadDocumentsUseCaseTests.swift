//
//  LoadDocumentsUseCaseTests.swift
//  i2tocr
//
//  Created by baner on 1/4/26.
//

import XCTest
import RxSwift
@testable import i2tocr
import RxBlocking

final class LoadDocumentsUseCaseTests: XCTestCase {

    func test_execute_returnsDocuments() throws {
        // Arrange (Given)
        let repo = MockDocumentRepository()
        repo.documents = [
            DocumentObject(id: "1", title: "Doc1", textDic: "Hello"),
            DocumentObject(id: "2", title: "Doc2", textDic: "World")
        ]

        let useCase = LoadDocumentsUseCase(repository: repo)

        // Act (When)
        let result = try useCase.execute().toBlocking().first()

        // Assert (Then)
        XCTAssertEqual(result?.count, 2)
        XCTAssertEqual(result?.first?.title, "Doc1")
    }
}
