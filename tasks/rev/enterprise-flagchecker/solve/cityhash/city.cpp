// Copyright (c) 2011 Google, Inc.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.
//
// CityHash Version 1, by Geoff Pike and Jyrki Alakuijala
//
// This file provides a few functions for hashing strings. On x86-64
// hardware in 2011, CityHash64() is faster than other high-quality
// hash functions, such as Murmur.  This is largely due to higher
// instruction-level parallelism.  CityHash64() and CityHash128() also perform
// well on hash-quality tests.
//
// CityHash128() is optimized for relatively long strings and returns
// a 128-bit hash.  For strings more than about 2000 bytes it can be
// faster than CityHash64().
//
// Functions in the CityHash family are not suitable for cryptography.
//
// WARNING: This code has not been tested on big-endian platforms!
// It is known to work well on little-endian platforms that have a small penalty
// for unaligned reads, such as current Intel and AMD moderate-to-high-end CPUs.
//
// By the way, for some hash functions, given strings a and b, the hash
// of a+b is easily derived from the hashes of a and b.  This property
// doesn't hold for any hash functions in this file.

#include "city.h"

#include <algorithm>
#include <iostream>

using namespace std;

#define UNALIGNED_LOAD64(p) (*(const uint64*)(p))
#define UNALIGNED_LOAD32(p) (*(const uint32*)(p))

#if !defined(LIKELY)
#if defined(__GNUC__)
#define LIKELY(x) (__builtin_expect(!!(x), 1))
#else
#define LIKELY(x) (x)
#endif
#endif

// Some primes between 2^63 and 2^64 for various uses.
static const uint64 k0 = 0xc3a5c85c97cb3127ULL;
static const uint64 k1 = 0xb492b66fbe98f273ULL;
static const uint64 k2 = 0x9ae16a3b2f90404fULL;
static const uint64 k3 = 0xc949d7c7509e6557ULL;

// Bitwise right rotate.  Normally this will compile to a single
// instruction, especially if the shift is a manifest constant.
static uint64 Rotate(uint64 val, int shift) {
  // Avoid shifting by 64: doing so yields an undefined result.
  return shift == 0 ? val : ((val >> shift) | (val << (64 - shift)));
}

// Equivalent to Rotate(), but requires the second arg to be non-zero.
// On x86-64, and probably others, it's possible for this to compile
// to a single instruction if both args are already in registers.
static uint64 RotateByAtLeast1(uint64 val, int shift) {
  return (val >> shift) | (val << (64 - shift));
}

static uint64 ShiftMix(uint64 val) {
  return val ^ (val >> 47);
}

static uint64 HashLen16(uint64 u, uint64 v) {
  return Hash128to64(uint128(u, v));
}

static uint64 HashLen0to16(const char *s, size_t len) {
  if (len > 8) {
    uint64 a = UNALIGNED_LOAD64(s);
    uint64 b = UNALIGNED_LOAD64(s + len - 8);
    return HashLen16(a, RotateByAtLeast1(b + len, len)) ^ b;
  }
  if (len >= 4) {
    uint64 a = UNALIGNED_LOAD32(s);
    return HashLen16(len + (a << 3), UNALIGNED_LOAD32(s + len - 4));
  }
  if (len > 0) {
    uint8 a = s[0];
    uint8 b = s[len >> 1];
    uint8 c = s[len - 1];
    uint32 y = static_cast<uint32>(a) + (static_cast<uint32>(b) << 8);
    uint32 z = len + (static_cast<uint32>(c) << 2);
    return ShiftMix(y * k2 ^ z * k3) * k2;
  }
  return k2;
}

// This probably works well for 16-byte strings as well, but it may be overkill
// in that case.
static uint64 HashLen17to32(const char *s, size_t len) {
  uint64 a = UNALIGNED_LOAD64(s) * k1;
  uint64 b = UNALIGNED_LOAD64(s + 8);
  uint64 c = UNALIGNED_LOAD64(s + len - 8) * k2;
  uint64 d = UNALIGNED_LOAD64(s + len - 16) * k0;
  return HashLen16(Rotate(a - b, 43) + Rotate(c, 30) + d,
                   a + Rotate(b ^ k3, 20) - c + len);
}

