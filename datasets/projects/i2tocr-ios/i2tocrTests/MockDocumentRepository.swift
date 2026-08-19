//
//  MockDocumentRepository.swift
//  i2tocr
//
//  Created by baner on 1/4/26.
//

import RxSwift
@testable import i2tocr

final class MockDocumentRepository: DocumentRepository {

    var documents: [DocumentObject] = []
    var shouldFail = false

    func getAllDocuments() -> Observable<[DocumentObject]> {
        shouldFail
        ? Observable.error(NSError(domain: "test", code: 0))
        : Observable.just(documents)
    }

    func saveDocument(_ document: DocumentObject) -> Observable<Bool> {
        shouldFail
        ? Observable.just(false)
        : {
            documents.append(document)
            return Observable.just(true)
        }()
    }

    func deleteDocument(id: String) -> Observable<Bool> {
        shouldFail
        ? Observable.just(false)
        : {
            documents.removeAll { $0.id == id }
            return Observable.just(true)
        }()
    }

    func updateDocument(id: String, newText: String) -> Observable<Bool> {
        shouldFail
        ? Observable.just(false)
        : {
            documents.first { $0.id == id }?.textDic = newText
            return Observable.just(true)
        }()
    }

    func clearAllDocuments() -> Observable<Bool> {
        documents.removeAll()
        return Observable.just(true)
    }
}
