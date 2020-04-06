#!/bin/bash

# Copyright (c) 2020 The Regents of the University of California.
# SPDX-License-Identifier: BSD 3-Clause

echo 'Installing ROCm'

echo blacklist amdgpu >> /etc/modprobe.d/blacklist.conf 

wget -qO - http://repo.radeon.com/rocm/apt/debian/rocm.gpg.key | apt-key add -

echo 'deb [arch=amd64] http://repo.radeon.com/rocm/apt/debian/ xenial main' | tee /etc/apt/sources.list.d/rocm.list

export DEBIAN_FRONTEND=noninteractive

apt update
apt install -y rocm-dkms

echo 'ROCm Installation Done'
