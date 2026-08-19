//
//  CreateDocumentFromOCRUseCaseTests.swift
//  i2tocr
//
//  Created by baner on 1/4/26.
//

import XCTest
import RxSwift
import RxBlocking
@testable import i2tocr

final class CreateDocumentFromOCRUseCaseTests: XCTestCase {

    func test_execute_createsDocumentWithDefaultTitle() throws {
        // Given
        let repo = MockDocumentRepository()
        let saveUseCase = SaveDocumentUseCase(repository: repo)
        let useCase = CreateDocumentFromOCRUseCase(saveUseCase: saveUseCase)

        // When
        let success = try useCase.execute(
            image: UIImage(),
            recognizedText: "Hello World",
            existingCount: 0,
            customTitle: nil
        )
        .toBlocking()
        .first()

        // Then
        XCTAssertTrue(success ?? false)
        XCTAssertEqual(repo.documents.count, 1)
        XCTAssertEqual(repo.documents.first?.title, "Document 1")
    }
}
