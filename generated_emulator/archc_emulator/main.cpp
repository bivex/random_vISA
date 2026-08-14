/******************************************************
 * SystemC Main Entrypoint for ArchC parsed_archc_isa model  *
 * Generated automatically by random_vISA             *
 ******************************************************/

const char *project_name = "parsed_archc_isa";
const char *project_file = "parsed_archc_isa.ac";
const char *archc_version = "2.4.1";
const char *archc_options = "";

#include <iostream>
#include <systemc.h>
#include "ac_stats_base.H"
#include "parsed_archc_isa.H"

int sc_main(int ac, char *av[]) {
    std::cout << "============================================================" << std::endl;
    std::cout << "ArchC SystemC Simulator for parsed_archc_isa" << std::endl;
    std::cout << "WordSize = 32 bits, Num Vector Regs = 32" << std::endl;
    std::cout << "============================================================" << std::endl;

    parsed_archc_isa proc1("parsed_archc_isa");
    proc1.init(ac, av);
    proc1.set_prog_args();

    // Initial register state setup
    proc1.VRB.write(1, 10);
    proc1.VRB.write(2, 2);
    proc1.XRB.write(1, 5);

    sc_start();

    proc1.PrintStat();
    std::cout << std::endl;
    return proc1.ac_exit_status;
}