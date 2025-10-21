### THIS IS A WORK IN PROGRESS -- YMMV, NO WARRANTY EXPRESSED OR IMPLIED. YOU CAN ENDANGER YOURSELF AND OTHERS.

# Pylon Venus Driver
This project integrates the Pylon compatible inverters with Victron Venus OS. It supports Pylon protocol mode by providing BMS data to the Sunny Island via the CAN bus (directly supported by socketcan devices). The software runs on the Venus OS device as a Venus driver and uses the Venus dbus to read/write data for use with the Venus device.

### Kudos to Victron Energy
Victron Engergy has provided much of the Venus OS architecture under Open Source copyright. This framework allows independent projects like this to exist. Even though we are using non-Victron hardware, we can include it into the Victron ecosystem with other Victron equipment. Victron stated that although they would not assist, they would not shut it down. Send support to Victron Energy by buying their products!

Tested with RPi 3B - v2.60 Build 20200906135923

### Kudos to Original SMA developer that this project was forked from

### Install

The provided install.sh script will copy files download dependencies and should provide a running configuration. It will not setup valid configuration values so don't expect this to be plug and play:

1. flash the included "candlelight" firmware image onto your CAN adapter using your computer (see CAN adapter below)
2. enable root access on your Venus device (see useful reading below)
3. from root login on the venus root home directory
4. connect the CAN adapter to your Venus / Raspberry Pi now. 
5. run wget https://github.com/warrenridley/PolyndriverVenus//install.sh
6. run chmod +x install.sh
7. run ./install.sh
8. answer Y to the install of the driver
9. answer Y to the dependencies (unless they are already installed)

## Victron VenusOS Notes

This project implements a com.victronenergy.vebus inverter/charger (like Multis, Quattros, Inverters) device so that the rest of the eco-system (web-ui, VRM portal, etc) grabs the data and displays/logs it.

Victron is amazing at letting Venus OS be open source AND documenting it VERY well so that hackers can have at it. Yeah, they are understandably not thrilled I'm using a third-party device with their free stuff, but aren't against me doing it and specifically didn't ask me to stop (I offered). So, go buy Victron stuff, even if you already have an SMA inverter. I have 4 of their solar charge controllers and love them!

That said, I'm not sure if I've emulated the Multiplus very well or in every way that I could. I did manage to reverse engineer the energy counting architecture so usage data should appear in the portal. But there are some quarks trying to do a 1-1 map Pylon to Victron. For example, the SMA reports inverter power flow and AC-2 (external) power flow, but not output power flow implicitly per line. So I had to do math (inverter power, External power, and output power should always sum to 0, right) to get that value. 

