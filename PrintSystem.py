from colorama import Fore, Back, Style

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

