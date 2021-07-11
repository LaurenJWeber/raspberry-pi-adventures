import RPi.GPIO as GPIO
import time
import jsons
from queue import SimpleQueue, Empty
from threading import Thread
from argparse import ArgumentParser

CONFIG_ERROR = 1
DOT = '.'
DASH = '-'
finish_signal = object()


class MorseConfig:
    
    def __init__(self):
        self.min_wait_seconds = 0.01
        self.gpo_dot = 1
        self.gpo_dash = 1
        self.dot_duration_seconds = 0.2
        self.dash_duration_seconds = 0.6
        self.inter_symbol_wait_seconds = 0.2
        self.inter_char_wait_seconds = 0.6
        self.inter_word_wait_seconds = 1.4
        self.string_to_send = ""
        self.alphabet = {}


class MorseCodeTransmitter:
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = MorseConfig()
    
    def read_config(self):
        with open(self.config_file, "r") as conf:
            json_config = conf.read().strip()
        self.config = jsons.loads(json_config, cls=MorseConfig)
        self.config.dot_duration_seconds = max(self.config.min_wait_seconds, self.config.dot_duration_seconds)
        self.config.dash_duration_seconds = max(self.config.min_wait_seconds, self.config.dash_duration_seconds)
        self.config.inter_symbol_wait_seconds = max(self.config.min_wait_seconds, self.config.inter_symbol_wait_seconds)
        self.config.inter_char_wait_seconds = max(self.config.min_wait_seconds, self.config.inter_char_wait_seconds)
        self.config.inter_word_wait_seconds = max(self.config.min_wait_seconds, self.config.inter_word_wait_seconds)
        self.config.string_to_send = self.config.string_to_send.upper()

    def configure_transmitter(self):
        try:
            self.read_config()
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.config.gpo_dot, GPIO.OUT)
            GPIO.setup(self.config.gpo_dash, GPIO.OUT)
            self.clear_display()
        except Exception as ex:
            print(f"Error applying configuration: {ex}")
            return False
        return True

    def clear_display(self):
        GPIO.output(self.config.gpo_dot, False)
        GPIO.output(self.config.gpo_dash, False)

    def transmit_character(self, character):
        if character in self.config.alphabet.keys():
            print(f"{character}: ", end="")
            for symbol in self.config.alphabet[character]:
                if symbol == DOT:
                    print("DOT ", end="")
                    GPIO.output(self.config.gpo_dot, True)
                    time.sleep(self.config.dot_duration_seconds)
                    GPIO.output(self.config.gpo_dot, False)
                elif symbol == DASH:
                    print("DASH ", end="")
                    GPIO.output(self.config.gpo_dash, True)
                    time.sleep(self.config.dash_duration_seconds)
                    GPIO.output(self.config.gpo_dash,  False)
                time.sleep(self.config.inter_symbol_wait_seconds)
        time.sleep(self.config.inter_char_wait_seconds)
        print("")

    def transmit_string(self):
        for char in self.config.string_to_send:
            if char.isspace():
                print("")
                time.sleep(self.config.inter_word_wait_seconds)
            else:
                self.transmit_character(char)
        print("________________________________")


def transmitter(morse_transmitter, max_repetitions, message_queue):
    continual_operation = max_repetitions == 0
    i = 0
    while i < max_repetitions or continual_operation:
        morse_transmitter.transmit_string()
        try:
            my_message = message_queue.get_nowait()
            if my_message is finish_signal:
                break
        except Empty:
            pass
        i += 1       
    print("==>Transmitter thread exited.")
    

def main():
    parser = ArgumentParser()
    parser.add_argument("config_file", type=str, help="Path to config file")
    parser.add_argument("repetitions",
                        type=int,
                        help="Number of times to repeat message, 0 for continual repeat",
                        nargs='?',
                        default=1
                        )
    args = parser.parse_args()
    my_morse_transmitter = MorseCodeTransmitter(args.config_file)

    if not my_morse_transmitter.configure_transmitter():
        exit(CONFIG_ERROR)

    msg_queue = SimpleQueue()
    send_thread = Thread(target=transmitter, args=(my_morse_transmitter, args.repetitions, msg_queue))
    send_thread.start()
    
    if args.repetitions == 0:
        input("** Press enter to quit. **\n")
        print("==>Received user input.  Transmitter will stop after current iteration.")
        msg_queue.put(finish_signal)


if __name__ == "__main__":
    main()
