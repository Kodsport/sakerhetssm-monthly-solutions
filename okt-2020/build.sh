set -e

umount /tmp/ssmmount || true
dd if=/dev/zero of=drive bs=512 count=131072
mkfs.fat -F 32 drive
mkdir /tmp/ssmmount -p
mount drive /tmp/ssmmount

zip flag.zip flag.txt
mv flag.zip /tmp/ssmmount
cp Untitled.png /tmp/ssmmount

umount /tmp/ssmmount
python3 build.py
mount drive /tmp/ssmmount
