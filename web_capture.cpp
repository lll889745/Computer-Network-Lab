#define _WIN32_WINNT 0x0501
//g++ -std=c++11 -o web_capture web_capture.cpp -I "C:\Program Files\Npcap\Include" -L "C:\Program Files\Npcap\Lib\x64" -lws2_32 -lpacket -lwpcap -mconsole
#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#include <atomic>
#include <chrono>
#include <ctime>
#include <fstream>
#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <pcap.h>
#include <stdlib.h>
#include <unistd.h>

struct iphdr
{
    unsigned char ihl : 4;
    unsigned char version : 4;
    unsigned char tos;
    unsigned short tot_len;
    unsigned short id;
    unsigned short frag_off;
    unsigned char ttl;
    unsigned char protocol;
    unsigned short check;
    unsigned int saddr;
    unsigned int daddr;
};

struct tcphdr
{
    unsigned short source;
    unsigned short dest;
    unsigned int seq;
    unsigned int ack_seq;
    unsigned short res1 : 4;
    unsigned short doff : 4;
    unsigned short fin : 1;
    unsigned short syn : 1;
    unsigned short rst : 1;
    unsigned short psh : 1;
    unsigned short ack : 1;
    unsigned short urg : 1;
    unsigned short res2 : 2;
    unsigned short window;
    unsigned short check;
    unsigned short urg_ptr;
};

#else
#include <netinet/ip.h>
#include <netinet/tcp.h>
#endif

std::atomic<int> captured_packets(0);
std::atomic<bool> stop_capture(false);
int max_packets = 10;
int timeout_seconds = 30;

void visit_website(const std::string& website) {
    std::string command = "curl -s -m " + std::to_string(timeout_seconds) + " " + website + " > /dev/null";
    system(command.c_str());
}

void packet_handler(u_char* user_data, const struct pcap_pkthdr* pkthdr, const u_char* pkt_data) {
    struct iphdr* ip_header = (struct iphdr*)(pkt_data + 14);
    uint16_t src_port = 0, dest_port = 0;

    if (ip_header->protocol == IPPROTO_TCP) {
        struct tcphdr* tcp_header = (struct tcphdr*)(pkt_data + 14 + ip_header->ihl * 4);
        src_port = ntohs(tcp_header->source);
        dest_port = ntohs(tcp_header->dest);
    }

    if (src_port == 80 || dest_port == 80) {
        captured_packets++;

        struct in_addr src_addr, dst_addr;
        src_addr.s_addr = ip_header->saddr;
        dst_addr.s_addr = ip_header->daddr;

        const char* src_ip = inet_ntoa(src_addr);
        const char* dst_ip =     inet_ntoa(dst_addr);

    std::cout << "Packet #" << captured_packets.load() << " - Source IP: " << src_ip
              << ", Destination IP: " << dst_ip << std::endl;
}

if (captured_packets.load() >= max_packets) {
    stop_capture.store(true);
}
}
int main(int argc, char *argv[]) {
// 初始化 Winsock
WSADATA wsaData;
int iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
if (iResult != 0) {
    std::cout << "WSAStartup failed with error: " << iResult << std::endl;
    return 1;
}

std::ifstream infile("website.txt");
std::string line;
std::vector<std::string> websites;

while (std::getline(infile, line)) {
    websites.push_back(line);
}

pcap_if_t* alldevs;
pcap_if_t* d;
pcap_t* adhandle;
char errbuf[PCAP_ERRBUF_SIZE];
int inum;

if (pcap_findalldevs(&alldevs, errbuf) == -1) {
    std::cerr << "Error in pcap_findalldevs: " << errbuf << std::endl;
    return 1;
}

inum = 0;
for (d = alldevs; d != NULL; d = d->next) {
    inum++;
}

d = alldevs;
adhandle = pcap_open_live(d->name, 65536, 1, 1000, errbuf);

if (adhandle == NULL) {
    std::cerr << "Error opening adapter: " << errbuf << std::endl;
    pcap_freealldevs(alldevs);
    return 1;
}

for (const auto& website : websites) {
    captured_packets.store(0);
    stop_capture.store(false);

    std::thread visitor_thread(visit_website, website);

    while (!stop_capture.load()) {
        pcap_loop(adhandle, 0, packet_handler, NULL);
        if (captured_packets.load() >= max_packets) {
            stop_capture.store(true);
        }
    }

    visitor_thread.join();
}

pcap_close(adhandle);
pcap_freealldevs(alldevs);
// 清理 Winsock
WSACleanup();
return 0;
}