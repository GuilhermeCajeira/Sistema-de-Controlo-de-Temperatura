from colorama import Fore, Back, Style


def print_configEnvironment(exterior_temp, time_of_day, room_division, desired_temperature):
    if exterior_temp == "Hot":
        exterior_temp = "Hot "

    if time_of_day == "Morning":
        time_of_day = " Morning "
    elif time_of_day == "Night":
        time_of_day = "  Night  "

    if room_division == "Bedroom":
        room_division = "  Bedroom  "
    elif room_division == "Office":
        room_division = "  Office   "

    # Prints the configuration of the environment
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "_____________________________________" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "|---- Configuration Environment ----|" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.WHITE + "|-      Exterior Temperature:      -| " + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTBLUE_EX + f"|                {exterior_temp}               |" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.WHITE + "|-           Time of Day:          -| " + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + f"|             {time_of_day}             |" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.WHITE + "|-         Room Division:          -| " + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTMAGENTA_EX + f"|            {room_division}            |" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "|___________________________________|" + Style.RESET_ALL)
    print('\n')   

    print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + f"Inicial System Temperature: {desired_temperature}°C" + Style.RESET_ALL)
    print('\n\n')


def print_PIDoutput(pid_output, current_temperature, desired_temperature):
    # Prints PID controller output and current temperature information
    print(Style.BRIGHT + "=     Desired Temperature: " + Fore.YELLOW + f"{desired_temperature:.2f}°C     =" + Style.RESET_ALL)
    
    if pid_output.PIDoutput > 0.01:
        print(Style.BRIGHT + "=     Current Temperature: " + Fore.RED + f"{current_temperature:.2f}°C     =" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.RED + "=       Temperature increasing...      =" + Style.RESET_ALL)
    elif pid_output.PIDoutput < -0.01:
        print(Style.BRIGHT + "=     Current Temperature: " + Fore.BLUE + f"{current_temperature:.2f}°C     =" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.BLUE + "=       Temperature decreasing...      =" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + "=     Current Temperature: " + Fore.GREEN + f"{current_temperature:.2f}°C     =" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.GREEN + "=          Temperature stable.         =" + Style.RESET_ALL)

    if pid_output.PIDoutput < 0:
        print(Style.BRIGHT + f"=       Controller Error: {pid_output.PIDoutput:.3f}       =" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + f"=       Controller Error: {pid_output.PIDoutput:.3f}        =" + Style.RESET_ALL)

    print('\n\n')

