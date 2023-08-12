import os
import urllib.request
from sys import platform

if platform in ("linux", "linux2", "darwin"):
    home = "~"
elif platform == "win32":
    home = "%USERPROFILE%/Desktop"
else:
    print("!! Unknown OS - Continuing with '~/' as Desktop path !!")
    home = "~"
    
def clear():
    os.system("cls;clear")

#### Menus ####


def main_menu():
    print(f""" ██ ██████   ██████     ████████  ██████   ██████  ██      ██   ██ ██ ████████ 
███      ██ ██             ██    ██    ██ ██    ██ ██      ██  ██  ██    ██    
 ██  █████  ██             ██    ██    ██ ██    ██ ██      █████   ██    ██    
 ██ ██      ██             ██    ██    ██ ██    ██ ██      ██  ██  ██    ██    
 ██ ███████  ██████        ██     ██████   ██████  ███████ ██   ██ ██    ██
\n\n\n\n================== MAIN MENU ==================\n[1] Main\n[2] Menu\n[3] Extra\n[4] Drivers\n[0] Exit\n\n\n\ndeclared home: {home}\ndeclared platform: {platform}""")

def main():
    print("""\n\n===== ADB Options =====\n[1] Device Information\n[2] Boot into Fastbootd\n[3] Boot into Bootloader/Fastboot\n[4] Boot into Recovery\n\n===== Fastboot Options =====\n[5] Device Information\n[6] Boot into System\n[7] Fix corrupted dm-verity\n\n!!! Not Implemented !!!\n[8] Manual Debloat\n""")

def menu():
    print("""\n\n[1] Flash Custom Recovery\n[2] Sideload OTA Package\n""")

def extra():
    print("""\n\n===== Bootloader Options =====\n[1] Unlock Bootloader\n[2] Lock Bootloader\n\n===== Backup Options =====\n[3] Back up IMEI\n[4] Back up partition\n\n===== Restore Options (Bootloader) =====\n[5] Restore IMEI\n[6] Restore vbmeta boot""")

def drivers():
    print("""\n\n===== Driver Options (WINDOWS ONLY) =====\n[1] Install ADB Drivers\n[2] Install PdaNet Drivers\n[3] Install usbdk64 Drivers\n""")


#### Modules ####

# 1 / Main - ADB #
def adb_deviceinfo():
    print("[>>] Printing device information (ADB)\n\nBrand:")
    os.system("adb shell getprop ro.product.manufacturer")
    print("\nDevice:")
    os.system("adb shell getprop ro.product.marketname")
    print("\nCodename:")
    os.system("adb shell getprop ro.product.device")
    print("\nModel:")
    os.system("adb shell getprop ro.product.cert")
    print("\nActive SIM Slot:")
    os.system("adb shell getprop ro.boot.slot")
    print("\nChipset:")
    os.system("adb shell getprop ro.boot.hardware")
    print("\nVNDK Version:")
    os.system("adb shell getprop ro.vndk.version")
    print("\nAndroid Version:")
    os.system("adb shell getprop ro.build.version.release")
    print("\nMIUI Version:")
    os.system("adb shell getprop ro.build.version.incremental")
    print("\nRegion:")
    os.system("adb shell getprop ro.miui.build.region")
    print("\nDisplay Info:")
    os.system("adb shell getprop sys.panel.display")
    print("\nBootloader Status:")
    os.system("adb shell getprop ro.secureboot.lockstate")
    print("\nEncryption Status:")
    os.system("adb shell getprop ro.crypto.state")
    print("\nBuild Date:")
    os.system("adb shell getprop ro.build.date")
    print("\nSecurity Patch Date:")
    os.system("adb shell getprop ro.build.version.security_patch")

    
def adb_bootfastbootd():
    print("[>>] Rebooting phone into Fastbootd mode")
    os.system("adb reboot fastboot")

def adb_bootfastboot():
    print("[>>] Rebooting phone into Bootloader/Fastboot mode")
    os.system("adb reboot bootloader")

def adb_bootrecovery():
    print("[>>] Booting phone into Recovery mode")
    os.system("adb reboot recovery")

# 1 / Main - Fastboot #

def fastboot_deviceinfo():
    print("[>>] Printing device information (Fastboot)\n\nBootloader Status:")
    os.system("fastboot getvar unlocked")
    print("\nActive SIM Slot:")
    os.system("fastboot getvar current-slot")
    print("\nCodename:")
    os.system("fastboot getvar product")

def fastboot_rebootsystem():
    print("[>>] Rebooting into System")
    os.system("fastboot reboot")

def dmverity_fix():
    print("[>>] Attempting to fix corrupted dm-verity")
    os.system("fastboot oem cdms")

