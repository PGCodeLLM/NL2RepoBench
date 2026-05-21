# Nl2RepoBench

## Project Overview

NL2Repo is a benchmark designed to evaluate the performance of Large Language Models (LLMs) and coding agents on **long-horizon tasks** that require generating a **complete, runnable code repository from scratch (0-to-1)**. The benchmark consists of **104 distinct tasks**, each paired with its own testing environment.

## Running the Code

The current setup runs OpenHands in **headless batch mode**. Model behavior is controlled via the `config.toml` file. If you need to change the model configuration, please modify `config.toml` **before** starting the run.

The system currently uses a **file-to-file** execution workflow and manages Docker containers via **python-on-whales**. At the moment, **only local execution is supported**.

> **Note:** When running in headless mode across multiple machines, you must set up shared file management (e.g., NFS) or manually transfer files to the target machines in advance.

### Prerequisites

Before starting, ensure that Docker is installed locally and that the following images are available:

- `docker.all-hands.dev/all-hands-ai/openhands:0.56`
- `docker.all-hands.dev/all-hands-ai/runtime:0.56-nikolaik`

The runtime image can be customized. The default image is sufficient for running Python-based tasks and comes with **Python 3.12** preinstalled. If you need to support other languages, you can build your own runtime image and update the corresponding configuration in `openhands/openhands_app.py` (line 176).

## Data Layout

1. The `test_files` directory contains all repository-related task data, including:
   - A `.txt` file specifying the number of test cases
   - The repository documentation in `.md` format
   - Two `.json` files used for testing

2. All Docker volume mounts used for headless execution are stored in the `workspaces` directory. Each task is assigned a **unique UUID directory**. The task-specific configuration file is copied from a template and modified accordingly (mainly to mount the workspace directory into the runtime container).

3. Final results are saved in the `result` directory. Each task produces a single aggregated `.json` file, named using the task’s randomly generated UUID.

4. The project is launched using a `config.json` file. A sample configuration is shown below:

```json
{
  "startPro": [
    {
      "moduleName": "",
      "baseUrl": "",
      "sk": "",
      "proNameList": [
        "math-verify"
      ]
    }
  ],
  "max_pool_size": 20
}
```

### Configuration Fields

- **startPro**: A list of task nodes.
  - Each node corresponds to a single model configuration.
  - **proNameList**: A list of task names, which must match the subdirectory names under `test_files`.

- **max_pool_size**: The maximum number of concurrent threads. Once this limit is reached, additional tasks will be queued until resources become available.

### Additional notes
- ```bash pull_nl2r_openhands_images.sh``` to pull images
- Endpoints should have /v1 at the end
- LiteLLM endpoints should use the openai/ prefix, apparently
- Model used needs to be specified in both config.json and template/config.template.toml
- Approximate costs - running an easy task with Qwen3-235B took about $5 on NewAPI (5RMB?)
- Models with "." in the name should have them replaced with "_"
- Some test_commands.json may be incorrectly formatted and give errors? Those may need to be changed when encountered
  - E.g.
  ```["touch README.md && pip install -e .","pytest --continue-on-collection-errors tests"]``` should become ```["sh -c 'touch README.md && pip install -e .'","pytest --continue-on-collection-errors tests"]```
- The source for the docker images was changed to ghcr.io because the old one was dead
- Existing config.template.toml now has network set to host because the containers can't communicate without it on Linux
- If something breaks, you'll need to stop the Docker containers from autodeleting in openhands_app.py. Set ```auto_remove=False```, and get Codex or your other tool of choice to modify the code to not rely on periodic polling for container deletion to determine the end of a run. Then, run ```bash get_docker_logs.sh``` - the logs will be dumped in ```docker_logs/```.
```bash run_nl2r_test.sh``` to start. Specify run number in the bash script
- i wish whoever was responsible for the documentation of this repo or lack thereof a very bad day