// Return a 16-byte hash for 48 bytes.  Quick and dirty.
// Callers do best to use "random-looking" values for a and b.
static pair<uint64, uint64> WeakHashLen32WithSeeds(
    uint64 w, uint64 x, uint64 y, uint64 z, uint64 a, uint64 b) {
  a += w;
  b = Rotate(b + a + z, 21);
  uint64 c = a;
  a += x;
  a += y;
  b += Rotate(a, 44);
  return make_pair(a + z, b + c);
}

// Return a 16-byte hash for s[0] ... s[31], a, and b.  Quick and dirty.
static pair<uint64, uint64> WeakHashLen32WithSeeds(
    const char* s, uint64 a, uint64 b) {
  return WeakHashLen32WithSeeds(UNALIGNED_LOAD64(s),
                                UNALIGNED_LOAD64(s + 8),
                                UNALIGNED_LOAD64(s + 16),
                                UNALIGNED_LOAD64(s + 24),
                                a,
                                b);
}

// Return an 8-byte hash for 33 to 64 bytes.
static uint64 HashLen33to64(const char *s, size_t len) {
  uint64 z = UNALIGNED_LOAD64(s + 24);
  uint64 a = UNALIGNED_LOAD64(s) + (len + UNALIGNED_LOAD64(s + len - 16)) * k0;
  uint64 b = Rotate(a + z, 52);
  uint64 c = Rotate(a, 37);
  a += UNALIGNED_LOAD64(s + 8);
  c += Rotate(a, 7);
  a += UNALIGNED_LOAD64(s + 16);
  uint64 vf = a + z;
  uint64 vs = b + Rotate(a, 31) + c;
  a = UNALIGNED_LOAD64(s + 16) + UNALIGNED_LOAD64(s + len - 32);
  z = UNALIGNED_LOAD64(s + len - 8);
  b = Rotate(a + z, 52);
  c = Rotate(a, 37);
  a += UNALIGNED_LOAD64(s + len - 24);
  c += Rotate(a, 7);
  a += UNALIGNED_LOAD64(s + len - 16);
  uint64 wf = a + z;
  uint64 ws = b + Rotate(a, 31) + c;
  uint64 r = ShiftMix((vf + ws) * k2 + (wf + vs) * k0);
  return ShiftMix(r * k0 + vs) * k2;
}

uint64 CityHash64(const char *s, size_t len) {
  if (len <= 32) {
    if (len <= 16) {
      return HashLen0to16(s, len);
    } else {
      return HashLen17to32(s, len);
    }
  } else if (len <= 64) {
    return HashLen33to64(s, len);
  }

  // For strings over 64 bytes we hash the end first, and then as we
  // loop we keep 56 bytes of state: v, w, x, y, and z.
  uint64 x = UNALIGNED_LOAD64(s);
  uint64 y = UNALIGNED_LOAD64(s + len - 16) ^ k1;
  uint64 z = UNALIGNED_LOAD64(s + len - 56) ^ k0;
  pair<uint64, uint64> v = WeakHashLen32WithSeeds(s + len - 64, len, y);
  pair<uint64, uint64> w = WeakHashLen32WithSeeds(s + len - 32, len * k1, k0);
  z += ShiftMix(v.second) * k1;
  x = Rotate(z + x, 39) * k1;
  y = Rotate(y, 33) * k1;

  // Decrease len to the nearest multiple of 64, and operate on 64-byte chunks.
  len = (len - 1) & ~static_cast<size_t>(63);
  do {
    x = Rotate(x + y + v.first + UNALIGNED_LOAD64(s + 16), 37) * k1;
    y = Rotate(y + v.second + UNALIGNED_LOAD64(s + 48), 42) * k1;
    x ^= w.second;
    y ^= v.first;
    z = Rotate(z ^ w.first, 33);
    v = WeakHashLen32WithSeeds(s, v.second * k1, x + w.first);
    w = WeakHashLen32WithSeeds(s + 32, z + w.second, y);
    std::swap(z, x);
    s += 64;
    len -= 64;
  } while (len != 0);
  return HashLen16(HashLen16(v.first, w.first) + ShiftMix(y) * k1 + z,
                   HashLen16(v.second, w.second) + x);
}

int main() {
  cout << CityHash64("PY_MAIN", 7) << endl;
}