# 2 / Menu #
def flash_recovery():
    fr = input(str("[!] Flashing recovery is *only* for codename *earth* devices as of right now, and may be unstable... Do you wish to continue?\n(Write 'I DO' to continue) ===>"))
    if fr == "I DO":
        frf = input(str("Drag & drop custom recovery img file ===> "))
        print("\n[>>] Flashing custom recovery...")
        os.system("fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img")
        os.system(f"fastboot flash boot {frf}")
        
def ota_sideload():
    otapkg = input(str("Drag & drop OTA package here ===> "))
    print("\n[>>] Attempting to sideload OTA package")
    os.system(f"adb sideload {otapkg}")

# 3 / Extra #
def bootloader_unlock():
    blu = input(str("[?] This option may not work, are you *sure* you want to continue?\n(Write 'I DO' to continue) ===>"))
    if blu == "I DO":
        os.system("fastboot flashing unlock")
    else:
        print("[?] User did not want to continue...")

def bootloader_lock():
    print("[>>] Attempting to lock bootloader")
    os.system("fastboot flashing lock")

def imei_backup():
    ib = input(str("[?] This option requires for your phone to be *rooted*, do you wish to continue?\n(Write 'I DO' to continue) ===>"))
    if ib == "I DO":
        print("[>>] Backing up IMEI, make sure to give the ADB shell root access!")
        os.system(f"""adb shell "su -c 'mkdir -p /sdcard/imeibackup && for part in proinfo nvcfg nvdata persist protect1 protect2; do dd if=/dev/block/platform/bootdevice/by-name/$part of=/sdcard/imeibackup/${part}.img; done && for part in seccfg nvram; do dd if=/dev/block/platform/bootdevice/by-name/$part of=/sdcard/imeibackup/${part}.bin; done'" && adb pull /sdcard/imeibackup {home}/""")
        print(f"[>>] Finished, if everything went well, the IMEI backup will be located at '{home}/imeibackup/'")   
    else:
        print("[?] User did not want to continue...")

