#define KBUILD_MODNAME "foo"
#include <uapi/linux/bpf.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/if_vlan.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include <bpf/bpf_helpers.h>
#include <linux/tcp.h>

// Define a constant for the host IP address
#define HOST_IP_ADDR 0x0A011501

// Map to store packet timestamps
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, u16);
    __type(value, u64);
    __uint(max_entries, 1000000);
} time_map SEC(".maps");

// Perf buffer to store packet data
struct {
    __uint(type, BPF_MAP_TYPE_PERF_EVENT_ARRAY);
    __uint(key_size, sizeof(int));
    __uint(value_size, sizeof(u32));
} perf_map SEC(".maps");

static u32 parse_tcp_src(void* data, u64 nh_off, void *data_end){
	struct tcphdr *tcp_hd = data + nh_off;
	if(tcp_hd + 1 > data_end)
		return 0;
	return tcp_hd->source;
}

static u32 parse_tcp_dst(void* data, u64 nh_off, void *data_end){
	struct tcphdr *tcp_hd = data + nh_off;
	if(tcp_hd + 1 > data_end)
		return 0;
	return tcp_hd->dest;
}

static u32 parse_tcp_seq(void* data, u64 nh_off, void *data_end){
	struct tcphdr *tcp_hd = data + nh_off;
	if(tcp_hd + 1 > data_end)
		return 0;
	return tcp_hd->seq;
}

static u32 parse_tcp_ack_seq(void* data, u64 nh_off, void *data_end){
	struct tcphdr *tcp_hd = data + nh_off;
	if(tcp_hd + 1 > data_end)
		return 0;
	return tcp_hd->ack_seq;
}

static u16 parse_tcp_psh(void* data, u64 nh_off, void *data_end){
	struct tcphdr *tcp_hd = data + nh_off;
	if(tcp_hd + 1 > data_end)
		return 0;
	return tcp_hd->psh;
}

static int parse_ipv4(void *data, u64 nh_off, void *data_end)
{
	struct iphdr *iph = data + nh_off;

	if (iph + 1 > data_end)
		return 0;
	return iph->protocol;
}

static int parse_ipv6(void *data, u64 nh_off, void *data_end)
{
	struct ipv6hdr *ip6h = data + nh_off;

	if (ip6h + 1 > data_end)
		return 0;
	return ip6h->nexthdr;
}

static u8 parse_ip_hlen(void* data, u64 nh_off, void *data_end){
	struct iphdr *iph = data + nh_off;
	if(iph + 1 > data_end)
		return 0;
	return iph->ihl;
}

static u16 parse_check_sum(void* data, u64 nh_off, void *data_end){
	struct iphdr *iph = data + nh_off;
	if(iph + 1 > data_end)
		return 0;
	return iph->id;
}

static u8 parse_tos(void* data, u64 nh_off, void *data_end){
	struct iphdr *iph = data +nh_off;
	if(iph + 1 > data_end)	return 0;
	return iph->tos;
}

static u16 parse_tot_len(void* data, u64 nh_off, void *data_end){
	struct iphdr *iph = data + nh_off;
	if(iph + 1 > data_end)	return 0;
	return iph->tot_len;
}

static u32 parse_src_ip(void* data, u64 nh_off, void *data_end){
	struct iphdr *iph = data + nh_off;
	if(iph + 1 > data_end) return 0;
	return iph->saddr;
}

static u32 parse_dst_ip(void* data, u64 nh_off, void *data_end){
	struct iphdr *iph = data + nh_off;
	if(iph + 1 > data_end) return 0;
	return iph->daddr;
}

// XDP program entry point
SEC("xdp1")
int xdp_prog1(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    struct ethhdr *eth = data;
    int rc = XDP_PASS;
    long *value;
    u16 h_proto;
    u64 nh_off;
    u32 ipproto;

    // Calculate network header offset
    nh_off = sizeof(*eth);
    if (data + nh_off > data_end)
        return rc;

    // Parse Ethernet protocol
    h_proto = eth->h_proto;

    // Handle VLAN tagged packet
    if (h_proto == htons(ETH_P_8021Q) || h_proto == htons(ETH_P_8021AD)) {
        struct vlan_hdr *vhdr;
        vhdr = data + nh_off;
        nh_off += sizeof(struct vlan_hdr);
        if (data + nh_off > data_end)
            return rc;
        h_proto = vhdr->h_vlan_encapsulated_proto;
    }

    // Parse IP protocol
    if (h_proto == htons(ETH_P_IP))
        ipproto = parse_ipv4(data, nh_off, data_end);
    else if (h_proto == htons(ETH_P_IPV6))
        ipproto = parse_ipv6(data, nh_off, data_end);
    else
        ipproto = 0;

    // Parse source IP address
    u32 src_addr = parse_src_ip(data, nh_off, data_end);

    // Check for specific source IP address
    if (src_addr == htonl(HOST_IP_ADDR)) {
        // Parse various fields from the packet
        u16 id = parse_check_sum(data, nh_off, data_end);
        u64 time = bpf_ktime_get_ns();
        u8 tos = parse_tos(data, nh_off, data_end);
        u8 iph_len = parse_ip_hlen(data, nh_off, data_end);
        u16 tot_len = parse_tot_len(data, nh_off, data_end);
        nh_off += iph_len * 4;
        u16 tcp_src = parse_tcp_src(data, nh_off, data_end);
        u16 tcp_dst = parse_tcp_dst(data, nh_off, data_end);
        u32 tcp_seq = parse_tcp_seq(data, nh_off, data_end);
        u32 tcp_ack_seq = parse_tcp_ack_seq(data, nh_off, data_end);
        u16 tcp_psh = parse_tcp_psh(data, nh_off, data_end);

        // Structure to store packet data
        struct holo_pkt_info {
            u16 id;
            u8 tos;
            u8 iph_len;
            u16 tot_len;
            __be32 src_addr;
            __be32 dst_addr;
            u16 tcp_src;
            u16 tcp_dst;
            u32 tcp_seq;
            u32 tcp_ack_seq;
            u16 tcp_psh;
        } __packed;

        // Pair of timestamp and packet info
        struct holo_pkt {
            u64 key;
            struct holo_pkt_info value;
        } __packed holo_pkt_stat;

        // Populate holo_pkt_stat with parsed data
        holo_pkt_stat.key = time;
        holo_pkt_stat.value.id = id;
       	holo_pkt_stat.value.tos = tos;
	    holo_pkt_stat.value.tot_len = tot_len;
	    holo_pkt_stat.value.src_addr = src_addr;
	    holo_pkt_stat.value.dst_addr = dst_addr;
	    holo_pkt_stat.value.tcp_src =  tcp_src;
	    holo_pkt_stat.value.tcp_dst =  tcp_dst;
	    holo_pkt_stat.value.tcp_seq =  tcp_seq;
	    holo_pkt_stat.value.tcp_ack_seq =  tcp_ack_seq;
	    holo_pkt_stat.value.tcp_psh =  tcp_psh;

	    u64 flags = BPF_F_CURRENT_CPU;
	    int ret;
	    ret = bpf_perf_event_output(ctx,   &perf_map, flags,
					    &holo_pkt_stat, sizeof(holo_pkt_stat));
        if (ret < 0) {
            return ret;
        }

	    bpf_map_update_elem(&time_map,  &id, &time,BPF_ANY);

	    return rc;
}

char _license[] SEC("license") = "GPL";

