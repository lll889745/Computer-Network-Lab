//Note: Use "g++ -o Capture_3 Capture_3.cpp -I"C:\Npcap SDK\Include" -L"C:\Program Files\Npcap\Lib\x64" -lwpcap -lws2_32" to compile
#include <pcap.h>
#include <stdio.h>
//实现对抓包数量、协议进行限制
void packet_handler(u_char *dumpfile, const struct pcap_pkthdr *header, const u_char *packet) {
    static int packet_count = 0;

    // Dump the packet to the file
    pcap_dump(dumpfile, header, packet);

    printf("Packet #%d:\n", ++packet_count);
    printf("Packet length: %d\n", header->len);
    printf("\n");
}

int main(int argc, char **argv) {
    char *dev, errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    pcap_dumper_t *dumpfile;
    bpf_program filter;         // Compiled filter expression
    char filter_exp[] = "tcp"; // Filter expression
    int num_packets = 100;       // Number of packets to capture

    // Find the default network device
    dev = pcap_lookupdev(errbuf);
    if (dev == NULL) {
        fprintf(stderr, "Couldn't find default device: %s\n", errbuf);
        return(2);
    }

    // Open the device for packet capture
    handle = pcap_open_live(dev, BUFSIZ, 1, 1000, errbuf);
    if (handle == NULL) {
        fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
        return(2);
    }

    // Compile and apply the filter expression
    if (pcap_compile(handle, &filter, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == -1) {
        fprintf(stderr, "Couldn't parse filter %s: %s\n", filter_exp, pcap_geterr(handle));
        return(2);
    }
    if (pcap_setfilter(handle, &filter) == -1) {
        fprintf(stderr, "Couldn't install filter %s: %s\n", filter_exp, pcap_geterr(handle));
        return(2);
    }

    // Open the dump file
    dumpfile = pcap_dump_open(handle, "capture.pcap");
    if (dumpfile == NULL) {
        fprintf(stderr, "Couldn't open dump file\n");
        return(2);
    }

    // Capture packets
    pcap_loop(handle, num_packets, packet_handler, (u_char *)dumpfile);

    // Close the dump file and free the handle
    pcap_dump_close(dumpfile);
    pcap_close(handle);

    printf("Capture complete.\n");

    return(0);
}
