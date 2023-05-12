#include <pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <winsock.h>
//Note: Use "g++ -o Capture_2 Capture_2.cpp -I"C:\Npcap SDK\Include" -L"C:\Program Files\Npcap\Lib\x64" -lwpcap -lws2_32" to compile
#define MAX_PACKETS 10
#define PCAP_FILE_PREFIX "capture_"

void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    static int packet_count = 0;
    char pcap_file_name[256];
    sprintf(pcap_file_name, "%s%d.pcap", PCAP_FILE_PREFIX, ++packet_count);

    pcap_dumper_t *dumpfile = pcap_dump_open((pcap_t *)user_data, pcap_file_name);
    if (dumpfile == NULL) {
        fprintf(stderr, "Error opening dump file\n");
        return;
    }

    pcap_dump((u_char *)dumpfile, pkthdr, packet);
    pcap_dump_close(dumpfile);

    printf("Packet #%d captured and saved to %s\n", packet_count, pcap_file_name);
}

int main() {
    pcap_t *handle;
    char errbuf[PCAP_ERRBUF_SIZE];
    char *dev;

    // Initialize Winsock
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup failed: %d\n", GetLastError());
        return 1;
    }

    // Find the default network device
    dev = pcap_lookupdev(errbuf);
    if (dev == NULL) {
        printf("Device not found: %s\n", errbuf);
        return 1;
    }

    // Open the network device
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL) {
        printf("Error opening device: %s\n", errbuf);
        return 1;
    }

    // Capture MAX_PACKETS packets
    if (pcap_loop(handle, MAX_PACKETS, packet_handler, (u_char *)handle) < 0) {
        fprintf(stderr, "\npcap_loop() failed: %s\n", pcap_geterr(handle));
        return 1;
    }

    // Close the pcap handle
    pcap_close(handle);
    printf("Capture complete.\n");

    // Clean up Winsock
    WSACleanup();

    return 0;
}
