from arena_api.system import system
import time

def create_devices_with_tries():
    """
    This function waits for the user to connect a device before raising
    an exception
    """
    tries = 0
    tries_max = 6
    sleep_time_secs = 10
    while tries < tries_max:  # Wait for device for 60 seconds
        devices = system.create_device()
        if not devices:
            print(
                f'Try {tries+1} of {tries_max}: waiting for {sleep_time_secs} '
                f'secs for a device to be connected!')
            for sec_count in range(sleep_time_secs):
                time.sleep(1)
                print(f'{sec_count + 1 } seconds passed ',
                      '.' * sec_count, end='\r')
            tries += 1
        else:
            print(f'Created {len(devices)} device(s)')
            return devices
    raise Exception(f'No device found! Please connect a device and run '
                    f'the example again.')


def create_device_and_settings():
    # Create a device
    devices = create_devices_with_tries()
    device = devices[0]
    print(f'Device used in the example:\n\t{device}')

    # Get nodes ---------------------------------------------------------------
    nodes = device.nodemap.get_node(['Width', 'Height', 'PixelFormat'])

    # Nodes
    print('Setting Width to its maximum value')
    nodes['Width'].value = nodes['Width'].max

    print('Setting Height to its maximum value')
    height = nodes['Height']
    height.value = height.max

    # Set pixel format to PolarizedDolp_RGB8
    # 07.07 RGB8 - MONO8
    pixel_format_name = 'RGB8'
    print(f'Setting Pixel Format to {pixel_format_name}')
    nodes['PixelFormat'].value = pixel_format_name

    return device

def destroy_devices():
    system.destroy_device()
