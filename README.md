# get python 3.13

however you want to

# get uv

`pip install uv`

## make a venv

`uv venv`

## build/run

`uv build` creates the wheel file.

`uv run <whatever command>` executes whatever command from within the venv.

## also

check out the `uv` command and `uv help` to figure out what's going on with uv.

# get just (optional)

- get the rust toolchain + cargo - https://rustup.rs/
- `cargo install just`

## use just

type `just go` to launch the python stuff
type `just mvn` to mvn install the working pom (need maven and jdk21)
type `just mvnbroken` to mvn install the broken pom
