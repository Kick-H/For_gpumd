Thanks. I have compared the stress results between NEP and ASE from the follow program:
```
#!/bin/bash
set -e
set -u

NEP=${your_dir}/GPUMD-output_stress_nep/src/nep

cd run_NEP
${NEP}

cd ../run_ASE
python run-ase.py
```

And the figure is shown here,
![energy](https://github.com/brucefan1983/GPUMD/assets/30561696/323a39f2-a104-478e-8892-f61b925976f8)
![force](https://github.com/brucefan1983/GPUMD/assets/30561696/27f5a4dc-f1a5-47e8-8538-1dee0cd3e153)
![stress](https://github.com/brucefan1983/GPUMD/assets/30561696/9d9c908d-1346-4f5e-a09d-3b4fcd70e0fe)
![virial](https://github.com/brucefan1983/GPUMD/assets/30561696/8b8a6448-11d4-4ed1-a0b2-683b59d7f83a)