So the Victron system (or whatever you use this code with) will needs its own battery monitor or device to measure/calculate the SoC at a minimum, plus you have to hard code some voltage limits to makeup the minimum BMS messages the SunnyIsland requires. I recommend the Smart Shunt (https://www.victronenergy.com/battery-monitors/smart-battery-shunt) or the BMV-712 (https://www.victronenergy.com/battery-monitors/bmv-712-smart) connected to the Raspberry Pi with the VE.Direct USB cable. Note: The VE.Direct interface on these devices are 3.3V

### Useful Reading

Venus Developmental Info see https://github.com/victronenergy/venus/wiki/howto-add-a-driver-to-Venus .

Enable Root / SSH Access see https://www.victronenergy.com/live/ccgx:root_access#:~:text=Go%20to%20Settings%2C%20General,Access%20Level%20change%20to%20Superuser. 

Add additional modules (now handles by install script) sww https://github.com/victronenergy/venus/wiki/installing-additional-python-modules.

## Pylon compatible

The Sunny Island was originally designed to use Lead Acid batteries, only. Lithium-ion support was added as a firmware update and does not contain any BMS logic. It requires an external BMS to provide details of the battery SoC, SoH, charge current need, etc. If it does not receive valid BMS data within a period of time, it will shutdown.

### CAN Bus
The Controller Area Network (CAN bus) is used at a rate of 500 kbs.

NOTE: The SMA SI will go into hard shutdown mode if it hasn't received a good BMS message after several minutes. If this happens you will need to power off the DC side of the inverter and wait for 15-30 min capacitors to drain. If the cover is off, you can monitor the red LED located left and down of the center control panel. When it goes off it can be powered on.

SMA SI Manual: https://files.sma.de/downloads/SI4548-6048-US-BE-en-21W.pdf

Page 53, Section 6.4.2 Connecting the Data Cable of the Lithium-Ion Batteries details where to connect the RJ45 CAN cable

#### CAN Adapter
The SMA SI use the CAN bus to communicate between master/slave and other devices. In order to participate on the CAN bus, you must have a CAN adapter. The tested CAN adapter is the open source USB CANable device (https://canable.io/). Either version from https://store.protofusion.org/ will work. The firmware installed from ProtoFusion store is slcan, which emmulates a tty serial device. This project supports the "candlelight" FW by default, which will require a FW flash to the canable device. To flash your adapter, follow the directions here: https://canable.io/getting-started.html#flashing-new-firmware Use the ST DFU tool if you are on Windows. For more info, see: https://github.com/jaedog/SMAVenusDriver/wiki/Canable-Firmware.

##### CAN Pinouts
The Pylon uses an RJ45 connector for its CAN Bus interface. 

For a T-568B RJ45 pinout, the pins and colors are:
1. White Orange - Sync1 (reserved)
2. Orange - CAN_GND
3. White Green - SYNC_H
4. Blue - CAN_H
5. White Blue - CAN_L
6. Green - SYNC_L
7. White Brown - Sync7 (reserved)
8. Brown - Sync8 (reserved)

The pins of interest are:

* CAN_GND - Pin 2
* CAN_H - Pin 4
* CAN_L - Pin 5

It is worth noting that there is a terminating resistor on both the CAN and SYNC lines as part of the SMA RJ-45 terminator dongle. However, in my experience terminating the CAN bus alone has not caused any issues with Master/Slave comms.

## Final Words
There are still things hard-coded for specific applications. Although, configurability is improving. It supports the SMA as an off-grid (with grid available during low battery) with DC tied solar setup and the begining of support for AC coupled configurations. (See related project: https://github.com/jaedog/EnvoyVenusDriver for Enphase support). Note: The BMS logic is still **very crude** and may not work well depending on battery capacity or settings used. 

In case it wasn’t obvious, one fall back with this hack is if the Raspberry pi crashes or shuts off, the inverters will shut off as well. I recommend you have an offline back-up raspberry pi setup and ready to go to swap out in that event. 

## Todo List

 1)	Proper charge controller state machine <-- IN WORK
 2)	Move configuration values (charge current, voltage thresholds, etc) to the Victron settings structure. 
 3)	Create GUI in WEB_UI to change settings or trigger actions. 
 4)	Convert polling CAN adapter to proper callback when new CAN message arrives.
 5)	Get logging working correctly. 

## Tidbits

###### To determine if the driver is running execute:
> ps | grep dbus-sma
```
  supervise dbus-sma
  multilog t s25000 n4 /var/log/dbus-sma   <-- this will show up if logging is enabled
  python /data/etc/dbus-sma/dbus-sma.py
  grep dbus-sma
```

###### For debugging the script
1. Make sure the service auto start is disabled. Go to the /data/etc/dbus-sma directory.
2. Add the "down" file in ./service directory
```
	touch ./service/down   <-- creates an empty file named "down"
```
3. Stop the service if is running by:
```
	svc -d /service/dbus-sma
	svstat /service/dbus-sma   <-- checks if it is running, you can also do the ps cmd above
```
4. If you are using ssh to remote to the shell, you might want to be able to connect/disconnect the shell without disturbing the process. For that use "screen", a terminal multiplexer.
	1. screen  <-- starts a new screen
	2. CTRL+A,D  <-- disconnects from running screen
	3. screen -r  <-- reattaches to running screen
