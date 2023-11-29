#include <linux/bpf.h>
#include <linux/if_link.h>
#include <assert.h>
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <libgen.h>
#include <sys/resource.h>
#include <net/if.h>

#include "bpf_util.h"
#include <bpf/bpf.h>
#include <bpf/libbpf.h>
#include <netinet/in.h>

// Global variables
static int ifindex;
static __u32 xdp_flags = XDP_FLAGS_UPDATE_IF_NOEXIST;
static __u32 prog_id;
static struct perf_buffer *pb = NULL;

// Function to handle program exit
static void int_exit(int sig) {
    __u32 curr_prog_id = 0;

    // Get the current XDP program ID
    if (bpf_get_link_xdp_id(ifindex, &curr_prog_id, xdp_flags)) {
        printf("bpf_get_link_xdp_id failed\n");
        exit(1);
    }
    // Detach the XDP program if it is still attached
    if (prog_id == curr_prog_id)
        bpf_set_link_xdp_fd(ifindex, -1, xdp_flags);
    else if (!curr_prog_id)
        printf("couldn't find a prog id on a given interface\n");
    else
        printf("program on interface changed, not removing\n");
    exit(0);
}

// Print usage information
static void usage(const char *prog) {
    fprintf(stderr,
        "usage: %s [OPTS] IFACE\n\n"
        "OPTS:\n"
        "    -S    use skb-mode\n"
        "    -N    enforce native mode\n"
        "    -F    force loading prog\n",
        prog);
}

// Structure for holding packet info
struct holo_pkt_info{
    u16 id;
    u8  tos;
    u8  iph_len;
    u16 tot_len;
    __be32 src_addr;
    __be32 dst_addr;
    u16 tcp_src;
    u16 tcp_dst;
    u32 tcp_seq;
    u32 tcp_ack_seq;
    u16 tcp_psh;
} __packed;

// Callback function for perf buffer output
static void print_pb_bpf_output(void *ctx, int cpu, void *data, __u32 size) {
    struct holo_pkt {
        u64 key;
        struct holo_pkt_info value;
    } __packed holo_pkt_stat;

    struct holo_pkt* e = data;
    __u64 k = e->key;
    struct holo_pkt_info v = e->value;
    // Print packet information with proper ntoh conversion
    printf("time %llu tos_val: %u id: %x tot_len: %u iph_len: %u src_addr: %x dst_addr: %x tcp_src: %u tcp_dst: %u tcp_seq: %x tcp_ack_seq: %x tcp_psh: %u\n",
        k, v.tos, ntohs(v.id), ntohs(v.tot_len), v.iph_len, ntohl(v.src_addr), ntohl(v.dst_addr), ntohs(v.tcp_src), ntohs(v.tcp_dst), ntohl(v.tcp_seq), ntohl(v.tcp_ack_seq), v.tcp_psh);
}

int main(int argc, char **argv) {
    // Program setup
    struct bpf_prog_load_attr prog_load_attr = {
        .prog_type = BPF_PROG_TYPE_XDP,
    };
    struct bpf_prog_info info = {};
    __u32 info_len = sizeof(info);
    const char *optstr = "FSN";
    int prog_fd, map_fd, opt;
    struct bpf_object *obj;
    struct bpf_map *map;
    char filename[256];
    int err;

    // Command-line argument parsing
    while ((opt = getopt(argc, argv, optstr)) != -1) {
        switch (opt) {
        case 'S':
            xdp_flags |= XDP_FLAGS_SKB_MODE;
            break;
        case 'N':
            xdp_flags |= XDP_FLAGS_DRV_MODE;
            break;
        case 'F':
            xdp_flags &= ~XDP_FLAGS_UPDATE_IF_NOEXIST;
            break;
        default:
            usage(basename(argv[0]));
            return 1;
        }
    }

    // Interface index setup
    ifindex = if_nametoindex(argv[optind]);
    if (!ifindex) {
        perror("if_nametoindex");
        return 1;
    }

    snprintf(filename, sizeof(filename), "%s_kern.o", argv[0]);
    prog_load_attr.file = filename;

    // Load BPF program
    if (bpf_prog_load_xattr(&prog_load_attr, &obj, &prog_fd))
        return 1;

    // Find the map within the BPF program
    map = bpf_map__next(NULL, obj);
    if (!map) {
        printf("finding a map in obj file failed\n");
        return 1;
    }
    map_fd = bpf_map__fd(map);

    if (!prog_fd) {
        printf("bpf_prog_load_xattr: %s\n", strerror(errno));
        return 1;
    }

    // Set up signal handling for graceful exit
    signal(SIGINT, int_exit);
    signal(SIGTERM, int_exit);

    // Attach the BPF program to the specified interface
    if (bpf_set_link_xdp_fd(ifindex, prog_fd, xdp_flags) < 0) {
        printf("link set xdp fd failed\n");
        return 1;
    }

    // Retrieve and check BPF program info
    err = bpf_obj_get_info_by_fd(prog_fd, &info, &info_len);
    if (err) {
        printf("can't get prog info - %s\n", strerror(errno));
        return err;
    }
    prog_id = info.id;

    // Set up and start the performance buffer
    int perf_map_fd = bpf_object__find_map_fd_by_name(obj, "perf_map");
    if (perf_map_fd < 0) {
        fprintf(stderr, "ERROR: finding perf map in obj file failed\n");
        return 1;
    }

    struct perf_buffer_opts pb_opts = {};
    pb_opts.sample_cb = print_pb_bpf_output;
    pb = perf_buffer__new(perf_map_fd, 8, &pb_opts);
    err = libbpf_get_error(pb);
    if (err) {
        perror("perf_buffer setup failed");
        return 1;
    }

    // Poll the performance buffer and handle events
    int ret;
    while ((ret = perf_buffer__poll(pb, 500)) >= 0) {
    }

    // Clean up resources on exit
    kill(0, SIGINT);
    return 0;
}
