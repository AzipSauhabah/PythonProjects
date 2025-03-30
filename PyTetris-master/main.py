from src.runner import GameRunner
from memory_profiler import profile
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

@profile
def main():
    gr = GameRunner()
    gr.game_run()

if __name__=="__main__":
    main()