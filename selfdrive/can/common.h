#ifndef SELFDRIVE_CAN_COMMON_H
#define SELFDRIVE_CAN_COMMON_H

#include <cstddef>
#include <cstdint>
#include <string>

#define ARRAYSIZE(x) (sizeof(x)/sizeof(x[0]))


unsigned int honda_checksum(unsigned int address, uint64_t d, int l);
unsigned int toyota_checksum(unsigned int address, uint64_t d, int l);

struct SignalPackValue {
  const char* name;
  double value;
};


struct SignalParseOptions {
  uint32_t address;
  const char* name;
  double default_value;
};

struct MessageParseOptions {
  uint32_t address;
  int check_frequency;
};

struct SignalValue {
  uint32_t address;
  uint16_t ts;
  const char* name;
  double value;
};


enum SignalType {
  DEFAULT,
  HONDA_CHECKSUM,
  HONDA_COUNTER,
  TOYOTA_CHECKSUM,
};

struct Signal {
  const char* name;
  int b1, b2, bo;
  bool is_signed;
  double factor, offset;
  SignalType type;
};

struct Msg {
  const char* name;
  uint32_t address;
  unsigned int size;
  size_t num_sigs;
  const Signal *sigs;
};

struct DBC {
  const char* name;
  size_t num_msgs;
  const Msg *msgs;
};

const DBC* dbc_lookup(const std::string& dbc_name);

void dbc_register(const DBC* dbc);

#define dbc_init(dbc) \
static void __attribute__((constructor)) do_dbc_init_ ## dbc(void) { \
  dbc_register(&dbc); \
}

#endif
