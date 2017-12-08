#!/bin/sh
update_packet_base_path='/root/works/program-update'
program_base_path='/root/works/xmppserver'

if [ ! -d "$update_packet_base_path" ]; then
	echo "the update packet path is wrong: "$update_packet_base_path
	exit 0
fi

if [ ! -d "$program_base_path" ]; then
	echo "the program xmppserver path is wrong: "$program_base_path
	exit 0
fi

new_program=$update_packet_base_path/xmppserver-packet-new/xmppserver
run_program=$program_base_path/xmppserver

if [ ! -f "$new_program" ]; then
	echo "the new program xmppserver is none: "$new_program
	exit 0
fi

echo "updating packet path: "$new_program

if [ -f "$run_program" ]; then
	cmp -s $new_program  $run_program
	if [ $? -eq 0 ]; then
		echo "the program is already the newest..."
		exit 0
	fi
fi

echo "running program path: "$run_program

time=`date "+%Y-%m-%d-%H:%M:%S"`
sudo supervisorctl stop xmppserver  > /dev/null 2>&1

echo "supervisor stopped xmppserver "

if [ ! -d "$update_packet_base_path/xmppserver-packet-old" ]; then
	mkdir $update_packet_base_path/xmppserver-packet-old
fi

mv "$run_program" $update_packet_base_path/xmppserver-packet-old/xmppserver-$time

echo "backup xmppserver program to: "$update_packet_base_path/xmppserver-packet-old/xmppserver-$time
cp $new_program $run_program
chmod 0700 $run_program
sudo supervisorctl start xmppserver  > /dev/null 2>&1
echo "supervisor started xmppserver "
echo "program xmppserver update ok"
