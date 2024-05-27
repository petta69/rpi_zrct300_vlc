from logger.logger import Logger
from lib.bravia_ssip import bravia_ssip


def main():
    print("Hello")
    my_bravia = bravia_ssip(host_ip="192.168.111.141", verbose=5)
#    my_bravia.send_power_on()

    my_bravia.get_power()



if __name__ == "__main__":
    main()