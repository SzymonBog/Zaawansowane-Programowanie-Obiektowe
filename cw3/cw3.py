class FileFacade:
    def write_file(self, filename, content):
        print(f"Opening file {filename}")
        print(f"Writing {content} to {filename}")

        print(f"File {filename} written")

    def read_file(self, filename):
        print(f"Opening file {filename}")
        print(f"Reading content from {filename}")
        print(f"Some content")

        print(f"File {filename} read")

    def delete_file(self, filename):
        print(f"Searching for {filename}")
        print(f"Deleting file {filename}")


f = FileFacade()
f.write_file("test.txt", "Hello World")
f.read_file("test.txt")
f.delete_file("test.txt")


# --------------------------------------------------------------


class ComplexImageLib:
    def load_buffer(self, img): print(f"Loading {img} to memory...")

    def apply_scale(self, factor): print(f"Scaling image by {factor * 100}%")

    def set_color_space(self, mode): print(f"Setting color space to {mode}")

    def run_compression(self, level): print(f"Compression: level {level}")

    def save_output(self): print("Saving image.")


class ImageProcessorFacade:
    def __init__(self):
        self.lib = ComplexImageLib()

    def quick_process(self, filename, size_factor=0.5, grayscale=True):
        self.lib.load_buffer(filename)
        self.lib.apply_scale(size_factor)
        if grayscale:
            self.lib.set_color_space("GRAY")
        self.lib.run_compression(9)
        self.lib.save_output()
        print("Process complete.")


editor = ImageProcessorFacade()
editor.quick_process("holidays.jpg")


# --------------------------------------------------------------


class MessageQueueFacade:
    def __init__(self, provider_type):
        self.provider_type = provider_type
        self._connect()

    def _connect(self):
        print(f"Connecting to {self.provider_type}...")
        print(f"Opening communication channel...")

    def send_message(self, queue_name, message):
        print(f"[{self.provider_type}] Sending: '{message}' to queue: {queue_name}")

    def receive_message(self, queue_name):
        print(f"[{self.provider_type}] Recieving message form {queue_name}...")
        return "Message"

    def close(self):
        print(f"Closing connection with {self.provider_type}.")


queue = MessageQueueFacade("RabbitMQ")
queue.send_message("orders", "New order nr 66")
msg = queue.receive_message("orders")
queue.close()