from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def get_extension(self) -> str:
        pass


class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self) -> Document:
        pass


class WordDocument(Document):
    def get_extension(self) -> str:
        return "docx"


class PDFDocument(Document):
    def get_extension(self) -> str:
        return "pdf"


class WordFactory(DocumentFactory):
    def create_document(self) -> Document:
        return WordDocument()


class PDFFactory(DocumentFactory):
    def create_document(self) -> Document:
        return PDFDocument()


class Factory1:
    _factories: dict

    def __init__(self) -> None:
        self._factories = {
            "docx": WordFactory,
            "pdf": PDFFactory,
        }

    def create_document(self, extension_: str) -> Document:
        return self._factories[extension_]().create_document()


factory = Factory1()
docx = factory.create_document("docx")
pdf = factory.create_document("pdf")
print(docx.get_extension())
print(pdf.get_extension())


class Animal(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass


class AnimalFactory(ABC):
    @abstractmethod
    def create_animal(self) -> Animal:
        pass


class Dog(Animal):
    def get_type(self) -> str:
        return "Dog"


class Cat(Animal):
    def get_type(self) -> str:
        return "Cat"


class DogFactory(AnimalFactory):
    def create_animal(self) -> Animal:
        return Dog()


class CatFactory(AnimalFactory):
    def create_animal(self) -> Animal:
        return Cat()


class Factory2:
    _factories: dict

    def __init__(self) -> None:
        self._factories = {
            "dog": DogFactory,
            "cat": CatFactory,
        }

    def create_animal(self, type_: str) -> Animal:
        return self._factories[type_]().create_animal()


factory = Factory2()
dog = factory.create_animal("dog")
cat = factory.create_animal("cat")
print(dog.get_type())
print(cat.get_type())


# --------------------------------------------------------


class DocumentDyn(ABC):
    @abstractmethod
    def get_extension(self) -> str:
        pass


class DocumentFactoryDyn(ABC):
    @abstractmethod
    def create_document(self) -> DocumentDyn:
        pass


class WordDocumentDyn(DocumentDyn):
    def get_extension(self) -> str:
        return "docx"


class PDFDocumentDyn(DocumentDyn):
    def get_extension(self) -> str:
        return "pdf"


class ExcelDocumentDyn(DocumentDyn):
    def get_extension(self) -> str:
        return "xlsx"


class WordFactoryDyn(DocumentFactoryDyn):
    def create_document(self) -> DocumentDyn:
        return WordDocumentDyn()


class PDFFactoryDyn(DocumentFactoryDyn):
    def create_document(self) -> DocumentDyn:
        return PDFDocumentDyn()


class ExcelFactoryDyn(DocumentFactoryDyn):
    def create_document(self) -> DocumentDyn:
        return ExcelDocumentDyn()


class FactoryDyn1:
    _factories: dict

    def __init__(self) -> None:
        self._factories = {
            "docx": WordFactoryDyn,
            "pdf": PDFFactoryDyn,
        }

    def register_format(self, new_extension: str, new_factory: DocumentFactoryDyn):
        self._factories[new_extension] = new_factory

    def create_document(self, extension_: str) -> DocumentDyn:
        doc_class = self._factories.get(extension_)
        if not doc_class:
            raise ValueError("Unregistered extension")
        return self._factories[extension_]().create_document()


factory = FactoryDyn1()
docx = factory.create_document("docx")
pdf = factory.create_document("pdf")
# xlsx1 = factory.create_document("xlsx")
factory.register_format("xlsx", ExcelFactoryDyn)
xlsx2 = factory.create_document("xlsx")
print(docx.get_extension())
print(pdf.get_extension())
print(xlsx2.get_extension())


class AnimalDyn(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass


class AnimalFactoryDyn(ABC):
    @abstractmethod
    def create_animal(self) -> AnimalDyn:
        pass


class DogDyn(AnimalDyn):
    def get_type(self) -> str:
        return "Dog"


class CatDyn(AnimalDyn):
    def get_type(self) -> str:
        return "Cat"


class BirdDyn(AnimalDyn):
    def get_type(self) -> str:
        return "Bird"


class DogFactoryDyn(AnimalFactoryDyn):
    def create_animal(self) -> AnimalDyn:
        return DogDyn()


class CatFactoryDyn(AnimalFactoryDyn):
    def create_animal(self) -> AnimalDyn:
        return CatDyn()


class BirdFactoryDyn(AnimalFactoryDyn):
    def create_animal(self) -> AnimalDyn:
        return BirdDyn()


class FactoryDyn2:
    _factories: dict

    def __init__(self) -> None:
        self._factories = {
            "dog": DogFactoryDyn,
            "cat": CatFactoryDyn,
        }

    def register_format(self, animal_type: str, new_factory: AnimalFactoryDyn):
        self._factories[animal_type] = new_factory

    def create_animal(self, animal_type_: str) -> AnimalDyn:
        doc_class = self._factories.get(animal_type_)
        if not doc_class:
            raise ValueError("Unregistered animal type")
        return self._factories[animal_type_]().create_animal()


factory = FactoryDyn2()
dog = factory.create_animal("dog")
cat = factory.create_animal("cat")
factory.register_format("bird", BirdFactoryDyn)
burd = factory.create_animal("bird")
print(dog.get_type())
print(cat.get_type())
print(burd.get_type())
