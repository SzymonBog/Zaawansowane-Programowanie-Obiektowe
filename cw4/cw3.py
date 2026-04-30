from abc import ABC, abstractmethod


class DocumentProcessing(ABC):
    form: str

    def __init__(self, form: str) -> None:
        self.form = form

    @abstractmethod
    def open_document(self) -> None:
        pass

    @abstractmethod
    def get_data(self) -> None:
        pass

    @abstractmethod
    def close_document(self) -> None:
        pass

    def process_document(self) -> None:
        self.open_document()
        self.get_data()
        self.close_document()


class PDFProcessing(DocumentProcessing):
    def open_document(self) -> None:
        print("Opening PDF")

    def get_data(self) -> None:
        print("Copping data from PDF file")

    def close_document(self) -> None:
        print("Closing PDF")


class DOCXProcessing(DocumentProcessing):
    def open_document(self) -> None:
        print("Opening DOCX")

    def get_data(self) -> None:
        print("Copping data from DOCX file")

    def close_document(self) -> None:
        print("Closing DOCX")


class TXTProcessing(DocumentProcessing):
    def open_document(self) -> None:
        print("Opening TXT")

    def get_data(self) -> None:
        print("Copping data from TXT file")

    def close_document(self) -> None:
        print("Closing TXT")


txt = TXTProcessing("txt")
txt.process_document()
print()
docx = DOCXProcessing("docx")
docx.process_document()
print()
pdf = PDFProcessing("pdf")
pdf.process_document()
print()

# --------------------------------------------------------


class OrderManagementSystem(ABC):
    delivery: str

    def __init__(self, delivery: str) -> None:
        self.delivery = delivery

    @abstractmethod
    def receive_order(self) -> None:
        pass

    @abstractmethod
    def prepare_order(self) -> None:
        pass

    @abstractmethod
    def attach_sticker(self) -> None:
        pass

    @abstractmethod
    def send_order(self) -> None:
        pass

    def manage_order(self) -> None:
        self.receive_order()
        self.prepare_order()
        self.attach_sticker()
        self.send_order()


class StandardDelivery(OrderManagementSystem):
    def receive_order(self) -> None:
        print("11:46 - Received order")

    def prepare_order(self) -> None:
        print("12:29 - Preparing order\n14:57 - Order prepared")

    def attach_sticker(self) -> None:
        print("16:01 - Attaching sticker")

    def send_order(self) -> None:
        print("17:01 - Sending order")


class ExpressDelivery(OrderManagementSystem):
    def receive_order(self) -> None:
        print("11:46 - Received order")

    def prepare_order(self) -> None:
        print("11:52 - Preparing order\n12:00 - Order prepared")

    def attach_sticker(self) -> None:
        print("12:03 - Attaching sticker")

    def send_order(self) -> None:
        print("12:05 - Sending order")


class SelfPickUp(OrderManagementSystem):
    def receive_order(self) -> None:
        print("11:46 - Received order")

    def prepare_order(self) -> None:
        print("12:25 - Preparing order\n14:00 - Order prepared")

    def attach_sticker(self) -> None:
        print("14:20 - Attaching sticker")

    def send_order(self) -> None:
        print("14:30 - Package ready to pick up")


sd = StandardDelivery("standard")
sd.manage_order()
print()
ed = ExpressDelivery("express")
ed.manage_order()
print()
sp = SelfPickUp("self_pick_up")
sp.manage_order()


# -----------------------------------------------------------


class DataExporter(ABC):
    def __init__(self, form: str) -> None:
        self.form = form

    @abstractmethod
    def open_document(self) -> None:
        pass

    @abstractmethod
    def select_data(self) -> None:
        pass

    @abstractmethod
    def select_format(self) -> None:
        pass

    @abstractmethod
    def export_data(self) -> None:
        pass

    @abstractmethod
    def close_document(self) -> None:
        pass

    def process(self) -> None:
        self.select_data()
        self.select_format()
        self.export_data()
        self.close_document()


class CSVExporter(DataExporter):
    def open_document(self) -> None:
        print("Opening File")

    def select_data(self) -> None:
        print("Selecting Data")

    def select_format(self) -> None:
        print("Selecting Format: CSV")

    def export_data(self) -> None:
        print("Exporting Data to CSV")

    def close_document(self) -> None:
        print("Closing File")


class JSONExporter(DataExporter):
    def open_document(self) -> None:
        print("Opening File")

    def select_data(self) -> None:
        print("Selecting Data")

    def select_format(self) -> None:
        print("Selecting Format: JSON")

    def export_data(self) -> None:
        print("Exporting Data to JSON")

    def close_document(self) -> None:
        print("Closing File")


class XMLExporter(DataExporter):
    def open_document(self) -> None:
        print("Opening File")

    def select_data(self) -> None:
        print("Selecting Data")

    def select_format(self) -> None:
        print("Selecting Format: XML")

    def export_data(self) -> None:
        print("Exporting Data to XML")

    def close_document(self) -> None:
        print("Closing File")


csv = CSVExporter("csv")
jx = JSONExporter("json")
xml = XMLExporter("xml")

csv.process()
print()
jx.process()
print()
xml.process()