def partition_backup():
    print("[>>] Backing up partition, sit tight...")
    dpath = f"{home}/partitionbackup"
    os.system(f"mkdir {dpath}")
    os.system(f"adb root")
    os.system(f"adb pull /dev/block/by-name/audio_dsp {dpath}/audio_dsp.img")
    os.system(f"adb pull /dev/block/by-name/boot {dpath}/boot.img")
    os.system(f"adb pull /dev/block/by-name/boot_para {dpath}/boot_para.img")
    os.system(f"adb pull /dev/block/by-name/cache {dpath}/cache.img")
    os.system(f"adb pull /dev/block/by-name/cam_vpu1 {dpath}/cam_vpu1.img")
    os.system(f"adb pull /dev/block/by-name/cam_vpu2 {dpath}/cam_vpu2.img")
    os.system(f"adb pull /dev/block/by-name/cam_vpu3 {dpath}/cam_vpu3.img")
    os.system(f"adb pull /dev/block/by-name/cdt_engineering {dpath}/cdt_engineering.img")
    os.system(f"adb pull /dev/block/by-name/dtbo {dpath}/dtbo.img")
    os.system(f"adb pull /dev/block/by-name/expdb {dpath}/expdb.img ")
    os.system(f"adb pull /dev/block/by-name/flashinfo {dpath}/flashinfo.img")
    os.system(f"adb pull /dev/block/by-name/frp {dpath}/frp.img")
    os.system(f"adb pull /dev/block/by-name/gz1 {dpath}/gz1.img")
    os.system(f"adb pull /dev/block/by-name/gz2 {dpath}/gz2.img")
    os.system(f"adb pull /dev/block/by-name/lk {dpath}/lk.img")
    os.system(f"adb pull /dev/block/by-name/lk2 {dpath}/lk2.img") 
    os.system(f"adb pull /dev/block/by-name/logo {dpath}/logo.img")
    os.system(f"adb pull /dev/block/by-name/md1img {dpath}/md1img.img")
    os.system(f"adb pull /dev/block/by-name/md_udc {dpath}/md_udc.img")
    os.system(f"adb pull /dev/block/by-name/metadata {dpath}/metadata.img")
    os.system(f"adb pull /dev/block/by-name/misc {dpath}/misc.img")
    os.system(f"adb pull /dev/block/by-name/my_custom {dpath}/my_custom.img")
    os.system(f"adb pull /dev/block/by-name/nvcfg {dpath}/nvcfg.img")
    os.system(f"adb pull /dev/block/by-name/nvdata {dpath}/nvdata.img")
    os.system(f"adb pull /dev/block/by-name/nvram {dpath}/nvram.img")
    os.system(f"adb pull /dev/block/by-name/oppo_custom {dpath}/oppo_custom.img")
    os.system(f"adb pull /dev/block/by-name/opporeserve1 {dpath}/opporeserve1.img")
    os.system(f"adb pull /dev/block/by-name/opporeserve2 {dpath}/opporeserve2.img")
    os.system(f"adb pull /dev/block/by-name/opporeserve3 {dpath}/opporeserve3.img")
    os.system(f"adb pull /dev/block/by-name/otp {dpath}/otp.img ")
    os.system(f"adb pull /dev/block/by-name/para {dpath}/para.img")
    os.system(f"adb pull /dev/block/by-name/persist {dpath}/persist.img")
    os.system(f"adb pull /dev/block/by-name/proinfo {dpath}/proinfo.img")
    os.system(f"adb pull /dev/block/by-name/protect1 {dpath}/protect1.img")
    os.system(f"adb pull /dev/block/by-name/protect2 {dpath}/protect2.img")
    os.system(f"adb pull /dev/block/by-name/recovery {dpath}/recovery.img")
    os.system(f"adb pull /dev/block/by-name/recovery_a {dpath}/recovery_a.img")
    os.system(f"adb pull /dev/block/by-name/scp1 {dpath}/scp1.img")
    os.system(f"adb pull /dev/block/by-name/scp2 {dpath}/scp2.img")
    os.system(f"adb pull /dev/block/by-name/sda {dpath}/sda.img")
    os.system(f"adb pull /dev/block/by-name/sdb {dpath}/sdb.img")
    os.system(f"adb pull /dev/block/by-name/sec1 {dpath}/sec1.img")
    os.system(f"adb pull /dev/block/by-name/seccfg {dpath}/seccfg.img")
    os.system(f"adb pull /dev/block/by-name/special_preload {dpath}/special_preload.img")
    os.system(f"adb pull /dev/block/by-name/spmfw {dpath}/spmfw.img")
    os.system(f"adb pull /dev/block/by-name/sspm_1 {dpath}/sspm_1.img")
    os.system(f"adb pull /dev/block/by-name/sspm_2 {dpath}/sspm_2.img")
    os.system(f"adb pull /dev/block/by-name/super {dpath}/super.img")
    os.system(f"adb pull /dev/block/by-name/tee1 {dpath}/tee1.img")
    os.system(f"adb pull /dev/block/by-name/tee2 {dpath}/tee2.img")
    os.system(f"adb pull /dev/block/by-name/vbmeta {dpath}/vbmeta.img")
    os.system(f"adb pull /dev/block/by-name/vbmeta_system {dpath}/vbmeta_system.img")
    os.system(f"adb pull /dev/block/by-name/vbmeta_vendor {dpath}/vbmeta_vendor.img")

def restore_imei():
    rid = input(str("Drag & drop IMEI backup folder ===> "))
    print("[>>] Restoring IMEI...")
    os.system(f"fastboot w seccfg,nvram,nvdata,nvcfg,protect1,protect2,persist,proinfo {rid}/seccfg.img,{rid}/nvram.img,{rid}/nvdata.img,{rid}/nvcfg.bin,{rid}/protect1.img,{rid}/protect2.img,{rid}/persist.img,{rid}/proinfo.bin")

def restore_partition():
    rid = input(str("Drag & drop partition backup folder ===> "))
    print("[>>] Restoring partition...")
    os.system(f"fastboot w audio_dsp,boot,boot_para,cache,cam_vpu1,cam_vpu2,cam_vpu3,cdt_engineering,dtbo,expdb,flashinfo,frp,gz1,gz2,lk,lk2,logo,mdlimg,md_udc,metadata,misc,my_custom,nvcfg,nvdata,nvram,oppo_custom,opporeserve1,opporeserve2,opporeserve3,otp,para,persist,proinfo,protect1,protect2,recovery,recovery_a,scp1,scp2,sda,sdb,sec1,seccfg,special_preload,spmfw,sspm_1,sspm_2,super,tee1,tee2,vbmeta,vbmeta_system,vbmeta_vendor {rid}/audio_dsp.img,{rid}/boot.img,{rid}/boot_para.img,{rid}/cache.img,{rid}/cam_vpu1.img,{rid}/cam_vpu2.img,{rid}/cam_vpu3.img,{rid}/cdt_engineering.img,{rid}/dtbo.img,{rid}/expdb.img,{rid}/flashinfo.img,{rid}/frp.img,{rid}/gz1.img,{rid}/gz2.img,{rid}/lk.img,{rid}/lk2.img,{rid}/logo.img,{rid}/mdlimg.img,{rid}/md_udc.img,{rid}/metadata.img,{rid}/misc.img,{rid}/my_custom.img,{rid}/nvcfg.img,{rid}/nvdata.img,{rid}/nvram.img,{rid}/oppo_custom.img,{rid}/opporeserve1.img,{rid}/opporeserve2.img,{rid}/opporeserve3.img,{rid}/otp.img,{rid}/para.img,{rid}/persist.img,{rid}/proinfo.img,{rid}/protect1.img,{rid}/protect2.img,{rid}/recovery.img,{rid}/recovery_a.img,{rid}/scp1.img,{rid}/scp2.img,{rid}/sda.img,{rid}/sdb.img,{rid}/sec1.img,{rid}/seccfg.img,{rid}/special_preload.img,{rid}/spmfw.img,{rid}/sspm_1.img,{rid}/sspm_2.img,{rid}/super.img,{rid}/tee1.img,{rid}/tee2.img,{rid}/vbmeta.img,{rid}/vbmeta_system.img,{rid}/vbmeta_vendor.img")

