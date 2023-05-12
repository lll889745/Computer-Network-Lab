#include <pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <winsock.h>
//Note: Use "g++ -o capture capture.cpp -I"C:\Npcap SDK\Include" -L"C:\Program Files\Npcap\Lib\x64" -lwpcap -lws2_32" to compile
void packet_handler(unsigned char *user_data, const struct pcap_pkthdr *pkthdr, const unsigned char *packet) {
    static int packet_count = 0;
    printf("Packet #%d:\n", ++packet_count);
    printf("Packet length: %d\n", pkthdr->len);
    printf("\n");
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

    // Capture 10 packets
    if (pcap_loop(handle, 10, packet_handler, NULL) < 0) {
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
