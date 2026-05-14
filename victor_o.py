"""Main entrypoint for Victor-O (Victor-Omni)"""

from victor_o.core import VictorO

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Victor-O Unified Runtime")
    parser.add_argument("--ticks", type=int, default=100, help="Number of ticks to run")
    args = parser.parse_args()

    system = VictorO()
    system.run(args.ticks)