5. Now run the script: python dbus-sma.py
6. TBD logging... 

###### Venus Service

Venus uses daemontools (https://cr.yp.to/daemontools.html) to supervise and start the driver aka service.

## History

### Hacking the Sunny Island Notes

The SMA SunnyIsland 6048 has two potential communications buses. One is a CAN bus “ComSync” and the other is a RS-485 bus "ComSma" that requires an adapter card to be installed. The CAN bus is used by the SMA’s to communicate from the master to the slaves in a cluster, and to a Battery Management System (BMS) when configure in Lithium Ion mode. The RS-485 bus is required to connect to SMA grid tie inverters and to the WebBox.

It's clear the RS-485 was always the intended bus to connect to logging and telemetry systems such as the discontinued Sunny WebBox that allows you to see system telemetry on the SMA portal. But as they are very expensive now that they are discontinued, it isn’t a good option.

I started dumping the CAN bus to see what was there. There is of course a lot of high frequency messages I’m sure are used to sync up master and slave units, as well as the BMS traffic which is documented on page 10 of this BMS manual: http://www.rec-bms.com/datasheet/UserManual9R_SMA.pdf

BUT I also noticed there were some bytes in some messages moving in ways that appeared to correlate to system metrics. And indeed, they did. However, resolution is rather low, all power metrics are reported in 100s of watts. I realized this matched what is shown on the inverter screen, and then a light went off. You can buy the SMA “SunnyRemote” box which also connects by CAN bus. So these messages must be the system data meant for the “SunnyRemote” which has the same screen and menu as the local screen on the inverters. 

SO what this codes is doing is broken down into to big parts. First, it needs to pretend to be a BMS so the SunnyIslands will ingest battery SoC and charge current commands. Second, it is listening for the traffic intended for the “SunnyRemote” box so we can use it to extract ang log system metrics. All this is done through the CAN bus, so no additional parts need to be ordered. 

##Possible compatable inverters
EG4 6000XP
EG4 12000XP
Afore AF1~3.6K-ASL-0
Afore AF1~3.6K-ASL-1
Afore AF1~3.6K-SL-1
Afore AF1~6K-ASL-0
Afore AF1~6K-SL-0
Afore AF3~12K-THP
Afore AF3~12K-THP-0
Afore AF3~15K-THM
Afore AF3~15K-THM-0
Afore AF3~17K-THA
Afore AF3~30K-TH
Afore AF3~30K-TH-0
Afore AF3~6K-ASL
Afore AF3~6K-SL
Afore AF3~6K-THC
Afore AF3~7K-THMA
Afore AF3~7K-THMA-0
Afore AF3~9.6K-DH
Afore AF4~6K-SLP
AISWEI ASW05kH-T2
AISWEI ASW06kH-T2
AISWEI ASW08kH-T2
AISWEI ASW10kH-T2
AISWEI ASW12kH-T2
AISWEI ASW06H-T1
AISWEI ASW08H-T1
AISWEI ASW10H-T1
AISWEI ASW12H-T1
AISWEI ASW15H-T1
AISWEI ASW08kH-T3
AISWEI ASW10kH-T3
AISWEI ASW12kH-T3
AISWEI ASW3000H-S2
AISWEI ASW3680H-S2
AISWEI ASW4000H-S2
AISWEI ASW5000H-S2
AISWEI ASW6000H-S2
AP Systems ELS-5K
ATESS HPS30
ATESS HPS50
ATESS HPS100
ATESS HPS120
ATESS HPS150
AUXSOL ASG-3.6SL-ZH
AUXSOL ASG-5SL-ZH
AUXSOL ASG-6SL-ZH
AUXSOL ASG-5TL-ZH
AUXSOL ASG-12TL-ZH
CE+T Sierra 25 (380Vdc)
CE+T Sierra 25 (48Vdc)
CHINT POWER ECA3K-SNL-EU
CHINT POWER ECA6K-SNL-EU
CHINT POWER ECH3K-SML-EU
CHINT POWER ECH6K-SML-EU
Delios DLX HV
Deye SUN-29.9K-SG01HP3-EU/AU
Deye SUN-50K-SG01HP3-EU/AU
Deye SUN-5K-SG01HP3-EU/AU
Deye SUN-25K-SG01HP3-EU/AU
Deye SUN-SG01LP1
Deye SUN-SG03LP1
Deye SUN-SG04LP1
Deye SUN-SG04LP3
Dream Maker PCS-1-3kW-30A-1
Dream Maker PCS-1-8kW-30A-1
Dream Maker PCS-3-25kW-100A-1
Dream Maker PCS-3-50kW-100A-1
Dream Maker PCS-3-4kW-25A-1
Dream Maker PCS-3-20kW-40A-1
EAST EAHI-3000-SL
EAST EAHI-6000-SL
EATON xStorage Home 3P
Efacec Battery Inverter
EPEVER GS-MPPT-60M-200V
EPEVER GS-MPPT-80M-200V
EPEVER GS-MPPT-100M-200V
ETEK ETH-25KTL-HT
ETEK ETH-50KTL-HT
ETEK ETH-3KTL-HS
ETEK ETH-8KTL-HS
ETEK ETH-4KTL-HT
ETEK ETH-20KTL-HT
FSP PowerManager 4-15kW PMI III
FSP PowerManager Zero
Goodwe EH series
Goodwe BH series
Goodwe ET 5-10KW
Goodwe BT 5-10KW
Goodwe GW-BP
Goodwe GW-ES
Goodwe HVM-48
Goodwe LVM-48P
Goodwe M2000H-48
Goodwe M3000H-48
Goodwe M5000H-48
Goodwe SPH 3000
Goodwe SPH 6000
Goodwe SPF 12000T DVM-US
Goodwe SPF 2000
Goodwe SPF 5000
Goodwe SPF 5000 ES
Goodwe SPF 6000 ES PLUS
Growatt AC series
Growatt ES series
Growatt GF1-3K48S1
Growatt GF1-5K48S1
Growatt HAS-LV
Growatt HYS-LV
Growatt MKS IV 5.6KW-B
Growatt MKS IV 6KW TWIN
Growatt MAX II-8000
Growatt SE 4K6AC
Growatt SE 5KAC
Growatt SE 6KAC
Growatt SE 4K6HB-60
Growatt SE 5KHB-120
Growatt SE 6KHB-120
Growocol GW-MPS0030
Growocol GW-MPS0500
Growocol MEGA0030TS
Growocol MEGA0500TS
Growocol MEGA0630
Growocol MPS0030
Growocol MPS0500
Hoymiles (general)
HYPONTECH HBS
HYPONTECH HBT
HYPONTECH HHT
HYPONTECH HHS
HYT HAT-HV
HYT HYT-HV
Imeon Energy 3.6
Imeon Energy 3HV
Imeon Energy 3.7HV
Imeon Energy 4.6HV
Imeon Energy 5HV
Imeon Energy 9.12
INVT BD series
INVT XD5KTR
INVT XD6KTR
INVT XD8KTR
INVT XD10KTR
INVT XD12KTR
KOSTAL PLENTICORE BI xx/26
KOSTAL PLENTICORE BI xx/26 G2
KOSTAL PLENTICORE G3
KOSTAL PLENTICORE plus
KOSTAL PLENTICORE plus G2
KOYOE KY-EST06KH
KOYOE KY-EST20KH
LEDIT FVDi series
LEDIT FVDx series
Lux Power AA1.0 SNA
Lux Power ACS AA1.0
Lux Power Hybrid HB
Lux Power LXP 3-6K Hybrid AA1.0
Lux Power LXP-LB-EU
Lux Power LXP-LB-US
MEGAREVO (general)
Moixa TBB
MUST PV1800 VHM 3KW
MUST PV1800 VHM 5.5KW
Noark Ex9N-DH-3KS-AU
Noark Ex9N-DH-8KS-AU
Noark Ex9N-DH-5KT-AU
Noark Ex9N-DH-12KT-AU
OPTI-Solar (general)
Pramac PBI
RiiO 2KVA
RiiO 6KVA
RiiO 2KVA Sun
RiiO 6KVA Sun
RiiO 3KVA
RiiO 8KVA
RiiO 3KVA Sun II
RiiO 8KVA Sun II
SAJ H2-3K-S2
SAJ H2-6K-S2
SAJ H2-5K-T2
SAJ H2-10K-T2
Salicru EQX2 3001-HSX
Salicru EQX2 8002-HSX
Salicru EQX2 4002-HT
Salicru EQX2 12002-HT
Senergy SE 3KHB-HV
Senergy SE 6KHB-HV
Senergy SE 4K6AC
Senergy SE 5KAC
Senergy SE 6KAC
Senergy SE 4K6HB-60
Senergy SE 5KHB-120
Senergy SE 6KHB-120
Senergy SE 5KHB-D3
Senergy SE 30KHB-D3
Sermatec SMT-10K-TL-TH
Sermatec SMT-30K-TL-TH
Sermatec SMT-50K-TL-TH
Sermatec SMT-5K-TL-LV
SINENG SN3HSU
SINENG SN6HSU
SMA SBS 3.7-10
SMA SBS6.0-10
Sofar HYD 10000 TL-3PH
Sofar HYD 15000 TL-3PH
Sofar HYD 20000 TL-3PH
Sol-Ark 30K-3P-208V-N
Sol-Ark 60K-3P-480V-N
Sol-Ark Limitless 15K-LV
Sol-Ark 12K-3P-380V
Sol-Ark 12K-P
Sol-Ark 5K-120V
Sol-Ark 5K/8K-48-ST
Sol-Ark 8K-120/230V
Sol-Ark 8K-230-1P
Solinteg MHS-3K
Solinteg MHS-8K
Solinteg MHT-25K
Solinteg MHT-50K
Solinteg MHT-4K
Solinteg MHT-20K
Solinteg MRS-3K
Solinteg MRS-8K
Solinteg MRT-25K
Solinteg MRT-50K
Solinteg MRT-4K
Solinteg MRT-20K
Solis RAI
Solis RHI
Solis RHI-3P-HVES-5G
Solis RH1-1P-HVES-5G
Solis S5-EA1P3K-L
Solis S5-EH1P3K-L
Solis S5-EH1P6K-L
Solis S6-EA1P3.6K-L
Solis S6-EA1P6K-L
Solis S6-EH1P3K-L-EU
Solis S6-EH1P6K-L-EU
Solis S6-EH1P3.8K-H-US
Solis S6-EH1P11.4K-H-US
Solis S6-EH3P29.9K-H
Solis S6-EH3P50K-H
Solis S6-EH3P5K-H-EU
Solis S6-EH3P10K-H-EU
Solis S6-EO1P4K-48
Solis S6-EO1P5K-48
Sungrow SC
Sungrow SH5.0RT
Sungrow SH6.0RT
Sungrow SH8.0RT
Sungrow SH10.0RT
Sungrow SH5K
Sunways (general)
Tsun TSOL-H/A-3.0K-H
Tsun TSOL-H/A-6.0K-H
Victron Multiplus 48V
YARD FORCE PG3700-SH
YARD FORCE PG4600-SH
YARD FORCE PG5000-SH
YI ENERGY HI-3P10K-H-Y1
YI ENERGY HI-3P12K-H-Y1
YI ENERGY HI-3P5K-H-Y1
YI ENERGY HI-3P6K-H-Y1
YI ENERGY HI-3P8K-H-Y1
