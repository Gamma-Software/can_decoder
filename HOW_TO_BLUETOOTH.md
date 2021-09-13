The following are instructions for connecting a Bluetooth device for serial communication on Arch Linux using BlueZ 5.31.


## Prerequisites

The following packages are required:

* `bluez`: `bluetoothd`
* `bluez-utils`: `bluetoothctl`, `rfcomm`


## Pair

1. Start daemon: `systemctl start bluetooth`
1. Pair using `bluetoothctl`:

   ```
   power on
   agent on
   scan on
   ... wait ...
   scan off
   pair <dev>
   ```

1. Create serial device: `rfcomm bind 0 <dev>`

You should now have `/dev/rfcomm0`.


## Unpair

1. Remove serial device: `rfcomm release 0`
1. Unpair using `bluetoothctl`:

   ```
   remove <dev>
   power off
   ```

1. Stop daemon: `systemctl stop bluetooth`


## Troubleshooting

Check `rfkill list` to make sure that the Bluetooth device is not blocked.