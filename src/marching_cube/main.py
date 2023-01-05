from marching_cube import MarchingCube


def main():
    # specificState = 139 error
    marching_cube = MarchingCube(verbose=True, specificState=193)
    marching_cube.run()


if __name__ == '__main__':
    main()
