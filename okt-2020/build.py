import struct
import random

first_fat_cluster = 0x400C
first_shuffled_sector = 0x100600
zip_direntry_cluster = 0x10043A
png_direntry_cluster = 0x10047A

with open("drive", "rb") as f:
    drive = f.read()

pointer = first_fat_cluster
while struct.unpack("<I", drive[pointer : pointer + 4])[0]:
    pointer += 4

cluster_count = (pointer - first_fat_cluster) // 4
print("clusters to shuffle:", cluster_count)
order = list(range(cluster_count))
random.shuffle(order)
print("order:", order)

shuffled_drive = bytearray(drive)

# shuffle fat
for i in range(cluster_count):
    cluster_offset = first_fat_cluster + (i * 4)
    original_value = (
        struct.unpack("<I", drive[cluster_offset : cluster_offset + 4])[0] & 0xFFFFFFF
    )
    cluster_moves_here = order[i]
    moves_original_points_to = (
        struct.unpack(
            "<I",
            drive[
                first_fat_cluster
                + (cluster_moves_here * 4) : first_fat_cluster
                + (cluster_moves_here * 4)
                + 4
            ],
        )[0]
        & 0xFFFFFFF
    ) - 3
    new_pointer = (
        order.index(moves_original_points_to) + 3
        if moves_original_points_to < 0xFFFFFF8
        else moves_original_points_to
    )
    shuffled_drive[cluster_offset : cluster_offset + 4] = struct.pack(
        "<I", new_pointer,
    )

# copy fat1 to fat2
shuffled_drive[0x82200 : 0x82200 + 0x7E000] = drive[0x4000 : 0x4000 + 0x7E000]

# fix png start cluster
old_cluster = struct.unpack(
    "<H", drive[png_direntry_cluster : png_direntry_cluster + 2]
)[0]
new_cluster = order.index(old_cluster - 3) + 3
shuffled_drive[png_direntry_cluster : png_direntry_cluster + 2] = struct.pack(
    "<H", new_cluster
)

# fix zip start cluster
old_cluster = struct.unpack(
    "<H", drive[zip_direntry_cluster : zip_direntry_cluster + 2]
)[0]
new_cluster = order.index(old_cluster - 3) + 3
shuffled_drive[zip_direntry_cluster : zip_direntry_cluster + 2] = struct.pack(
    "<H", new_cluster
)

# shuffle sectors
for i in range(cluster_count):
    sector_offset = first_shuffled_sector + (i * 512)
    new_sector_offset = first_shuffled_sector + (order[i] * 512)
    shuffled_drive[sector_offset : sector_offset + 512] = drive[
        new_sector_offset : new_sector_offset + 512
    ]

# with open("drive", "wb") as f:
#     f.write(shuffled_drive)

# at this point the filesystem is fully functional again, just with sectors shuffled around, so lets break it again!
# delete cluster list for zip (mark zip as empty space, even though theres still a direntry pointing at it)

pointer = first_fat_cluster + (new_cluster - 3) * 4
while struct.unpack("<I", shuffled_drive[pointer : pointer + 4])[0] < 0xFFFFFF8:
    next_cluster = struct.unpack("<I", shuffled_drive[pointer : pointer + 4])[0]
    shuffled_drive[pointer : pointer + 4] = b"\x00" * 4
    pointer = first_fat_cluster + (next_cluster - 3) * 4
shuffled_drive[pointer : pointer + 4] = b"\x00" * 4

with open("drive", "wb") as f:
    f.write(shuffled_drive)
