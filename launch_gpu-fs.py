#!/usr/bin/env python3

#This is a job launch script for GPU FS project

import os
import sys
from uuid import UUID

from gem5art.artifact.artifact import Artifact
from gem5art.run import gem5Run
from gem5art.tasks.tasks import run_gem5_instance

packer = Artifact.registerArtifact(
    command = '''wget https://releases.hashicorp.com/packer/1.4.3/packer_1.4.3_linux_amd64.zip;
    unzip packer_1.4.3_linux_amd64.zip;
    ''',
    typ = 'binary',
    name = 'packer',
    path =  'disk-image/packer',
    cwd = 'disk-image',
    documentation = 'Program to build disk images. Downloaded sometime in August from hashicorp.'
)

experiments_repo = Artifact.registerArtifact(
        command = 'git clone https://github.com/darchr/gpu-fs-experiments.git',
    typ = 'git repo',
    name = 'gpu-fs-experiments',
    path =  './',
    cwd = '../',
    documentation = 'Experiments repo to run GPU full system with gem5'
)

gem5_repo = Artifact.registerArtifact(
    command = 'git clone https://gem5.googlesource.com/public/gem5',
    typ = 'git repo',
    name = 'gem5',
    path =  'gem5/',
    cwd = './',
    documentation = 'cloned gem5 master branch from googlesource (Nov 18, 2019)'
)

m5_binary = Artifact.registerArtifact(
    command = 'make -f Makefile.x86',
    typ = 'binary',
    name = 'm5',
    path =  'gem5/util/m5/m5',
    cwd = 'gem5/util/m5',
    inputs = [gem5_repo,],
    documentation = 'm5 utility'
)

disk_image = Artifact.registerArtifact(
    command = './packer build gpu-fs.json',
    typ = 'disk image',
    name = 'boot-disk',
    cwd = 'disk-image',
    path = 'disk-image/gpu-fs/gpu-fs-image/gpu-fs',
    inputs = [packer, experiments_repo, m5_binary,],
    documentation = 'Ubuntu with m5 binary installed and root auto login'
)

gem5_binary = Artifact.registerArtifact(
    command = '''cd gem5;
    git fetch "https://gem5.googlesource.com/amd/gem5" refs/changes/83/23483/1 && git cherry-pick FETCH_HEAD
    git fetch "https://gem5.googlesource.com/amd/gem5" refs/changes/84/23484/1 && git cherry-pick FETCH_HEAD
    git fetch "https://gem5.googlesource.com/amd/gem5" refs/changes/85/23485/4 && git cherry-pick FETCH_HEAD
    git fetch "https://gem5.googlesource.com/amd/gem5" refs/changes/43/23743/3 && git cherry-pick FETCH_HEAD
    scons build/X86/gem5.opt PROTOCOL = 'GPU_VIPER' TARGET_GPU_ISA = 'gcn3' BUILD_GPU = True -j8
    ''',
    typ = 'gem5 binary',
    name = 'gem5',
    cwd = 'gem5/',
    path =  'gem5/build/X86/gem5.opt',
    inputs = [gem5_repo,],
    documentation = 'Cloning the current tip, and cherry-picking the patches from the staging branch.'
)

if __name__ == "__main__":
    boot_types = ['systemd']
    num_cpus = ['1']
    #cpu_types = ['kvm', 'atomic', 'simple', 'o3']
    cpu_types = ['kvm']
    mem_types = ['ruby']

    for boot_type in boot_types:
        for cpu in cpu_types:
            for num_cpu in num_cpus:
                for mem in mem_types:
                    run = gem5Run.createFSRun(
                        'gem5/build/X86/gem5.opt',
                        'configs-boot-tests/run_exit.py',
                        'results/run_exit/vmlinux-{}/boot-exit/{}/{}/{}/{}'.
                        format(linux, cpu, mem, num_cpu, boot_type),
                        gem5_binary, gem5_repo, experiments_repo,
                        os.path.join('disk-image', 'vmlinux'),
                        'disk-image/gpu-fs/gpu-fs-image/gpu-fs',
                        linux_binaries[linux], disk_image,
                        cpu, mem, num_cpu, boot_type,
                        timeout = 6*60*60 #6 hours
                        )
                    run_gem5_instance.apply_async((run,))
