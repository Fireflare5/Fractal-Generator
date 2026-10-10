unsigned long crcTable[256];

int crcTableComputed = 0;

void makeCRCTable()
{
    unsigned long int c;
    int n, k;

    for (n = 0; n < 256; ++n)
    {
        c = (unsigned long) n;

        for (k = 0; k < 8; ++k)
        {
            if (c & 1)
            {
                c = 0xEDB88320L ^ (c >> 1);
            } else {
                c = c >> 1;
            }
        }

        crcTable[n] = c;
    }

    crcTableComputed = 1;
}

unsigned long updateCRC(unsigned long crc, unsigned char *buf, int len)
{
    unsigned long c = crc;
    int n;

    if (!crcTableComputed)
    {
        makeCRCTable();
    }

    for (n = 0; n < len; ++n)
    {
        c = crcTable[(c ^ buf[n]) & 0xFF] ^ (c >> 8);
    }

    return c;
}

unsigned long crc(unsigned char *buf, int len)
{
    return updateCRC(0xFFFFFFFFL, buf, len);
}