# 4 / DRIVERS #
def install_adb_driver():
    print("[>>] Downloading & running ADB driver installer...")
    urllib.request.urlretrieve("https://cdn.discordapp.com/attachments/545659735903567874/1133155743852400782/adb-setup-1.4.3.exe", "%USERPROFILE%\Downloads\adb-setup-1.4.3.exe")
    os.system("%USERPROFILE%\Downloads\adb-setup-1.4.3.exe")

def install_pdanet_driver():
    print("[>>] Downloading & running PdaNet driver installer...")
    urllib.request.urlretrieve("https://cdn.discordapp.com/attachments/545659735903567874/1133155744246669382/PdaNetA5221.exe", r"%USERPROFILE%\Downloads\PdaNetA5221.exe")
    os.system(r"%USERPROFILE%\Downloads\PdaNetA5221.exe")
    
def install_usbdk64_driver():
    print("[>>] Downloading & running usbdk64 installer...")
    if platform.architecture()[0] == "64bit":
        urllib.request.urlretrieve("https://cdn.discordapp.com/attachments/545659735903567874/1133155744791941271/UsbDk_1.0.22_x64.msi", r"%USERPROFILE%\Downloads\UsbDk_1.0.22_x64.msi")
        os.system(r"%USERPROFILE%\Downloads\UsbDk_1.0.22_x64.msi")
    elif platform.architecture()[0] == "32bit":
        urllib.request.urlretrieve("https://cdn.discordapp.com/attachments/545659735903567874/1133155745127469109/UsbDk_1.0.22_x86.msi", r"%USERPROFILE%\Downloads\UsbDk_1.0.22_x86.msi")
        os.system(r"%USERPROFILE%\Downloads\UsbDk_1.0.22_x86.msi")

### Execution ###
def rtime():
    clear()
    main_menu()
    choice = input("===> ")
    if choice == "1":#main
        clear()
        main()
        choice = input("===> ")
        if choice == "1":
            adb_deviceinfo()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "2":
            adb_bootfastbootd()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "3":
            adb_bootfastboot
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "4":
            adb_bootrecovery
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "5":
            fastboot_deviceinfo()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "5":
            fastboot_rebootsystem()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "6":
            dmverity_fix()
            input("\n\nPress any key to continue...")
            rtime()
        else:
            print("Invalid input, returning to main menu...")
            rtime()
    elif choice == "2":#menu
        clear()
        menu()
        choice = input("===> ")
        if choice == "1":
            flash_recovery()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "2":
            ota_sideload()
            input("\n\nPress any key to continue...")
            rtime()
        else:
            print("Invalid input, returning to main menu...")
            rtime()
    elif choice == "3":#extra
        clear()
        extra()
        choice = input("===> ")
        if choice == "1":
            bootloader_unlock()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "2":
            bootloader_lock()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "3":
            imei_backup()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "4":
            partition_backup()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "5":
            restore_imei()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "6":
            restore_partition()
            input("\n\nPress any key to continue...")
            rtime()
        else:
            print("Invalid input, returning to main menu...")
            rtime()
    elif choice == "4":
        clear()
        drivers()
        choice = input("===> ")
        if choice == "1":
            install_adb_driver()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "2":
            install_pdanet_driver()
            input("\n\nPress any key to continue...")
            rtime()
        elif choice == "3":
            install_usbdk64_driver()
            input("\n\nPress any key to continue...")
            rtime()
        else:
            print("Invalid input, returning to main menu...")
            rtime()
    elif choice == "0":
        print("Thank you for using my tool!\nMade with love by synth, goodbye!")
        exit()
    else:
        print("Invalid input")
        rtime()

rtime()
