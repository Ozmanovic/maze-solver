from maze_app import main
import argparse

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Maze Generator & Solver')
    parser.add_argument('--width', type=int, default=1280, help='Window width (default: 1280)')
    parser.add_argument('--height', type=int, default=720, help='Window height (default: 720)')
    args = parser.parse_args()

    # Run the application with the specified window size
    main(width=args.width, height=args.height)
