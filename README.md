# gpu-fs-experiments

This repo contains the artifacts for the GPU FullSystem project. It is based on [gem5art template|https://github.com/darchr/gem5art-template], and folows the semantics of gem5art. Artifacts included in this repo:
* disk-image: contains all relevant scripts to generate disk images and the images themselves.
* gem5-configs: contains gem5 configs.
* results: contains the experiment's results.
* A launch script. `launch_boot_tests.py` is an example launch script used in boot-test experiment.

To install gem5art,
```sh
pip install gem5art-artifact gem5art-run gem5art-tasks
```

[More details about gem5art](https://github.com/darchr/gem5art).

Additional steps to launch the experiment could be found [here](https://gem5art.readthedocs.io/en/latest/tutorials/boot-tutorial.html).
