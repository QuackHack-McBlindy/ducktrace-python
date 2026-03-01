# **ducktrace‑python**

A duck‑themed logging system for Python, with colourful console output and automatic file logging.    

**🦆 Works seamlessly with the `ducktrace` family:**  
  - [ducktrace‑tui](https://github.com/QuackHack-McBlindy/ducktrace-tui) (TUI for Viewing logs and service management)  
  - [ducktrace‑logger](https://github.com/QuackHack-McBlindy/ducktrace-logger) (Rust apps)  
  - [ducktrace‑sh](https://github.com/QuackHack-McBlindy/ducktrace-sh) (Bash scripts)  


  
## **Features**

- **📄 Logs are written to `~/.config/duckTrace/` (configurable via `DT_LOG_PATH`)**

- **🎨 Colourful, duck‑themed console output**

- **📁 Respects `DT_LOG_LEVEL` and `DT_LOG_FILE` environment variables**

- **⏱️ Includes a `timed_function` decorator and `TranscriptionTimer` context manager for performance measurement**

- **🛠️ Simple `dt_debug`, `dt_info`, … functions for quick logging**


<br>   
  
## **Installation**


```bash
pip install ducktrace
```

Or directly from GitHub:  
  
  
```bash
pip install git+https://github.com/QuackHack-McBlindy/ducktrace-python.git
```

    
#### **NixOS (using flakes)**

  
Add the flake input to your flake.nix:

```nix
{
  inputs.ducktrace-python.url = "github:QuackHack-McBlindy/ducktrace-python";

  outputs = { self, nixpkgs, ducktrace-python, ... }: {
    nixosConfigurations.myMachine = nixpkgs.lib.nixosSystem {
      modules = [
        {
          environment.systemPackages = [
            ducktrace-python.packages.${system}.default
          ];
        }
      ];
    };
  };
}
```

  
  

#### **Build from source**


```bash
$ git clone https://github.com/QuackHack-McBlindy/ducktrace-python.git
$ cd ducktrace-python
$ pip install .
``` 


Or with Nix (inside the repo):

```bash
nix build
# result/ will contain the package
```   

## **Usage**

```python
import ducktrace

# Initialise logging (reads DT_LOG_LEVEL, DT_LOG_PATH, DT_LOG_FILE)
ducktrace.setup_ducktrace_logging()

ducktrace.dt_info("Application started")
ducktrace.dt_debug("This is a debug message")
ducktrace.dt_error("Something went wrong")

# Timing decorator
@ducktrace.timed_function()
def slow_function():
    time.sleep(1)

slow_function()

# Context manager timer
with ducktrace.TranscriptionTimer("database query") as timer:
    # … some work …
    timer.lap("after connect")
    # … more work …
```  
    

## **Environment Variables**


`$DT_LOG_LEVEL` – DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)

`$DT_LOG_PATH` – directory for log files (default: ~/.config/duckTrace/)

`$DT_LOG_FILE` – filename inside that directory (default: PyDuckTrace.log) 

  
  
<br><br>
  

## **License**

**MIT**
