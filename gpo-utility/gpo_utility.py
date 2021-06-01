import RPi.GPIO as GPIO
import time
import jsons
from argparse import ArgumentParser

CONFIG_ERROR = 1


class GpoTesterConfig:
    
    def __init__(self):
        self.gpo_list = []
        self.blink_period_seconds = 1.0
        self.blink_duty_cycle = 0.5


class GpoTester:
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = GpoTesterConfig()
    
    def read_config(self):
        with open(self.config_file, "r") as conf:
            json_config = conf.read().strip()
        self.config = jsons.loads(json_config, cls=GpoTesterConfig)
        self.config.blink_duty_cycle = max(0.0, self.config.blink_duty_cycle)
        self.config.blink_duty_cycle = min(1.0, self.config.blink_duty_cycle)
        self.config.blink_period_seconds = max(0.0, self.config.blink_period_seconds)
    
    def configure_gpos(self):
        try:
            self.read_config()
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            for pin in self.config.gpo_list:
                GPIO.setup(pin, GPIO.OUT)
        except Exception as ex:
            print(f"Error configuring GPOs: {ex}")
            return False

        return True

    def clear_gpos(self):
        for pin in self.config.gpo_list:
            GPIO.output(pin, False)
            
    def set_gpos(self):
        for pin in self.config.gpo_list:
            GPIO.output(pin, True)
        
    def blink_gpos_in_sequence(self):
        on_time_seconds = self.config.blink_period_seconds * self.config.blink_duty_cycle
        off_time_seconds = self.config.blink_period_seconds - on_time_seconds   
        for pin in self.config.gpo_list:
            GPIO.output(pin, True)
            time.sleep(on_time_seconds)
            GPIO.output(pin, False)
            time.sleep(off_time_seconds)
    
    def show_all_gpos(self):
        self.set_gpos()
        time.sleep(self.config.blink_period_seconds)
        self.clear_gpos()


def main():
    
    parser = ArgumentParser()
    parser.add_argument("config_file", type=str, help="Path to config file")
    args = parser.parse_args()
    my_gpo_tester = GpoTester(args.config_file)

    if not my_gpo_tester.configure_gpos():
        exit(CONFIG_ERROR)

    my_gpo_tester.clear_gpos()
    my_gpo_tester.blink_gpos_in_sequence()
    my_gpo_tester.show_all_gpos()


if __name__ == "__main__":
    main()
